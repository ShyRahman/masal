"""Read Masal's results from the private inbox repo, decrypt them locally and print a summary.
Needs: gh (logged in), node, and the private key at ~/.maths-inbox/private.pem. Usage: python3 read_inbox.py [--raw] [owner/repo]"""
import json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith('--')]; repo = args[0] if args else 'ShyRahman/maths-inbox'
issues = json.loads(subprocess.run(['gh', 'api', f'repos/{repo}/issues?state=all&per_page=100&sort=created&direction=asc', '--paginate'], capture_output=True, text=True, check=True).stdout.replace('][', ','))
bank = json.loads(subprocess.run(['node', '-e', f"const m=require('{here}/questions.js');console.log(JSON.stringify({{T:m.TOPICS,Q:m.QUICK.qs.concat(m.CHECK2.qs)}}))"], capture_output=True, text=True, check=True).stdout)
topics = {t['id']: t['label'] for t in bank['T']}; parts = {q['id'] + p['id']: (q, p) for q in bank['Q'] for p in q['parts']}
A, C, P, log = {}, {}, {}, []
for i in issues:
    try:
        d = json.loads(subprocess.run(['node', os.path.join(here, 'inbox_decrypt.js')], input=i['body'], capture_output=True, text=True, check=True).stdout)
    except Exception: continue                       # not one of ours (or tampered): ignore
    log.append((d['when'], d['kind'])); A.update(d.get('a', {})); C.update(d.get('c', {})); P.update(d.get('p', {}).get('main', d.get('p', {})))
# Parent overrides (kept on this Mac, not in any repo): {"q27a": {"st": "right", "note": "..."}}
ovp = os.path.expanduser('~/.maths-inbox/overrides.json')
OV = json.load(open(ovp)) if os.path.exists(ovp) else {}
for k, o in OV.items():
    if k in A: A[k] = dict(A[k], st=o['st'], overridden=True)
if '--raw' in sys.argv: print(json.dumps({'a': A, 'c': C, 'p': P}, indent=1)); sys.exit()
SURE = {3: 'pretty sure', 2: 'not sure', 1: 'guessing'}   # 0 with an answer = she did not tap how sure; 0 with no answer = skipped
kinds = {k: sum(1 for _, x in log if x == k) for k in ('topics', 'topics2', 'progress', 'finish', 'finish2')}
print(f'{len(log)} submissions (' + ', '.join(f'{n} {k}' for k, n in kinds.items() if n) + ')' + (f', latest {max(w for w, _ in log)}' if log else '') + f'; {len(A)} answers, {len(C)} topics rated' + ('; part 1 FINISHED' if kinds['finish'] else '; part 1 not finished') + ('; part 2 FINISHED' if kinds['finish2'] else '; part 2 not finished' if any(k.startswith('q') and int(k[1:3]) in (8,11,28,29,30,32,33,35,37,38,39,40) for k in A) else '') if log else '')
if P: print('Feeling:', P.get('feeling'), '| Hardest:', P.get('hardest'))
from fractions import Fraction
def exp(p):
    k = p['kind']
    if k == 'num':
        f = Fraction(p['exp']).limit_denominator(64)
        return str(f) if abs(float(f) - p['exp']) < 1e-9 else str(round(p['exp'], 4))
    return {'mc': lambda: p['options'][p['correct']], 'alg': lambda: p['variants'][0], 'prime': lambda: p['exp'], 'sf': lambda: p['exp']}.get(k, lambda: '')()
print('\nWhat she says vs what she did')
for t in [t for t in bank['T'] if t.get('core') or t.get('core2')]:
    mine = [(k, A[k]) for k in A if k in parts and parts[k][0]['topic'] == t['id']]
    res = {s: sum(1 for _, r in mine if r['st'] == s) for s in ('right', 'wrong', 'check', 'skip')}
    print(f"  {t['label']:<38} says {C.get(t['id'], {}).get('level', '-'):<7} -> " + (', '.join(f'{n} {s}' for s, n in res.items() if n) or 'no answers'))
print('\nAnswers (id | her answer | expected | mark | how sure)')
for k, r in sorted(A.items()):
    if k in parts: print(f"  {k:<6} | {r.get('raw') or '(blank)'!s:<22} | {exp(parts[k][1])!s:<16} | {r['st']:<6} | {SURE.get(r.get('sure')) or ('skipped' if r['st'] == 'skip' else 'not stated')}" + ('  <- parent override' if r.get('overridden') else ''))
sw = [k for k, r in A.items() if r.get('sure') == 3 and r['st'] == 'wrong']
print('\nPretty sure but wrong:', ', '.join(sw) or 'none')
