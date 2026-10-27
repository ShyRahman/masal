# Masal's maths check-in

A phone-friendly maths baseline: rate 12 topics, then answer 12 questions. Plain HTML/JS, no framework.

- `app.src.html`, `marker.js`, `questions.js` are the sources. `python3 build.py` assembles `dist/site/index.html` (what Netlify serves) plus a copy for claude.ai artifacts.
- The hosted page posts results to a Netlify Form named `results` when she finishes the topics and the questions. The `code` field is base64 JSON of her answers.
- Tests: `node test.js` (answer marking), `python3 smoke_test.py <tmpdir>` (artifact version, stand-in database), `python3 smoke_hosted.py <tmpdir>` (hosted version, stub fetch). Headless Google Chrome is needed for the smoke tests.
- Deploy: Netlify is linked to this repo with publish directory `dist/site` (set in `netlify.toml`). Commit the rebuilt `dist/site/` and push.

No personal data beyond a first name is in this repo. Do not add the Corbettmaths PDFs or any photos of the exercise book here.
