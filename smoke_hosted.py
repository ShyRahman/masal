"""Hosted (standalone) copy: serves dist/site over http://localhost and checks the automatic Netlify-form send, with fetch stubbed.
Usage: python3 platform/smoke_hosted.py <tmpdir>"""
import os, sys, re, json, base64, subprocess, threading, http.server, socketserver, functools, html as H
here = os.path.dirname(os.path.abspath(__file__)); tmp = sys.argv[1]
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
site = os.path.join(here, 'dist', 'site')
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
Handler = functools.partial(Q, directory=site)
httpd = socketserver.TCPServer(('127.0.0.1', 0), Handler); port = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()
fails = 0
def check(l, c):
    global fails; print('PASS' if c else 'FAIL', l); fails += 0 if c else 1

def run(name, fetch_stub, script):
    # the harness page is the real index.html plus a stub and a driver, served from the same origin so location.protocol is http:
    src = open(os.path.join(site, 'index.html')).read()
    inj = ('<script>window.__posts=[];window.fetch=' + fetch_stub + ';</script>')
    drv = ('<pre id="res"></pre><script>(async function(){var w=function(m){return new Promise(function(r){setTimeout(r,m)})};var o={};try{' + script +
           '}catch(e){o.error=String(e)}o.posts=window.__posts;document.getElementById("res").textContent=JSON.stringify(o)})()</script>')
    out_html = src.replace('<form name="results"', inj + '<form name="results"', 1).replace('</body>', drv + '</body>')
    open(os.path.join(site, '_t_' + name + '.html'), 'w').write(out_html)
    try:
        r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=15000', '--dump-dom', f'http://127.0.0.1:{port}/_t_{name}.html'], capture_output=True, text=True, timeout=90)
    finally:
        os.remove(os.path.join(site, '_t_' + name + '.html'))
    m = re.search(r'<pre id="res">(.*?)</pre>', r.stdout, re.S)
    return json.loads(H.unescape(m.group(1))) if m else {'error': 'no result'}

FLOW = """
await w(500); o.home = document.body.innerText;
location.hash = '#confidence'; await w(150);
document.querySelector('.topic[data-t="fractions"] .chip[data-l="wobbly"]').click();
document.getElementById('confDone').click(); await w(200);
location.hash = '#round-q'; await w(150);
document.querySelector('#in-q01a').value = '168'; document.querySelector('[data-s="3"]').click(); document.querySelector('#next').click(); await w(100);
for (var i = 0; i < 11; i++) { document.querySelector('#skip').click(); await w(40); }
await w(300);
o.end = document.body.innerText;
"""
ok = run('ok', "function(u,x){window.__posts.push({u:u,m:x.method,h:x.headers,b:x.body});return Promise.resolve({ok:true,status:200})}", FLOW)
check('hosted: no JS error', 'error' not in ok)
check('hosted: no scary "not connected" banner, no Send button', 'not connected' not in ok['home'] and 'Send my results' not in ok['home'])
posts = ok.get('posts', [])
check('hosted: topics sent when she taps Done', any('kind=topics' in p['b'] for p in posts))
fin = [p for p in posts if 'kind=finish' in p['b']]
check('hosted: finish sent exactly once, to / as a form post', len(fin) == 1 and fin[0]['u'] == '/' and fin[0]['m'] == 'POST' and 'form-name=results' in fin[0]['b'] and 'x-www-form-urlencoded' in json.dumps(fin[0]['h']))
if fin:
    from urllib.parse import parse_qs
    code = parse_qs(fin[0]['b'])['code'][0]
    j = json.loads(base64.b64decode(code).decode())
    check('hosted: payload decodes to all 12 questions with q01a right', len({v['q'] for v in j['a'].values()}) == 12 and j['a']['q01a']['st'] == 'right')
check('hosted: she is told it was sent', 'Sent to your parent' in ok['end'])
check('hosted: form is in the page for Netlify to detect', 'data-netlify="true"' in open(os.path.join(site, 'index.html')).read())

bad = run('bad', "function(u,x){window.__posts.push({b:x.body});return Promise.reject(new Error('offline'))}", FLOW)
check('hosted failure: no JS error', 'error' not in bad)
check('hosted failure: she is told, and gets the Send my results fallback', 'Could not send automatically' in bad['end'] and 'Send my results' in bad['end'])
check('hosted failure: finish is not re-sent in a loop', len([p for p in bad['posts'] if 'kind=finish' in p['b']]) == 1)
httpd.shutdown()
print('\n%d FAILED' % fails if fails else '\nall hosted checks passed'); sys.exit(1 if fails else 0)
