# Masal's study space

A phone-friendly study site. The main page is a subject picker (Maths now, Science later); Maths starts with a short check-in: rate 12 topics, then answer 12 questions. Plain HTML/JS, no framework, hosted on GitHub Pages at https://shyrahman.github.io/masal/. To add a subject: add a tile in `viewHub()` and a `viewX()` route in `app.src.html`.

## How results travel
1. She fills in the page. Her answers stay in her browser while she works.
2. When she taps Done on the topics, and when she finishes the questions, the page **encrypts** her results in the browser with a public key, then files the encrypted blob as an issue in a **private** inbox repo, using a token that can only write issues to that one repo.
3. Only the private key (kept on the parent's computer, never in any repo) can decrypt. A leaked token or link therefore exposes nothing readable.
4. `python3 read_inbox.py` fetches the issues with `gh`, decrypts them locally and prints a summary.

If the token is missing or the send fails, the page shows a paste-a-code button instead.

## Files
- `app.src.html`, `marker.js`, `questions.js`: sources. `build.py` assembles `dist/site/index.html` (gitignored; the workflow builds it).
- `inbox-public-key.txt`: the public key (safe to publish). `inbox_decrypt.js`, `read_inbox.py`: parent-side tools.
- `.github/workflows/pages.yml`: builds and deploys. Needs the repository secret `INBOX_TOKEN` (fine-grained token, Issues: read and write, on the inbox repo only).
- Tests: `node test.js` (answer marking); `python3 smoke_hosted.py <tmpdir>` (encrypt, send, decrypt round trip with a throwaway key); `python3 smoke_test.py <tmpdir>` (the claude.ai artifact build). Headless Google Chrome is required for the smoke tests.

Do not add the Corbettmaths PDFs, results, keys or photos of the exercise book here.
