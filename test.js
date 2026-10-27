// Run: node platform/test.js. Every question's stated answer must mark right; listed typical wrong answers must not.
const M = require('./marker.js'), { ROUNDS } = require('./questions.js');
let fail = 0;
const t = (label, got, want) => { if (got !== want) { fail++; console.log('FAIL', label, 'got', got, 'want', want); } };
const part = (qid, pid) => ROUNDS.flatMap(r => r.qs).find(q => q.id === qid).parts.find(p => p.id === pid);
const ok = (qid, pid, answers) => answers.forEach(a => t(`${qid}${pid} "${a}"`, M.markPart(part(qid, pid), a), 'right'));
const no = (qid, pid, answers, want) => answers.forEach(a => t(`${qid}${pid} "${a}"`, M.markPart(part(qid, pid), a), want || 'wrong'));
ok('q01','a',['168','168 ']); ok('q01','b',['240']); no('q01','b',['230','24']);
ok('q02','a',['0.048']); no('q02','a',['0.0475','0.05'],'wrong');
ok('q03','a',['420']); no('q03','a',['400','91'])
ok('q04','a',['-12','−12','= -12']); no('q04','a',['12','-4'])
ok('q05','a',['17/12','1 5/12','1  5/12']); no('q05','a',['1 1/2','5/12']); no('q05','a',['1.4167'],'check');
ok('q06','a',['10/3','3 1/3']); no('q06','a',['3 1/4'])
ok('q07','a',['276','£276','£276.00']); no('q07','a',['36','255'])
ok('q08','a',['75','£75']); no('q08','a',['72','48'])
ok('q09','a',['36','£36']); ok('q09','b',['48'])
ok('q10','a',['2^3 x 3^2','2³×3²','3^2*2^3','2^3*3^2','2^3 3^2'.replace(' ','x')]); no('q10','a',['2^2 x 3^3','8 x 9'],'wrong'); ok('q10','b',['6']); ok('q10','c',['36']);
ok('q10','a',['2x2x2x3x3']);
ok('q11','a',['7/20']); no('q11','a',['35/100'],'check'); ok('q11','b',['37.5%','37.5','37.5 %']); no('q11','b',['0.375','3/8'])
ok('q12','a',['2a+7b','7b+2a','2a + 7b']); no('q12','a',['9ab','2a+3b'],'check');
ok('q13','a',['4x+5','5+4x']); ok('q14','a',['x^2+2x-15','x²+2x−15','-15+2x+x^2']); ok('q15','a',['3y^2+10y-8','3y²+10y−8']);
t('q15 wrong gives check', M.markPart(part('q15','a'), '3y^2+7y-20'), 'check');
ok('q16','a',['6','x=6','x = 6']); no('q16','a',['-6','5']); ok('q17','a',['11']);
ok('q18','a',['(5-f)/2','g=(5-f)/2','5/2 - f/2','(f-5)/-2']); no('q18','a',['(f+5)/-2'],'check');
ok('q19','a',['3x(2x-3)','3x(2x−3)','(2x-3)3x']); ok('q19','a',['3×(2×−3)']);   // the × key used as the letter x
t('q13 with × for x is read, not skipped or crashed', M.markPart(part('q13','a'), '−12×²+ 52× −24'), 'check');
t('q14 x² typed with the × key', M.markPart(part('q14','a'), '×²+2×−15'), 'right'); no('q19','a',['3(2x^2-3x)'],'check');
ok('q20','a',['(x+3)(x+4)','(x+4)(x+3)','(x + 3)(x + 4)']);
ok('q21','a',['4n+3','n=4n+3'.replace('n=','')]); no('q21','a',['4n-1'],'check');
t('q22 mc right', M.markPart(part('q22','a'), 1), 'right'); t('q22 mc wrong', M.markPart(part('q22','a'), 0), 'wrong');
t('q22 text', M.markPart(part('q22','b'), 'n is 25.75'), 'check');
ok('q23','a',['(5x+2)/12']); no('q23','a',['(5x-2)/12'],'check');
ok('q24','a',['20a^9','20a⁹','20 a^9']); ok('q24','b',['8x^15','8x¹⁵']); no('q24','b',['8x^8','6x^15'],'check');
ok('q25','a',['1']); ok('q25','b',['1/8','0.125']); no('q25','b',['-8','1/6'])
ok('q26','a',['9']); ok('q26','b',['4/3','1 1/3']); no('q26','b',['3/4'])
ok('q27','a',['4.6x10^-4','4.6 × 10^-4','4.6×10⁻⁴','4.6e-4','4.6 x 10^(-4)']); no('q27','a',['0.00046','46x10^-5'],'check'); no('q27','a',['4.6x10^4','4.6x10^-3'],'wrong');
ok('q27','b',['1.2x10^4','1.2 × 10⁴']); no('q27','b',['12x10^3','12000'],'check');
ok('q28','a',['720','720°']); ok('q28','b',['9','9 sides'])
ok('q29','a',['36pi','36π','pi36']); ok('q29','b',['10π']); no('q29','a',['113.1','36'],'check');
ok('q30','a',['17','17cm','17 cm']); ok('q31','a',['25000','25 000','25,000']); no('q31','a',['250','2500'])
ok('q32','a',['60','60km/h','60 km/h']);
ok('q33','a',['6']); ok('q33','b',['5']); ok('q33','c',['7']);
ok('q34','a',['1/5','0.2','20%']); ok('q34','b',['1/4','0.25','25%']); no('q34','b',['1/2','5/10','0.5'])
ok('q35','a',['540.80','£540.80','540.8']); no('q35','a',['540'],'check'); no('q35','a',['520','500'],'wrong');
ok('q36','a',['75']); t('q37', M.markPart(part('q37','a'), 1), 'right');
t('blank is skip', M.markPart(part('q01','a'), '  '), 'skip');
// every numeric/alg question has at least one expected value and no duplicated ids
const ids = new Set(); ROUNDS.forEach(r => r.qs.forEach(q => { if (ids.has(q.id)) { fail++; console.log('dup', q.id); } ids.add(q.id); q.parts.forEach(p => { if (p.kind==='num'&&typeof p.exp!=='number') {fail++;console.log('bad exp',q.id,p.id);} }); }));
console.log(fail ? fail + ' FAILED' : 'all marker tests passed', '-', ROUNDS.flatMap(r=>r.qs).length, 'questions,', ROUNDS.flatMap(r=>r.qs).reduce((n,q)=>n+q.parts.length,0), 'parts');
process.exit(fail ? 1 : 0);
