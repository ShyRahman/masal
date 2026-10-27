"""Headless-Chrome smoke test of dist/masal-maths-checkin.html with an in-memory stand-in for window.claude (db + user).
Usage: python3 platform/smoke_test.py <tmpdir>   Prints PASS/FAIL lines. Cannot test real claude.ai sharing or sign-in."""
import os, sys, json, re, subprocess
here = os.path.dirname(os.path.abspath(__file__)); tmp = sys.argv[1]
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
page = open(os.path.join(here, 'dist', 'masal-maths-checkin.html')).read()

STUB = """<script>
window.__store = %SEED%;
(function(){
  var subs = [];
  function col(name){ window.__store[name] = window.__store[name] || {}; return {
    doc: function(id){ return { set: async function(d){ window.__store[name][id] = JSON.parse(JSON.stringify(d)); fire(); },
                                delete: async function(){ delete window.__store[name][id]; fire(); } }; },
    onSnapshot: function(cb){ var f = function(){ var s = window.__store[name] || {}; cb({ docs: Object.keys(s).map(function(k){ return { id:k, data:function(){ return s[k]; } }; }) }); }; subs.push(f); setTimeout(f,0); return function(){}; } }; }
  function fire(){ setTimeout(function(){ subs.forEach(function(f){ f(); }); }, 0); }
  var USER = %USER%;
  window.claude = { use: async function(n){
    if (n === 'user') return { isOwner: async()=>USER.owner, canEdit: async()=>USER.owner, can: async()=>USER.write };
    if (n === 'db') return USER.db ? { collection: col } : null; return null; } };
})();
</script>"""

def run(name, seed, user, script):
    html = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'
            + STUB.replace('%SEED%', json.dumps(seed)).replace('%USER%', json.dumps(user)) + page +
            '<pre id="res"></pre><script>(async function(){var wait=function(ms){return new Promise(function(r){setTimeout(r,ms)})};var out={};try{' + script + '}catch(e){out.error=String(e&&e.stack||e)}document.getElementById("res").textContent=JSON.stringify(out);})();</script></body></html>')
    p = os.path.join(tmp, name + '.html'); open(p, 'w').write(html)
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=15000', '--dump-dom', 'file://' + p], capture_output=True, text=True, timeout=90)
    m = re.search(r'<pre id="res">(.*?)</pre>', r.stdout, re.S)
    if not m: print('FAIL', name, 'no result; stderr:', r.stderr[-300:]); return None
    import html as H; return json.loads(H.unescape(m.group(1)))

fails = 0
def check(label, cond):
    global fails
    print('PASS' if cond else 'FAIL', label)
    fails += 0 if cond else 1

# Masal on a phone where saving works: 12 topics, then the 12 questions
CHILD = """
await wait(400);
out.homeText = document.body.innerText;
location.hash = '#confidence'; await wait(150);
out.topicRows = document.querySelectorAll('.topic').length;
document.querySelector('.topic[data-t="fractions"] .chip[data-l="wobbly"]').click();
document.querySelector('.topic[data-t="expand2"] .chip[data-l="lost"]').click();
var h = document.querySelector('#hardest'); h.value = 'two brackets'; h.dispatchEvent(new Event('change'));
document.querySelector('[data-f="2"]').click(); await wait(200);
location.hash = '#round-q'; await wait(150);
out.header = document.querySelector('.row.spread .muted.small').textContent;
out.q1 = document.querySelector('.stem').textContent;
document.querySelector('#in-q01a').value = '168'; document.querySelector('#in-q01b').value = '250';
document.querySelector('[data-s="3"]').click(); document.querySelector('#next').click(); await wait(150);
document.querySelector('#skip').click(); await wait(150);
document.querySelector('#in-q05a').value = '17/12'; document.querySelector('#next').click(); await wait(150);
out.afterQ5 = document.querySelector('.stem').textContent;
for (var i = 0; i < 9; i++) { document.querySelector('#skip').click(); await wait(60); }
out.endTitle = document.querySelector('h2').textContent;
out.endText = document.body.innerText;
await wait(300);
out.store = window.__store;
"""
res = run('child', {}, {'owner': False, 'write': True, 'db': True}, CHILD)
if res:
    check('child: no JS error', 'error' not in res)
    check('child: home has just two steps, no optional extras', 'How do you feel' in res['homeText'] and '12 questions' in res['homeText'] and 'Go deeper' not in res['homeText'] and 'optional' not in res['homeText'].lower())
    check('child: no Send-my-results button while saving works', 'Send my results' not in res['homeText'])
    check('child: confidence has exactly 12 topics', res.get('topicRows') == 12)
    check('child: question header "1 of 12"', 'question 1 of 12' in res.get('header', ''))
    a = res['store'].get('answers', {})
    check('child: q01a right + sure', a.get('q01a', {}).get('st') == 'right' and a['q01a']['sure'] == 3)
    check('child: q01b wrong', a.get('q01b', {}).get('st') == 'wrong')
    check('child: q03 skipped saved', a.get('q03a', {}).get('st') == 'skip' and a['q03a'].get('skipped') is True)
    check('child: q05 mixed number right', a.get('q05a', {}).get('st') == 'right')
    check('child: moved on to q07 (percent)', '£240' in res.get('afterQ5', ''))
    check('child: all 12 questions recorded', len({v['q'] for v in a.values()}) == 12)
    check('child: finish screen', 'All done' in res.get('endTitle', ''))
    check('child: finish screen has no Send button and no next-round', 'Send my results' not in res['endText'] and 'Next:' not in res['endText'])
    check('child: confidence saved', res['store'].get('confidence', {}).get('expand2', {}).get('level') == 'lost')
    check('child: profile saved', res['store'].get('profile', {}).get('main', {}).get('feeling') == 2 and res['store']['profile']['main'].get('hardest') == 'two brackets')

# saving not connected (not signed in): works locally and offers the paste-a-code fallback
NOSAVE = """
await wait(400);
out.home = document.body.innerText;
location.hash = '#round-q'; await wait(150);
document.querySelector('#in-q01a').value = '168'; document.querySelector('#next').click(); await wait(100);
out.stored = localStorage.getItem('masal-baseline-v1') ? JSON.parse(localStorage.getItem('masal-baseline-v1')).a.q01a : null;
"""
res = run('nosave', {}, {'owner': False, 'write': None, 'db': False}, NOSAVE)
if res:
    check('no-db: says answers stay on this phone and offers Send my results', 'stay on this phone' in res['home'] and 'Send my results' in res['home'])
    check('no-db: answer kept on the phone', res.get('stored') and res['stored']['st'] == 'right')

SEED = {'answers': {
  'q15a': {'r':'q','q':'q15','p':'a','topic':'expand2','raw':'3y^2+7y-20','st':'check','sure':3,'secs':40,'at':'2026-10-28T18:00:00.000Z'},
  'q13a': {'r':'q','q':'q13','p':'a','topic':'expand1','raw':'4x+5','st':'right','sure':1,'secs':30,'at':'2026-10-28T17:59:00.000Z'},
  'q27b': {'r':'q','q':'q27','p':'b','topic':'stdform','raw':'12x10^3','st':'wrong','sure':3,'secs':50,'at':'2026-10-28T18:05:00.000Z'},
  'q01a': {'r':'q','q':'q01','p':'a','topic':'tables','raw':'168','st':'right','sure':3,'secs':20,'at':'2026-10-28T17:00:00.000Z'},
  'q05a': {'r':'q','q':'q05','p':'a','topic':'fractions','raw':'17/12','st':'right','sure':2,'secs':20,'at':'2026-10-28T17:01:00.000Z'}},
  'confidence': {'expand2': {'level':'lost'}, 'tables': {'level':'got'}, 'fractions': {'level':'wobbly'}, 'stdform': {'level':'got'}},
  'profile': {'main': {'hardest':'brackets <b>x</b>', 'feeling': 2}}}
OWNER = """
await wait(400);
out.home = document.body.innerText;
location.hash = '#parent'; await wait(250);
out.h1 = document.querySelector('h1').textContent;
out.text = document.body.innerText;
out.xssSafe = ![].slice.call(document.querySelectorAll('#app b')).some(function(b){return b.textContent === 'x'});
var btn = document.querySelector('.ov[data-id="q15a"] button[data-o="right"]'); btn.click(); await wait(250);
out.review = window.__store.reviews && window.__store.reviews.q15a;
location.hash = '#round-q'; await wait(150);
out.banner = (document.querySelector('.banner') || {}).textContent || '';
out.header = document.querySelector('.row.spread .muted.small').textContent;
document.querySelector('#in-q03a').value = '1'; document.querySelector('#next').click(); await wait(100);
out.ownerPreviewSaved = !!(window.__store.answers && window.__store.answers.q03a);
"""
res = run('owner', SEED, {'owner': True, 'write': True, 'db': True}, OWNER)
if res:
    t = res.get('text', '')
    check('owner: no JS error', 'error' not in res)
    check('owner: home has Parent view link', 'Parent view' in res['home'])
    check('owner: parent view renders', res.get('h1', '').startswith('Masal'))
    check('owner: tile counts 5 answers of 16 parts', '5 / 16' in t)
    check('owner: only the 12 core topics are listed', t.count('not rated') + t.count('Got it') + t.count('Wobbly') + t.count('Lost') >= 8 and 'Angles in polygons' not in t)
    check('owner: flags "says confident, got some wrong"', 'Says confident, got some wrong' in t)
    check('owner: flags "better than she thinks"', 'Better than she thinks' in t)
    check('owner: sure-but-wrong list names q27b', 'q27b' in t)
    check('owner: guessing-but-right list names q13a', 'q13a' in t)
    check('owner: her free text is escaped', res.get('xssSafe') is True and 'brackets <b>x</b>' in t)
    check('owner: override saved to reviews', (res.get('review') or {}).get('st') == 'right')
    check('owner: question page is in preview mode and resumes at the unanswered ones (12 - 5 = 7)', 'Preview mode' in res.get('banner', '') and 'of 7' in res.get('header', ''))
    check('owner: preview answers are not saved', res.get('ownerPreviewSaved') is False)

VIEWER = "await wait(400); location.hash = '#parent'; await wait(200); out.text = document.body.innerText;"
res = run('viewer', SEED, {'owner': False, 'write': True, 'db': True}, VIEWER)
if res: check('child cannot open the parent view', 'only for the person who set this page up' in res.get('text', '') and 'where things stand' not in res.get('text', ''))
print('\n%d FAILED' % fails if fails else '\nall smoke checks passed'); sys.exit(1 if fails else 0)
