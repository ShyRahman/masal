"""Assemble dist/masal-maths-checkin.html from app.src.html + marker.js + questions.js (run test.js first: node platform/test.js)."""
import os
here = os.path.dirname(os.path.abspath(__file__))
rd = lambda n: open(os.path.join(here, n)).read()
html = rd('app.src.html').replace('/*MARKER*/', rd('marker.js')).replace('/*QUESTIONS*/', rd('questions.js'))
os.makedirs(os.path.join(here, 'dist'), exist_ok=True)
open(os.path.join(here, 'dist', 'masal-maths-checkin.html'), 'w').write(html)
print(len(html), 'bytes')

# Hosted copy: the same page as an ordinary web page (GitHub Pages). Three values are filled in here and never committed:
#   INBOX_REPO (default ShyRahman/maths-inbox), INBOX_TOKEN (env only: a fine-grained token with Issues write on that one private repo),
#   INBOX_PUBKEY (inbox-public-key.txt: the parent's PUBLIC key; the private key never leaves the parent's computer).
# Without INBOX_TOKEN the placeholder stays and the page offers the paste-a-code button instead of sending.
repo = os.environ.get('INBOX_REPO', 'ShyRahman/maths-inbox')
token = os.environ.get('INBOX_TOKEN') or '__INBOX_TOKEN__'   # empty counts as not configured
pub = os.environ.get('INBOX_PUBKEY') or (open(os.path.join(here, 'inbox-public-key.txt')).read().strip() if os.path.exists(os.path.join(here, 'inbox-public-key.txt')) else '__INBOX_PUBKEY__')
hosted = html.replace('__INBOX_REPO__', repo).replace('__INBOX_TOKEN__', token).replace('__INBOX_PUBKEY__', pub)
wrap = ('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="robots" content="noindex,nofollow">'
        '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui}[hidden]{display:none!important}</style>'
        '</head><body>' + hosted + '</body></html>')
site = os.path.join(here, 'dist', 'site'); os.makedirs(site, exist_ok=True)
open(os.path.join(site, 'index.html'), 'w').write(wrap)
open(os.path.join(site, 'robots.txt'), 'w').write('User-agent: *\nDisallow: /\n')
open(os.path.join(site, '.nojekyll'), 'w').write('')
print('hosted page', len(wrap), 'bytes; token configured:', not token.startswith('__'))
