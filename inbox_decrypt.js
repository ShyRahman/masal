// Decrypts one result blob ({v,k,iv,ct}, as filed by the page) read from stdin. Usage: node inbox_decrypt.js [private.pem]   (default ~/.maths-inbox/private.pem)
const c = require('crypto'), fs = require('fs'), os = require('os'), path = require('path');
const pem = fs.readFileSync(process.argv[2] || path.join(os.homedir(), '.maths-inbox', 'private.pem'));
let raw = ''; process.stdin.on('data', d => raw += d).on('end', () => {
  const b = JSON.parse(raw), key = c.privateDecrypt({ key: pem, oaepHash: 'sha256', padding: c.constants.RSA_PKCS1_OAEP_PADDING }, Buffer.from(b.k, 'base64'));
  const ct = Buffer.from(b.ct, 'base64'), d = c.createDecipheriv('aes-256-gcm', key, Buffer.from(b.iv, 'base64'));
  d.setAuthTag(ct.subarray(ct.length - 16));                       // WebCrypto appends the GCM tag to the ciphertext
  process.stdout.write(Buffer.concat([d.update(ct.subarray(0, ct.length - 16)), d.final()]).toString('utf8'));
});
