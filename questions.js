// Question bank for the baseline page: the same 37 questions as gcse-maths/scripts/build_diagnostic.py, split into parts for phone entry.
// Display markup: ^{..} superscript, {a//b} stacked fraction.  Parts: kind num|alg|prime|sf|mc|text.
// `exp` for num/sf is a number; `variants` for alg are accepted spellings (order of terms is handled by the marker).
var TOPICS = [
  { id: 'tables', core: true, strand: 'Number', label: 'Times tables' },
  { id: 'rounding', core: true, strand: 'Number', label: 'Rounding and estimating' },
  { id: 'negatives', strand: 'Number', label: 'Negative numbers' },
  { id: 'fractions', core: true, strand: 'Number', label: 'Fractions' },
  { id: 'percent', core: true, strand: 'Number', label: 'Percentages' },
  { id: 'ratio', core: true, strand: 'Number', label: 'Ratio and sharing' },
  { id: 'primes', strand: 'Number', label: 'Prime factors, HCF and LCM' },
  { id: 'fdp', strand: 'Number', label: 'Fractions, decimals and percentages' },
  { id: 'collect', strand: 'Algebra', label: 'Collecting like terms' },
  { id: 'expand1', core: true, strand: 'Algebra', label: 'Expanding brackets' },
  { id: 'expand2', core: true, strand: 'Algebra', label: 'Expanding two brackets' },
  { id: 'equations', core: true, strand: 'Algebra', label: 'Solving equations' },
  { id: 'subject', core: true, strand: 'Algebra', label: 'Changing the subject of a formula' },
  { id: 'factorise', strand: 'Algebra', label: 'Factorising' },
  { id: 'sequences', core: true, strand: 'Algebra', label: 'Sequences and nth term' },
  { id: 'algfrac', strand: 'Algebra', label: 'Algebraic fractions' },
  { id: 'indices', strand: 'Indices', label: 'Index laws' },
  { id: 'negfrac', strand: 'Indices', label: 'Negative and fractional indices' },
  { id: 'stdform', core: true, strand: 'Indices', label: 'Standard form' },
  { id: 'angles', strand: 'Shape and measures', label: 'Angles in polygons' },
  { id: 'circles', strand: 'Shape and measures', label: 'Circles: area and circumference' },
  { id: 'pythag', strand: 'Shape and measures', label: 'Pythagoras' },
  { id: 'units', strand: 'Shape and measures', label: 'Units, area conversions and speed' },
  { id: 'averages', strand: 'Data and money', label: 'Mean, median and range' },
  { id: 'prob', core: true, strand: 'Data and money', label: 'Probability' },
  { id: 'money', strand: 'Data and money', label: 'Money: interest, currency, best buys' }
];

var ROUNDS = [
  { id: 'a', title: 'Round A', sub: 'Number and fractions', mins: 15, qs: [
    { id: 'q01', topic: 'tables', calc: false, stem: 'Work these out in your head or on paper.', parts: [
      { id: 'a', label: '12 × 14', kind: 'num', exp: 168 }, { id: 'b', label: '15 × 16', kind: 'num', exp: 240 }] },
    { id: 'q02', topic: 'rounding', stem: 'Round 0.04752 to <b>2 significant figures</b>.', parts: [{ id: 'a', kind: 'num', exp: 0.048 }] },
    { id: 'q03', topic: 'rounding', stem: 'Estimate &nbsp;(6.8 × 31.2) ÷ 0.52 &nbsp;by rounding each number to 1 significant figure. Give the answer to your estimate.', parts: [{ id: 'a', kind: 'num', exp: 420 }] },
    { id: 'q04', topic: 'negatives', stem: 'Work out &nbsp;−7 − (−3) + 2 × (−4)', parts: [{ id: 'a', kind: 'num', exp: -12 }] },
    { id: 'q05', topic: 'fractions', stem: 'Work out &nbsp;{3//4} + {2//3}. &nbsp;Give your answer as a mixed number.', parts: [{ id: 'a', kind: 'num', exp: 17 / 12, hint: 'write a mixed number like 1 1/2, or 3/2' }] },
    { id: 'q06', topic: 'fractions', stem: 'Work out &nbsp;2{1//2} ÷ {3//4}', parts: [{ id: 'a', kind: 'num', exp: 10 / 3, hint: 'e.g. 1 1/2 or 3/2' }] },
    { id: 'q07', topic: 'percent', stem: 'Increase £240 by 15%.', parts: [{ id: 'a', kind: 'num', exp: 276 }] },
    { id: 'q08', topic: 'percent', hard: true, stem: 'A coat costs £60 in a sale, after 20% was taken off. What was the <b>original</b> price?', parts: [{ id: 'a', kind: 'num', exp: 75 }] },
    { id: 'q09', topic: 'ratio', stem: 'Share £84 in the ratio 3 : 4.', parts: [
      { id: 'a', label: 'the smaller share (£)', kind: 'num', exp: 36 }, { id: 'b', label: 'the larger share (£)', kind: 'num', exp: 48 }] },
    { id: 'q10', topic: 'primes', stem: 'a) Write 72 as a product of prime factors, using powers. &nbsp; b) Find the HCF of 12 and 18. &nbsp; c) Find the LCM of 12 and 18.', parts: [
      { id: 'a', label: 'a) 72 =', kind: 'prime', exp: '2^3*3^2', hint: 'type powers like 2^3 x 3^2' },
      { id: 'b', label: 'b) HCF', kind: 'num', exp: 6 }, { id: 'c', label: 'c) LCM', kind: 'num', exp: 36 }] },
    { id: 'q11', topic: 'fdp', stem: 'a) Write 0.35 as a fraction in its simplest form. &nbsp; b) Write {3//8} as a percentage.', parts: [
      { id: 'a', label: 'a)', kind: 'num', exp: 7 / 20, simplest: true, hint: 'a fraction like 3/5' }, { id: 'b', label: 'b) %', kind: 'num', exp: 37.5, pct: true }] }
  ] },
  { id: 'b', title: 'Round B', sub: 'Algebra', mins: 15, qs: [
    { id: 'q12', topic: 'collect', stem: 'Simplify &nbsp;3a + 5b − a + 2b', parts: [{ id: 'a', kind: 'alg', variants: ['2a+7b'] }] },
    { id: 'q13', topic: 'expand1', stem: 'Expand and simplify &nbsp;3(2x − 1) − 2(x − 4)', parts: [{ id: 'a', kind: 'alg', variants: ['4x+5'] }] },
    { id: 'q14', topic: 'expand2', hard: true, stem: 'Expand and simplify &nbsp;(x + 5)(x − 3)', parts: [{ id: 'a', kind: 'alg', variants: ['x^2+2x-15'], hint: 'write powers like x^2 or x²' }] },
    { id: 'q15', topic: 'expand2', hard: true, stem: 'Expand and simplify &nbsp;(3y − 2)(y + 4)', parts: [{ id: 'a', kind: 'alg', variants: ['3y^2+10y-8'] }] },
    { id: 'q16', topic: 'equations', stem: 'Solve &nbsp;5x − 7 = 2x + 11', parts: [{ id: 'a', label: 'x =', kind: 'num', exp: 6 }] },
    { id: 'q17', topic: 'equations', stem: 'Solve &nbsp;3(x + 2) = 4x − 5', parts: [{ id: 'a', label: 'x =', kind: 'num', exp: 11 }] },
    { id: 'q18', topic: 'subject', stem: 'Make <b>g</b> the subject of &nbsp;f = 5 − 2g', parts: [{ id: 'a', label: 'g =', kind: 'alg', variants: ['(5-f)/2', '5/2-f/2', '(f-5)/-2', '-(f-5)/2', '(-f+5)/2'], hint: 'e.g. (3-f)/4' }] },
    { id: 'q19', topic: 'factorise', stem: 'Factorise fully &nbsp;6x^{2} − 9x', parts: [{ id: 'a', kind: 'alg', variants: ['3x(2x-3)', '(2x-3)3x', '(2x-3)(3x)', '3x(-3+2x)'], hint: 'e.g. 2x(x+1)' }] },
    { id: 'q20', topic: 'factorise', hard: true, stem: 'Factorise &nbsp;x^{2} + 7x + 12', parts: [{ id: 'a', kind: 'alg', variants: ['(x+3)(x+4)', '(x+4)(x+3)'] }] },
    { id: 'q21', topic: 'sequences', stem: 'Find the nth term of the sequence &nbsp;7, 11, 15, 19, …', parts: [{ id: 'a', label: 'nth term =', kind: 'alg', variants: ['4n+3', '3+4n'] }] },
    { id: 'q22', topic: 'sequences', stem: 'Is 100 a term of the sequence with nth term 4n − 3?', parts: [
      { id: 'a', kind: 'mc', options: ['Yes', 'No'], correct: 1 },
      { id: 'b', label: 'How do you know?', kind: 'text', area: true }] },
    { id: 'q23', topic: 'algfrac', hard: true, stem: 'Write as a single fraction &nbsp;{(2x − 1)//3} − {(x − 2)//4}', parts: [{ id: 'a', kind: 'alg', variants: ['(5x+2)/12', '(2+5x)/12'], hint: 'e.g. (3x+1)/6' }] }
  ] },
  { id: 'c', title: 'Round C', sub: 'Indices and standard form', mins: 10, qs: [
    { id: 'q24', topic: 'indices', stem: 'Simplify these.', parts: [
      { id: 'a', label: '5a^{3} × 4a^{6}', kind: 'alg', variants: ['20a^9'], hint: 'write powers like a^9 or a⁹' },
      { id: 'b', label: '(2x^{5})^{3}', kind: 'alg', variants: ['8x^15'] }] },
    { id: 'q25', topic: 'negfrac', hard: true, stem: 'Work these out.', parts: [
      { id: 'a', label: '5^{0}', kind: 'num', exp: 1 }, { id: 'b', label: '2^{−3}', kind: 'num', exp: 0.125, hint: 'a fraction like 1/4 or a decimal' }] },
    { id: 'q26', topic: 'negfrac', hard: true, stem: 'Work these out.', parts: [
      { id: 'a', label: '27^{2/3}', kind: 'num', exp: 9 }, { id: 'b', label: '({9//16})^{−1/2}', kind: 'num', exp: 4 / 3, hint: 'a fraction like 3/4' }] },
    { id: 'q27', topic: 'stdform', hard: true, stem: 'Give both answers in <b>standard form</b>.', parts: [
      { id: 'a', label: 'a) 0.00046', kind: 'sf', exp: 0.00046, hint: 'type like 3.2 x 10^5' },
      { id: 'b', label: 'b) (3 × 10^{5}) × (4 × 10^{−2})', kind: 'sf', exp: 12000 }] }
  ] },
  { id: 'd', title: 'Round D', sub: 'Shape and measures', mins: 10, qs: [
    { id: 'q28', topic: 'angles', stem: 'a) Work out the sum of the interior angles of a hexagon. &nbsp; b) A regular polygon has an exterior angle of 40°. How many sides does it have?', parts: [
      { id: 'a', label: 'a) degrees', kind: 'num', exp: 720 }, { id: 'b', label: 'b) sides', kind: 'num', exp: 9 }] },
    { id: 'q29', topic: 'circles', hard: true, stem: 'Leave your answers in terms of π (type pi).<br>a) A circle has radius 6 cm. Find its area.<br>b) A circle has diameter 10 cm. Find its circumference.', parts: [
      { id: 'a', label: 'a) area (cm²)', kind: 'alg', variants: ['36pi', 'pi36', '36*pi'], hint: 'e.g. 20pi' }, { id: 'b', label: 'b) circumference (cm)', kind: 'alg', variants: ['10pi', 'pi10', '10*pi'] }] },
    { id: 'q30', topic: 'pythag', stem: 'A right-angled triangle has shorter sides 8 cm and 15 cm. Find the length of the hypotenuse.', parts: [{ id: 'a', label: 'cm', kind: 'num', exp: 17 }] },
    { id: 'q31', topic: 'units', stem: 'Change 2.5 m^{2} into cm^{2}.', parts: [{ id: 'a', label: 'cm²', kind: 'num', exp: 25000 }] },
    { id: 'q32', topic: 'units', stem: 'A car travels 150 km in 2 hours 30 minutes. Find its average speed.', parts: [{ id: 'a', label: 'km/h', kind: 'num', exp: 60 }] }
  ] },
  { id: 'e', title: 'Round E', sub: 'Data, probability and money', mins: 10, qs: [
    { id: 'q33', topic: 'averages', stem: 'Find the mean, median and range of &nbsp;3, 8, 4, 10, 5', parts: [
      { id: 'a', label: 'mean', kind: 'num', exp: 6 }, { id: 'b', label: 'median', kind: 'num', exp: 5 }, { id: 'c', label: 'range', kind: 'num', exp: 7 }] },
    { id: 'q34', topic: 'prob', stem: 'A bag has 5 red, 3 blue and 2 green counters.<br>a) Find P(green).<br>b) A counter is taken out, put back, and a second is taken out. Find P(both red).', parts: [
      { id: 'a', label: 'a)', kind: 'num', exp: 0.2, hint: 'a fraction like 1/3 or a decimal' }, { id: 'b', label: 'b)', kind: 'num', exp: 0.25 }] },
    { id: 'q35', topic: 'money', calc: true, stem: '£500 is invested at 4% compound interest per year. Find the total after 2 years. <span class="calc">Calculator allowed.</span>', parts: [{ id: 'a', label: '£', kind: 'num', exp: 540.8 }] },
    { id: 'q36', topic: 'money', calc: true, stem: '£1 = €1.16. Change €87 into pounds. <span class="calc">Calculator allowed.</span>', parts: [{ id: 'a', label: '£', kind: 'num', exp: 75 }] },
    { id: 'q37', topic: 'money', stem: 'Which is the better buy: <b>3 litres for £2.40</b> or <b>5 litres for £3.75</b>?', parts: [{ id: 'a', kind: 'mc', options: ['3 litres for £2.40', '5 litres for £3.75'], correct: 1 }] }
  ] }
];

// The short first sitting: one representative question per core topic, picked to include the areas the exercise book flagged. Same question ids as the rounds, so nothing is asked twice.
var QUICK = { id: 'q', title: 'Quick start', sub: 'Her answers', mins: 15,
  ids: ['q01', 'q03', 'q05', 'q07', 'q09', 'q13', 'q15', 'q16', 'q18', 'q21', 'q27', 'q34'] };
QUICK.qs = QUICK.ids.map(function (id) { var f; ROUNDS.forEach(function (r) { r.qs.forEach(function (x) { if (x.id === id) f = x; }); }); return f; });

if (typeof module !== 'undefined') module.exports = { TOPICS: TOPICS, ROUNDS: ROUNDS, QUICK: QUICK };
