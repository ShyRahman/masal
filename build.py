"""Assemble dist/masal-maths-checkin.html from app.src.html + marker.js + questions.js (run test.js first: node platform/test.js)."""
import os
here = os.path.dirname(os.path.abspath(__file__))
rd = lambda n: open(os.path.join(here, n)).read()
html = rd('app.src.html').replace('/*MARKER*/', rd('marker.js')).replace('/*QUESTIONS*/', rd('questions.js'))
os.makedirs(os.path.join(here, 'dist'), exist_ok=True)
open(os.path.join(here, 'dist', 'masal-maths-checkin.html'), 'w').write(html)
print(len(html), 'bytes')

# Standalone copy: the same page wrapped as an ordinary web page, for hosting anywhere (no claude.ai needed).
# With no window.claude the page runs offline-mode: answers stay on her phone and "Send my results" gives a code to paste into the parent view.
wrap = ('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui}[hidden]{display:none!important}</style>'
        '</head><body><form name="results" method="POST" data-netlify="true" netlify-honeypot="bot-field" hidden><input name="bot-field"><input name="kind"><input name="when"><textarea name="code"></textarea></form>' + html + '</body></html>')
open(os.path.join(here, 'dist', 'masal-maths-checkin-standalone.html'), 'w').write(wrap)
print('standalone', len(wrap), 'bytes')

# Netlify wants a folder containing index.html
os.makedirs(os.path.join(here, 'dist', 'site'), exist_ok=True)
open(os.path.join(here, 'dist', 'site', 'index.html'), 'w').write(wrap)
open(os.path.join(here, 'dist', 'site', 'robots.txt'), 'w').write('User-agent: *\nDisallow: /\n')   # ask search engines not to list it
