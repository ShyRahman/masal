"""Hosted copy (GitHub Pages build): serves it over http://localhost with fetch stubbed, and proves the whole encrypted path:
the page encrypts in the browser -> POST to the GitHub issues API -> inbox_decrypt.js decrypts with a temporary private key.
Usage: python3 smoke_hosted.py <tmpdir>      (run python3 build.py first)"""
import os, sys, re, json, subprocess, threading, http.server, socketserver, functools, html as H
here = os.path.dirname(os.path.abspath(__file__)); tmp = sys.argv[1]
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
site = os.path.join(here, 'dist', 'site')
# throwaway keypair for the test only
kp = subprocess.run(['node', '-e', "const c=require('crypto');const k=c.generateKeyPairSync('rsa',{modulusLength:3072});process.stdout.write(JSON.stringify({pub:k.publicKey.export({type:'spki',format:'der'}).toString('base64'),priv:k.privateKey.export({type:'pkcs8',format:'pem'})}))"], capture_output=True, text=True, check=True)
kp = json.loads(kp.stdout); privpath = os.path.join(tmp, 'test-private.pem'); open(privpath, 'w').write(kp['priv'])
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
httpd = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=tmp)); port = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()
fails = 0
def check(l, c):
    global fails; print('PASS' if c else 'FAIL', l); fails += 0 if c else 1
base = open(os.path.join(site, 'index.html')).read()
def run(name, page, fetch_stub, script):
    inj = '<script>window.__posts=[];window.fetch=' + fetch_stub + ';</script>'
    drv = ('<pre id="res"></pre><script>(async function(){var w=function(m){return new Promise(function(r){setTimeout(r,m)})};var o={};try{' + script +
           '}catch(e){o.error=String(e)}o.posts=window.__posts;document.getElementById("res").textContent=JSON.stringify(o)})()</script>')
    out_html = page.replace('<body>', '<body>' + inj, 1).replace('</body>', drv + '</body>')
    p = os.path.join(tmp, '_h_' + name + '.html'); open(p, 'w').write(out_html)
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=20000', '--dump-dom', f'http://127.0.0.1:{port}/_h_{name}.html'], capture_output=True, text=True, timeout=120)
    m = re.search(r'<pre id="res">(.*?)</pre>', r.stdout, re.S)
    return json.loads(H.unescape(m.group(1))) if m else {'error': 'no result'}
realpub = open(os.path.join(here, 'inbox-public-key.txt')).read().strip()
assert realpub in base, 'build.py should have put the public key in the page'
configured = base.replace('__INBOX_TOKEN__', 'test-token-123').replace(realpub, kp['pub']).replace('ShyRahman/maths-inbox', 'test/inbox')
FLOW = """
await w(500); o.hub = document.body.innerText; location.hash = '#maths'; await w(150); o.home = document.body.innerText;
location.hash = '#confidence'; await w(150);
document.querySelector('.topic[data-t="fractions"] .chip[data-l="wobbly"]').click();
var h = document.querySelector('#hardest'); h.value = 'two brackets'; h.dispatchEvent(new Event('change'));
document.querySelector('[data-f="2"]').click();
document.getElementById('confDone').click(); await w(400);
location.hash = '#round-q'; await w(150);
document.querySelector('#in-q01a').value = '168'; document.querySelector('#in-q01b').value = '250'; document.querySelector('[data-s="3"]').click(); document.querySelector('#next').click(); await w(100);
for (var i = 0; i < 11; i++) { document.querySelector('#skip').click(); await w(40); }
await w(600); o.end = document.body.innerText;
"""
STUB_OK = "function(u,x){window.__posts.push({u:u,h:x.headers,b:x.body});return Promise.resolve({ok:true,status:201})}"
ok = run('ok', configured, STUB_OK, FLOW)
check('hosted: no JS error', 'error' not in ok)
check('hosted: opens on the subject picker', "Masal's study space" in ok['hub'] and 'Science' in ok['hub'])
check('hosted: no "not connected" banner and no Send button while sending works', 'not connected' not in ok['home'] and 'Send my results' not in ok['home'])
posts = ok.get('posts', [])
check('hosted: sends go to the inbox repo issues API with the bearer token', len(posts) >= 2 and all(p['u'] == 'https://api.github.com/repos/test/inbox/issues' and p['h'].get('Authorization') == 'Bearer test-token-123' for p in posts))
check('hosted: topics once, a progress checkpoint after questions 4 and 8, finish exactly once', sum('(topics)' in p['b'] for p in posts) == 1 and sum('(progress)' in p['b'] for p in posts) == 2 and sum('(finish)' in p['b'] for p in posts) == 1)
check('hosted: the token and the answers never appear in plain text in what is sent', all('168' not in p['b'] and 'two brackets' not in p['b'] and 'wobbly' not in p['b'] for p in posts))
fin = [json.loads(p['b']) for p in posts if '(finish)' in p['b']]
if fin:
    blob = fin[0]['body']
    d = subprocess.run(['node', os.path.join(here, 'inbox_decrypt.js'), privpath], input=blob, capture_output=True, text=True)
    plain = json.loads(d.stdout) if d.returncode == 0 else {}
    check('round trip: the private key decrypts what the browser encrypted', d.returncode == 0 and plain.get('kind') == 'finish')
    check('round trip: all 12 questions, q01a right and q01b wrong, topic and note present', len({v['q'] for v in plain.get('a', {}).values()}) == 12 and plain['a']['q01a']['st'] == 'right' and plain['a']['q01b']['st'] == 'wrong' and plain['c']['fractions']['level'] == 'wobbly' and plain['p']['hardest'] == 'two brackets')
    other = subprocess.run(['node', os.path.join(here, 'inbox_decrypt.js'), os.path.expanduser('~/.maths-inbox/private.pem')], input=blob, capture_output=True, text=True)
    check('a different private key cannot decrypt it', other.returncode != 0)
check('hosted: she is told it was sent', 'Sent to your parent' in ok['end'])
VIS = """
await w(500); location.hash = '#round-q'; await w(150);
document.querySelector('#in-q01a').value = '168'; document.querySelector('#next').click(); await w(100);
o.before = window.__posts.length;
Object.defineProperty(document, 'visibilityState', { value: 'hidden', configurable: true }); document.dispatchEvent(new Event('visibilitychange')); await w(400);
o.afterHide = window.__posts.length;
document.dispatchEvent(new Event('visibilitychange')); await w(300);   // nothing new since: no duplicate
o.afterAgain = window.__posts.length;
"""
vis = run('vis', configured, STUB_OK, VIS)
check('leaving the page with unsent answers files one progress update (keepalive), and not twice', 'error' not in vis and vis['before'] == 0 and vis['afterHide'] == 1 and vis['afterAgain'] == 1 and '(progress)' in vis['posts'][0]['b'])
bad = run('bad', configured, "function(u,x){window.__posts.push({b:x.body});return Promise.reject(new Error('offline'))}", FLOW)
check('failure: no JS error; she is told and gets the fallback button', 'error' not in bad and 'Could not send automatically' in bad['end'] and 'Send my results' in bad['end'])
check('failure: finish is not re-sent in a loop', len([p for p in bad['posts'] if '(finish)' in p['b']]) == 1)
unconf = run('unconf', base, STUB_OK, FLOW)   # real public key, but no token in the build
check('token not configured: nothing is sent and the paste-a-code fallback is offered', 'error' not in unconf and not unconf['posts'] and 'Send my results' in unconf['end'])
check('the committed/built page has no real token in it unless the build was given one', 'github_pat_' not in base and 'ghp_' not in base)
httpd.shutdown()
print('\n%d FAILED' % fails if fails else '\nall hosted checks passed'); sys.exit(1 if fails else 0)
