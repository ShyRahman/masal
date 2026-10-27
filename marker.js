// Answer marking for the baseline page. Plain functions, no DOM: tested by test.js, inlined by build.py.
// Statuses: 'right' | 'wrong' | 'check' (could not decide: a parent looks) | 'skip'.
// Maths answers have many valid spellings, so anything not recognised is 'check', never 'wrong', except numbers.
var SUPS = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁻':'-'};

function clean(s) {
  s = String(s == null ? '' : s).trim().toLowerCase();
  s = s.replace(/[−–—]/g, '-').replace(/[×·]/g, '*').replace(/÷/g, '/').replace(/π/g, 'pi');
  s = s.replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+/g, function (m) { return '^' + Array.from(m).map(function (c) { return SUPS[c]; }).join(''); });
  return s;
}

// -> {v, pct} or null
function parseNum(raw) {
  var s = clean(raw).replace(/^[a-z]\s*=\s*/, '').replace(/^=\s*/, '');
  s = s.replace(/[£€$]/g, '').replace(/\s*(cm\^?[23]?|m\^?[23]?|km\/h|mph|km|mm|kg|degrees?|sides?|litres?|°|s|g)\s*$/, '').trim();
  var pct = false;
  if (/%$/.test(s)) { pct = true; s = s.slice(0, -1).trim(); }
  s = s.replace(/^\((.*)\)$/, '$1').trim();
  if (/^-?\d{1,3}(?:[ ,]\d{3})+(?:\.\d+)?$/.test(s)) s = s.replace(/[ ,]/g, '');
  var m;
  if ((m = s.match(/^(-?)(\d+)\s+(\d+)\/(\d+)$/))) {
    var d = +m[4]; if (!d) return null;
    return { v: (m[1] ? -1 : 1) * (+m[2] + (+m[3]) / d), pct: pct };
  }
  if ((m = s.match(/^(-?\d+(?:\.\d+)?)\s*\/\s*(\d+(?:\.\d+)?)$/))) {
    if (!+m[2]) return null;
    return { v: +m[1] / +m[2], pct: pct };
  }
  if (/^-?(?:\d+\.?\d*|\.\d+)$/.test(s)) return { v: +s, pct: pct };
  return null;
}

// exp: number. opts.pct: the expected value is itself a percentage (so "37.5%" and "37.5" both mean 37.5).
function markNum(raw, exp, opts) {
  if (!String(raw == null ? '' : raw).trim()) return 'skip';
  var p = parseNum(raw); opts = opts || {};
  if (!p) return 'check';
  var v = p.v;
  if (p.pct && !opts.pct) v = v / 100;
  var tol = 1e-9 * Math.max(1, Math.abs(exp));
  if (Math.abs(v - exp) <= tol) return 'right';
  if (exp !== 0 && Math.abs(v - exp) / Math.abs(exp) <= 0.002) return 'check';   // looks like a rounded version
  return 'wrong';
}

// Polynomial-ish canonical form so 7y+2x == 2x+7y, x^2+2x-15 == -15+2x+x^2, 27b^3a^6 == 27a^6b^3. null if not that shape.
function canonPoly(raw) {
  var s = clean(raw).replace(/\s+/g, '').replace(/\*/g, '');
  if (!s || /[()\/]/.test(s)) return null;
  var terms = s.replace(/-/g, '+-').split('+').filter(Boolean), sum = {};
  for (var i = 0; i < terms.length; i++) {
    var m = terms[i].match(/^(-?)(\d*\.?\d*)((?:[a-z](?:\^-?\d+)?)*)$/);
    if (!m) return null;
    var c = (m[1] ? -1 : 1) * (m[2] === '' ? 1 : +m[2]);
    if (m[2] === '.' || isNaN(c)) return null;
    var vars = {}, re = /([a-z])(?:\^(-?\d+))?/g, mm;
    while ((mm = re.exec(m[3]))) vars[mm[1]] = (vars[mm[1]] || 0) + (mm[2] === undefined ? 1 : +mm[2]);
    var key = Object.keys(vars).sort().map(function (k) { return k + vars[k]; }).join('');
    sum[key] = (sum[key] || 0) + c;
  }
  return Object.keys(sum).filter(function (k) { return sum[k] !== 0; }).sort().map(function (k) { return sum[k] + '|' + k; }).join(';');
}

function strip(s) { return clean(s).replace(/\s+/g, '').replace(/^[a-z]=/, ''); }

function markAlg(raw, variants) {
  if (!String(raw == null ? '' : raw).trim()) return 'skip';
  var c = canonPoly(raw), t = strip(raw);
  for (var i = 0; i < variants.length; i++) {
    if (c !== null && canonPoly(variants[i]) === c) return 'right';
    if (strip(variants[i]) === t) return 'right';
  }
  return 'check';
}

// "2^3 x 3^2" style: bases sorted, exponents compared. Expects a full prime factorisation.
function primeMap(raw) {
  var s = clean(raw).replace(/\s+/g, '').replace(/([\d)])x(?=[\d(])/g, '$1*');
  if (!/^\d+(\^\d+)?(\*\d+(\^\d+)?)*$/.test(s)) return null;
  var map = {};
  s.split('*').forEach(function (f) { var a = f.split('^'); map[a[0]] = (map[a[0]] || 0) + (a[1] ? +a[1] : 1); });
  return Object.keys(map).map(Number).sort(function (a, b) { return a - b; }).map(function (k) { return k + '^' + map[k]; }).join('*');
}
function markPrime(raw, exp) {
  if (!String(raw == null ? '' : raw).trim()) return 'skip';
  var a = primeMap(raw);
  return a === null ? 'check' : (a === primeMap(exp) ? 'right' : 'wrong');
}

// Standard form: expected is a number. A numerically right answer that is not A x 10^n with 1<=A<10 is 'check'.
function parseSF(raw) {
  var s = clean(raw).replace(/\s+/g, '').replace(/([\d.])x(?=10)/g, '$1*');
  var m = s.match(/^(-?\d*\.?\d+)\*10\^\(?(-?\d+)\)?$/) || s.match(/^(-?\d*\.?\d+)e(-?\d+)$/);
  return m ? { m: +m[1], e: +m[2] } : null;
}
function markSF(raw, exp) {
  if (!String(raw == null ? '' : raw).trim()) return 'skip';
  var p = parseSF(raw), v;
  if (p) v = p.m * Math.pow(10, p.e);
  else { var q = parseNum(raw); if (!q || q.pct) return 'check'; v = q.v; }
  if (Math.abs(v - exp) > 1e-9 * Math.abs(exp)) return 'wrong';
  return p && Math.abs(p.m) >= 1 && Math.abs(p.m) < 10 ? 'right' : 'check';
}

function markPart(part, raw) {
  var blank = !String(raw == null ? '' : raw).trim();
  if (blank) return 'skip';
  switch (part.kind) {
    case 'num': {
      var r = markNum(raw, part.exp, { pct: part.pct }), f = part.simplest && clean(raw).replace(/\s+/g, '').match(/^(\d+)\/(\d+)$/);
      if (r === 'right' && f) { var x = +f[1], y = +f[2]; while (y) { var tmp = y; y = x % y; x = tmp; } if (x > 1) return 'check'; }   // right value, not in simplest form
      return r;
    }
    case 'alg': return markAlg(raw, part.variants);
    case 'prime': return markPrime(raw, part.exp);
    case 'sf': return markSF(raw, part.exp);
    case 'mc': return String(raw) === String(part.correct) ? 'right' : 'wrong';
    default: return 'check';          // free-text explanation
  }
}

if (typeof module !== 'undefined') module.exports = { clean: clean, parseNum: parseNum, markNum: markNum, canonPoly: canonPoly, markAlg: markAlg, markPrime: markPrime, markSF: markSF, markPart: markPart };
