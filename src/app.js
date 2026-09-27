const PHASES = ['1–3주 · 기초', '4–8주 · 핵심 유형', '9–12주 · 추가 유형', '13–16주 · 실전'];
const PRIORITY = {samsung:[4,5,6,7,8], kakao:[3,9,10,11,12], pg:[3,9,10,12], hyundai:[4,5,7,9]};
const CO_NAME = {samsung:'삼성', kakao:'카카오', pg:'네이버·SK 등', hyundai:'현대차그룹'};
const STATUS = {solved:'혼자 풂', hint:'해설 보고 풂', fail:'못 풂'};
const SRC = {P:'프로그래머스', C:'코드트리 · 삼성 기출', H:'코드트리 · HSAT 기출'};
const INTERVALS = [1, 3, 7, 14];
const LVMIN = {LV1:15, LV2:30, LV3:50, LV4:70, LV5:90};
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const pad = n => String(n).padStart(2, '0');
const ymd = d => `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
const today = () => ymd(new Date());
const addDays = (s, n) => { const d = new Date(s + 'T00:00:00'); d.setDate(d.getDate() + n); return ymd(d); };
const daysBetween = (a, b) => Math.round((new Date(b+'T00:00:00') - new Date(a+'T00:00:00')) / 86400000);
const md = s => s ? `${Number(s.slice(5,7))}/${Number(s.slice(8,10))}` : '';
const fmtH = m => { m = Math.round(m); const h = Math.floor(m/60), r = m % 60; return h ? `${h}시간${r ? ` ${r}분` : ''}` : `${r}분`; };
const url = x => x.s === 'P' ? `https://school.programmers.co.kr/learn/courses/30/lessons/${x.id}` : `https://www.codetree.ai/ko/frequent-problems/${x.s === 'C' ? 'samsung-sw' : 'hsat'}/problems/${x.id}/description`;
const est = (x, sql) => x.s === 'C' ? 150 : x.s === 'H' ? 60 : sql ? (x.lv === 'LV3' ? 20 : 30) : (LVMIN[x.lv] || 40);

// ---------- index ----------
const PROBS = {}, SETS = {};
WEEKS.forEach(w => {
  const sets = [];
  const add = (title, items, kind, co, extra) => {
    const set = Object.assign({title, items, kind, co, id: `${w.n}-${sets.length}`}, extra || {});
    sets.push(set);
    items.forEach(x => { PROBS[x.s + x.id] = {x, w, set, min: est(x, title === 'SQL')}; });
  };
  if (w.must) add('필수', w.must, 'must', null);
  if (w.sql) add('SQL', w.sql, 'must', ['pg']);
  (w.groups || []).forEach(g => add(g[0].replace('보충 ', '보충 · ').replace(/^(보충 · )\((.*)\)$/, '$1$2'), g[1], g[3] === 'more' ? 'more' : 'must', g[2]));
  if (w.mock) add('모의고사 · 삼성 기출 2문제', w.mock.items, 'mock', w.mock.co, {min: w.mock.min});
  (w.mocks || []).forEach(m => add('모의고사 · ' + m.t, m.items, 'mock', m.co, {min: m.min}));
  if (w.more) add('도전 (선택)', w.more, 'more', null);
  SETS[w.n] = sets;
});

// ---------- state ----------
const blank = () => ({v:2, status:{}, notes:{}, review:{}, settings:{co:[], exam:'', hours:2}, log:{}, mocks:[], timer:null, plan:null});
function loadLocal(){
  try {
    const raw = localStorage.getItem('cote-state-v2');
    if (raw) { const s = Object.assign(blank(), JSON.parse(raw)); s.settings = Object.assign(blank().settings, s.settings); return s; }
    const old = JSON.parse(localStorage.getItem('cote-probs') || '{}'), s = blank();
    Object.keys(old).forEach(k => { if (old[k]) s.status[k] = 'solved'; });
    return s;
  } catch(e) { return blank(); }
}
let S = loadLocal();
let docRef = null, saveTimer = null, saving = false, pending = false, sampleFn = null;
function persist(){
  try { localStorage.setItem('cote-state-v2', JSON.stringify(S)); } catch(e) {}
  if (docRef) { clearTimeout(saveTimer); saveTimer = setTimeout(flush, 1200); }
}
async function flush(){
  if (!docRef) return;
  if (saving) { pending = true; return; }
  saving = true;
  try { await docRef.set(JSON.parse(JSON.stringify(S))); setSync('기록: Claude 계정'); }
  catch(e) {
    if (['invalid_argument','revoked','not_granted'].includes(e && e.code)) { docRef = null; setSync('기록: 이 브라우저'); }
    else setSync('기록: 저장 실패, 다시 시도 예정');
  }
  saving = false;
  if (pending) { pending = false; flush(); }
}
const setSync = t => { $('#syncState').textContent = t; };
function mergeState(remote, local){
  const r = Object.assign(blank(), remote); r.settings = Object.assign(blank().settings, r.settings);
  for (const f of ['status','notes','review']) for (const k in local[f]) if (!(k in r[f])) r[f][k] = local[f][k];
  for (const d in local.log) r.log[d] = Math.max(r.log[d] || 0, local.log[d]);
  return r;
}
const isDone = k => S.status[k] === 'solved' || S.status[k] === 'hint';
const coSel = () => S.settings.co || [];
const relevant = co => !co || !coSel().length || co.some(c => coSel().includes(c));
const coreKeys = n => SETS[n].filter(s => s.kind !== 'more' && relevant(s.co)).flatMap(s => s.items.map(x => x.s + x.id));

function setStatus(key, st){
  const prev = S.status[key];
  if (st) S.status[key] = st; else delete S.status[key];
  if (st && !prev) S.log[today()] = (S.log[today()] || 0) + 1;
  if ((st === 'hint' || st === 'fail') && !S.review[key]) S.review[key] = {step:0, due:addDays(today(), 1)};
  persist(); refreshRows(key); refresh();
}
function reviewDone(key, ok){
  const r = S.review[key]; if (!r) return;
  if (ok) { r.step++; if (r.step >= INTERVALS.length) { delete S.review[key]; S.status[key] = 'solved'; } else r.due = addDays(today(), INTERVALS[r.step]); }
  else { r.step = 0; r.due = addDays(today(), 1); }
  S.log[today()] = (S.log[today()] || 0) + 1;
  persist(); refresh(); renderDetail();
}

// ---------- problem row ----------
const openPanels = new Set();
function rowHtml(x, opt){
  opt = opt || {};
  const key = x.s + x.id, P = PROBS[key], st = S.status[key];
  const right = [
    st ? `<span class="st-${st}">${STATUS[st]}</span>` : '',
    S.notes[key] ? '<span class="memo-mark" title="메모 있음">메모</span>' : '',
    opt.week ? `<span>${pad(P.w.n)}주</span>` : '',
    `<span class="lv">${esc(x.lv)} · ${fmtH(P.min)}</span>`,
    `<button type="button" class="more" data-more="${esc(key)}" aria-expanded="${openPanels.has(key)}">기록</button>`
  ].join('');
  return `<li class="row${isDone(key) ? ' is-done' : ''}" data-key="${esc(key)}" data-opt="${opt.week ? 'w' : ''}">
    <input type="checkbox" ${isDone(key) ? 'checked' : ''} aria-label="${esc(x.t)} 풀었음">
    <span class="name"><a href="${url(x)}" target="_blank" rel="noopener">${esc(x.t)}</a><span class="src">${SRC[x.s]}</span>${x.sol ? `<a class="sol" href="${x.sol}" target="_blank" rel="noopener" title="카카오 공식 해설">해설</a>` : ''}</span>
    <span class="right">${right}</span>
    ${opt.extra || ''}${openPanels.has(key) ? panelHtml(key) : ''}</li>`;
}
function panelHtml(key){
  const st = S.status[key] || '', r = S.review[key];
  const seg = [['','안 풂'],['solved','혼자 풂'],['hint','해설 보고 풂'],['fail','못 풂']].map(([v,l]) =>
    `<label><input type="radio" name="st-${esc(key)}" value="${v}" ${st === v ? 'checked' : ''}>${l}</label>`).join('');
  return `<div class="panel">
    <div class="seg" role="radiogroup" aria-label="풀이 상태">${seg}</div>
    ${r ? `<p class="small ink2">다음 복습 ${md(r.due)} (${r.step + 1}/${INTERVALS.length}회차)</p>` : '<p class="small muted">"해설 보고 풂"이나 "못 풂"을 고르면 복습 일정이 잡힙니다.</p>'}
    <label class="fld"><span>메모</span><textarea rows="2" data-note="${esc(key)}" placeholder="막힌 이유나 핵심 아이디어">${esc(S.notes[key] || '')}</textarea></label>
    ${sampleFn ? `<div class="fld"><span>막혔을 때 Claude에게 힌트 받기 (정답 코드는 주지 않습니다)</span>
      <textarea rows="3" data-ctx="${esc(key)}" placeholder="지문 요약이나 작성 중인 코드를 붙여 넣으면 더 정확합니다 (선택)"></textarea>
      <div class="ai-btns"><button type="button" class="btn line sm" data-hint="1" data-key="${esc(key)}">방향</button><button type="button" class="btn line sm" data-hint="2" data-key="${esc(key)}">쓸 알고리즘</button><button type="button" class="btn line sm" data-hint="3" data-key="${esc(key)}">핵심 아이디어</button><button type="button" class="btn line sm" data-hint="review" data-key="${esc(key)}">내 코드 검토</button><button type="button" class="lnk" data-stop="${esc(key)}" hidden>중지</button></div>
      <div class="ai-out" data-out="${esc(key)}" hidden></div></div>` : ''}
  </div>`;
}
function refreshRows(key){
  document.querySelectorAll(`li.row[data-key="${CSS.escape(key)}"]`).forEach(li => {
    const extra = li.querySelector('.rv')?.outerHTML || '';
    const t = document.createElement('ul');
    t.innerHTML = rowHtml(PROBS[key].x, {week: li.dataset.opt === 'w', extra});
    li.replaceWith(t.firstElementChild);
  });
}

// ---------- router ----------
let curWeek = null, curView = 'today';
const VIEW_NAME = {today:'오늘', plan:'커리큘럼', guide:'가이드', companies:'기업별 정보', resources:'자료'};
function renderCrumb(){
  const parts = ['코딩테스트 로드맵', VIEW_NAME[curView]];
  if (curView === 'plan' && curWeek && !filterOn()) { const w = WEEKS.find(w => w.n === curWeek); parts.push(`${pad(w.n)}주 · ${w.t}`); }
  $('#crumb').innerHTML = parts.map((p, i) => i === parts.length - 1 ? `<b>${esc(p)}</b>` : `<span>${esc(p)}</span>`).join('<span class="sep">›</span>');
}
function firstOpenWeek(){ const w = WEEKS.find(w => coreKeys(w.n).some(k => !isDone(k))); return w ? w.n : 16; }
function route(){
  const h = location.hash.replace('#', '') || 'today';
  let view = h, m = h.match(/^w(\d+)$/);
  if (m) { view = 'plan'; curWeek = Math.min(16, Math.max(1, Number(m[1]))); }
  if (!['today','plan','guide','companies','resources'].includes(view)) view = 'today';
  document.querySelectorAll('.view').forEach(v => v.hidden = v.id !== 'v-' + view);
  document.querySelectorAll('.act a').forEach(a => a.setAttribute('aria-current', a.dataset.view === view ? 'page' : 'false'));
  curView = view;
  if (view === 'plan') { if (!curWeek) curWeek = firstOpenWeek(); renderSide(); renderDetail(); }
  renderCrumb();
  window.scrollTo(0, 0);
}
window.addEventListener('hashchange', route);

// ---------- today ----------
function renderGrass(){
  const end = new Date(today() + 'T00:00:00'), start = new Date(end); start.setDate(end.getDate() - end.getDay() - 7 * 15);
  let cells = '', total = 0, days = 0;
  for (let d = new Date(start); d <= end || d.getDay() !== 0; d.setDate(d.getDate() + 1)) {
    const k = ymd(d), n = S.log[k] || 0, fut = d > end;
    if (!fut) { total += n; if (n) days++; }
    const lv = fut ? 'fut' : n >= 5 ? 'l3' : n >= 3 ? 'l2' : n >= 1 ? 'l1' : '';
    cells += `<i class="${lv}" title="${fut ? '' : `${md(k)} ${n}문제`}"></i>`;
    if (d > end && d.getDay() === 6) break;
  }
  $('#grass').innerHTML = cells;
  $('#grass').setAttribute('aria-label', `최근 16주 동안 ${days}일, ${total}문제`);
  $('#actMeta').textContent = `최근 16주 · ${days}일 공부 · ${total}문제`;
}
function streak(){ let n = 0, d = today(); if (!S.log[d]) d = addDays(d, -1); while (S.log[d]) { n++; d = addDays(d, -1); } return n; }
function renderToday(){
  document.querySelectorAll('#coChips input').forEach(i => i.checked = coSel().includes(i.value));
  $('#examDate').value = S.settings.exam || '';
  $('#hoursDay').value = S.settings.hours || 2;
  const all = WEEKS.flatMap(w => coreKeys(w.n)), remaining = all.filter(k => !isDone(k));
  const done = all.length - remaining.length, remMin = remaining.reduce((a, k) => a + PROBS[k].min, 0);
  const hours = Number(S.settings.hours) || 2, needDays = Math.ceil(remMin / (hours * 60));
  let left = null, dLabel = '—', dSub = '날짜를 정하세요';
  if (S.settings.exam) { left = daysBetween(today(), S.settings.exam); dLabel = left > 0 ? `D-${left}` : left === 0 ? 'D-day' : '지남'; dSub = S.settings.exam.replaceAll('-', '.'); }
  $('#stats').innerHTML = [
    ['진행', `${done}<span class="small muted"> / ${all.length}</span>`, all.length ? `${Math.round(done / all.length * 100)}%` : ''],
    ['시험까지', dLabel, dSub],
    ['남은 공부', fmtH(remMin), `하루 ${hours}시간이면 ${needDays}일`],
    ['연속 공부', `${streak()}일`, `오늘 ${S.log[today()] || 0}문제`],
  ].map(([k, v, s]) => `<div class="stat"><span class="k">${k}</span><span class="v">${v}</span><span class="s">${s}</span></div>`).join('');
  let pace = '';
  if (left !== null && left > 0) pace = needDays <= left ? `지금 계획대로면 시험 ${left - needDays}일 전에 모두 끝납니다.` : `이대로면 ${needDays - left}일이 모자랍니다. 하루 ${Math.ceil(remMin / 60 / left * 2) / 2}시간으로 늘리거나, 지원 회사 우선 주차부터 공부하세요.`;
  else if (left !== null) pace = '시험 날짜가 지났습니다. 다음 목표 날짜를 넣어 주세요.';
  if (coSel().length) pace += ` ${coSel().map(c => CO_NAME[c]).join(', ')} 기준으로 관련 없는 기출은 빼고 계산했습니다.`;
  $('#pace').textContent = pace.trim(); $('#pace').hidden = !pace.trim();
  renderGrass();
  const n = firstOpenWeek(), w = WEEKS.find(w => w.n === n), ks = coreKeys(n), d = ks.filter(isDone).length;
  $('#curWeek').innerHTML = `<div><div class="small muted">지금 공부할 주차</div><div class="t">${pad(n)}주 · ${esc(w.t)}</div><div class="small ink2">${d} / ${ks.length}문제 · 통과 기준: ${esc(w.goal)}</div></div><a class="btn" href="#w${n}" style="text-decoration:none">이어서 공부하기</a>`;
  if (!S.plan || S.plan.date !== today()) S.plan = {date: today(), keys: pickNext([], hours * 60)};
  const picks = S.plan.keys.filter(k => PROBS[k]), used = picks.reduce((a, k) => a + PROBS[k].min, 0);
  const allDone = picks.length && picks.every(isDone);
  $('#todayMeta').innerHTML = picks.length ? `약 ${fmtH(used)}${allDone ? ' · <button type="button" class="lnk" id="moreToday">더 풀기</button>' : ''}` : '';
  $('#todayList').innerHTML = picks.length ? picks.map(k => rowHtml(PROBS[k].x, {week:true})).join('') : '<li class="empty">남은 필수 문제가 없습니다. 모의고사와 도전 문제를 풀어 보세요.</li>';
  const due = Object.keys(S.review).filter(k => S.review[k].due <= today() && PROBS[k]);
  const later = Object.keys(S.review).length - due.length;
  $('#reviewList').innerHTML = due.length ? due.map(k => rowHtml(PROBS[k].x, {week:true, extra:`<span class="rv ai-btns" style="grid-column:2/-1"><button type="button" class="btn sm" data-rv="ok" data-key="${esc(k)}">혼자 풀었음</button><button type="button" class="btn line sm" data-rv="no" data-key="${esc(k)}">또 막힘</button></span>`})).join('')
    : `<li class="empty">오늘 복습할 문제가 없습니다.${later ? ` 예정된 복습 ${later}개.` : ''}</li>`;
}

function pickNext(exclude, budget){
  const out = []; let used = 0;
  for (const k of WEEKS.flatMap(w => coreKeys(w.n))) {
    if (isDone(k) || exclude.includes(k) || S.review[k] || PROBS[k].set.kind !== 'must') continue;
    if (out.length && used + PROBS[k].min > budget) break;
    out.push(k); used += PROBS[k].min; if (out.length >= 8) break;
  }
  return out;
}

// ---------- lectures ----------
function lecTag(u){
  if (u.includes('blog.encrypted.gg')) return '바킹독 · 글과 영상 · C++';
  if (u.includes('PLRx0vPvlEmd')) return '나동빈 · 영상 · Python';
  if (u.includes('youtu')) return '유튜브 영상';
  if (u.includes('tech.kakao.com')) return '카카오 공식 해설';
  if (u.includes('sql_practice_kit')) return '프로그래머스 문제 모음';
  if (u.includes('frequent-problems')) return '코드트리 기출 목록';
  if (u.includes('hyundai-ngv')) return '현대차그룹 HSAT';
  return '접수 페이지';
}
const PY_REPO = 'https://github.com/hanXen/basic-algo-lecture-python';
function lectureHtml(w){
  const study = w.n <= 12;
  const links = w.lec.map(l => `<a href="${l.u}" target="_blank" rel="noopener">${esc(l.t)}</a> <span class="small muted">${lecTag(l.u)}</span>`).join('<br>');
  const baek = w.lec.filter(l => l.u.includes('blog.encrypted.gg'));
  const hasPy = baek.some(l => { const m = l.t.match(/0x([0-9A-F]{2})/i); return m && parseInt(m[1], 16) <= 0x11; });
  let note = '';
  if (study) {
    note = '먼저 보고 아래 문제를 푸세요.';
    if (baek.length) {
      note += ' 바킹독 강의의 예제 코드는 C++입니다.';
      if (hasPy) note += ` Python으로 보려면 같은 예제를 Python으로 푼 <a href="${PY_REPO}" target="_blank" rel="noopener">풀이 모음</a>을 참고하세요.`;
      note += ' 강의 끝의 연습 문제는 백준 문제라 지금은 채점이 안 되니 건너뜁니다.';
    }
    note = `<p class="small muted" style="margin-top:4px">${note}</p>`;
  }
  return `<dt>${study ? '개념 강의' : '참고 링크'}</dt><dd>${links}${note}</dd>`;
}

// ---------- curriculum ----------
function renderSide(){
  let html = '', last = -1;
  WEEKS.forEach(w => {
    if (w.ph !== last) { if (last >= 0) html += '</div>'; html += `<div><div class="grp eyebrow">${PHASES[w.ph]}</div>`; last = w.ph; }
    const ks = coreKeys(w.n), d = ks.filter(isDone).length, pri = coSel().some(c => PRIORITY[c].includes(w.n));
    html += `<button type="button" class="wk${ks.length && d === ks.length ? ' complete' : ''}" data-week="${w.n}" aria-current="${w.n === curWeek}"><span class="n">${pad(w.n)}</span><span>${esc(w.t)}${pri ? '<span class="pri" title="지원 회사 우선 주차"></span>' : ''}</span><span class="c">${d}/${ks.length}</span></button>`;
  });
  $('#side').innerHTML = html + '</div>';
  $('#wkSelect').innerHTML = WEEKS.map(w => `<option value="${w.n}" ${w.n === curWeek ? 'selected' : ''}>${pad(w.n)}주 · ${esc(w.t)} (${coreKeys(w.n).filter(isDone).length}/${coreKeys(w.n).length})</option>`).join('');
}
const unfolded = new Set();
function filterOn(){ return !!(($('#fText').value || '').trim() || $('#fStatus').value); }
function matchKey(k){
  const q = ($('#fText').value || '').trim().toLowerCase(), st = $('#fStatus').value, P = PROBS[k];
  if (q && ![P.x.t, P.w.t, P.set.title, SRC[P.x.s]].some(s => s.toLowerCase().includes(q))) return false;
  if (st === 'todo' && isDone(k)) return false;
  if (st === 'done' && !isDone(k)) return false;
  if (st === 'review' && !S.review[k]) return false;
  if (st === 'memo' && !S.notes[k]) return false;
  return true;
}
function renderDetail(){
  if (!curWeek) curWeek = firstOpenWeek();
  $('#fClear').hidden = !filterOn();
  if (filterOn()) {
    const hits = Object.keys(PROBS).filter(matchKey);
    let html = `<p class="small muted">${hits.length}개 문제</p>`;
    WEEKS.forEach(w => {
      const ks = hits.filter(k => PROBS[k].w.n === w.n); if (!ks.length) return;
      html += `<div class="set"><div class="set-h"><a class="t" href="#w${w.n}">${pad(w.n)}주 · ${esc(w.t)}</a></div><ul class="list">${ks.map(k => rowHtml(PROBS[k].x)).join('')}</ul></div>`;
    });
    $('#detail').innerHTML = `<div class="pane" style="padding:0">${html}</div>`;
    renderCrumb(); return;
  }
  const w = WEEKS.find(w => w.n === curWeek), ks = coreKeys(w.n), d = ks.filter(isDone).length;
  const mins = ks.reduce((a, k) => a + PROBS[k].min, 0);
  const pri = coSel().filter(c => PRIORITY[c].includes(w.n));
  let html = `<div class="dhead"><span class="eyebrow">${PHASES[w.ph]}</span><h1>${pad(w.n)}주 · ${esc(w.t)}</h1>
    <div class="dmeta"><span>${d} / ${ks.length}문제 완료</span><span>약 ${fmtH(mins)}</span>${pri.length ? `<span style="color:var(--accent)">${pri.map(c => CO_NAME[c]).join('·')} 우선</span>` : ''}</div>
    <div class="bar"><i style="width:${ks.length ? d / ks.length * 100 : 0}%"></i></div></div>
    <dl class="info">
      ${w.lec.length ? lectureHtml(w) : ''}
      <dt>배울 것</dt><dd>${esc(w.learn)}</dd>
      ${w.pit && w.pit.length ? `<dt>자주 하는 실수</dt><dd><ul>${w.pit.map(p => `<li>${esc(p)}</li>`).join('')}</ul></dd>` : ''}
      <dt>통과 기준</dt><dd>${esc(w.goal)}</dd>
    </dl>`;
  SETS[w.n].forEach(set => {
    const rel = relevant(set.co) || unfolded.has(set.id);
    const setMin = set.items.reduce((a, x) => a + PROBS[x.s + x.id].min, 0);
    let m = `${set.items.length}문제 · 약 ${fmtH(setMin)}`;
    if (set.co) m += ` · ${set.co.map(c => CO_NAME[c]).join(', ')}`;
    let tools = '';
    if (set.kind === 'mock' && rel) {
      const hist = S.mocks.filter(x => x.set === set.title).slice(-3).map(x => `${md(x.date)} ${x.solved}/${x.total}문제 ${fmtH(x.minutes)}`).join(' · ');
      m = `${set.items.length}문제 · 제한 ${fmtH(set.min)}`;
      tools = `<div class="ai-btns"><button type="button" class="btn sm" data-mock="${set.id}">타이머 시작</button>${hist ? `<span class="small muted">지난 기록 ${esc(hist)}</span>` : ''}</div>`;
    }
    html += `<div class="set${rel ? '' : ' off'}"><div class="set-h"><span class="t">${esc(set.title)}</span><span class="m">${m}</span></div>
      ${rel ? tools + `<ul class="list">${set.items.map(x => rowHtml(x)).join('')}</ul>` : `<button type="button" class="lnk" data-unfold="${set.id}">지원 회사와 관련 없어 접어 두었습니다 · 펼치기</button>`}</div>`;
  });
  const prev = w.n > 1 ? `<a href="#w${w.n - 1}">← ${pad(w.n - 1)}주</a>` : '<span></span>';
  const next = w.n < 16 ? `<a href="#w${w.n + 1}">${pad(w.n + 1)}주 →</a>` : '<span></span>';
  html += `<div class="pager">${prev}${next}</div>`;
  $('#detail').innerHTML = `<div class="pane" style="padding:0">${html}</div>`;
  renderCrumb();
}

// ---------- code highlight ----------
const FLOW = /<span class="hljs-keyword">(if|elif|else|for|while|return|import|from|continue|break|in|try|except|catch|throw|raise|with|yield|pass|not|and|or|is|switch|case|do)<\/span>/g;
function hl(line, language){
  if (!line) return ' ';
  try { if (window.hljs) return window.hljs.highlight(line, {language: language || lang, ignoreIllegals:true}).value.replace(FLOW, '<span class="hljs-keyword flow">$1</span>'); } catch(e) {}
  return esc(line);
}

// ---------- code files (Python / Java) ----------
let lang = 'python';
try { lang = localStorage.getItem('cote-lang') === 'java' ? 'java' : 'python'; } catch(e) {}
const FILES = {python:['grid_bfs.py', 'combination.py', 'rotate.py', 'param_search.py', 'dijkstra.py', 'union_find.py', 'prefix_sum.py', 'starter.py'],
  java:['GridBfs.java', 'Combination.java', 'Rotate.java', 'ParamSearch.java', 'Dijkstra.java', 'UnionFind.java', 'PrefixSum.java', 'Main.java']};
const IO_FILES = {python:['solution.py', 'swea.py', 'stdin.py'], java:['Solution.java', 'Solution.java', 'Main.java']};
const codeOf = o => lang === 'java' && o.java ? o.java : o.code;
const lines = (code) => code.split('\n').map(l => `<span class="l">${hl(l)}</span>`).join('');
function renderCode(){
  document.querySelectorAll('.langsw input').forEach(i => i.checked = i.value === lang);
  $('#tpls').innerHTML = INFO.templates_python.map((t, i) => `<div class="file"><div class="file-tab"><span class="fn">${FILES[lang][i]}</span><span class="desc">${esc(t.name.replace(/^\d+\.\s*/, ''))}</span><button type="button" class="copy" data-copy="${i}">복사</button></div><pre class="code"><code>${lines(codeOf(t))}</code></pre></div>`).join('');
  $('#ioFiles').innerHTML = INFO.io_formats.map((f, i) => `<div class="file"><div class="file-tab"><span class="fn">${IO_FILES[lang][i]}</span><span class="desc">${esc(f.site)}</span><button type="button" class="copy" data-io="${i}">복사</button></div><p class="note">${esc(f.how)}${lang === 'java' && f.how_java ? ' ' + esc(f.how_java) : ''}</p><pre class="code"><code>${lines(codeOf(f))}</code></pre></div>`).join('');
}

// ---------- theme ----------
const THEMES = ['system', 'light', 'dark'], THEME_NAME = {system:'테마: 시스템', light:'테마: 라이트', dark:'테마: 다크'};
let theme = 'system';
try { theme = localStorage.getItem('cote-theme') || 'system'; } catch(e) {}
function renderTheme(){
  if (theme === 'system') document.documentElement.removeAttribute('data-theme'); else document.documentElement.setAttribute('data-theme', theme);
  $('#themeBtn').textContent = THEME_NAME[theme];
}

// ---------- companies & resources (static) ----------
function renderStatic(){
  $('#coTable').innerHTML = '<thead><tr><th>기업</th><th>시험 환경</th><th>구성</th><th>출제 경향</th><th>참고</th><th>근거 시점</th></tr></thead><tbody>' +
    INFO.company_formats.map(c => {
      const m = c.company.match(/^(.*?)\s*\((.*)\)$/), name = m ? m[1] : c.company, sub = m ? m[2] : '';
      const conf = c.confidence === '여러 출처 일치' ? '' : ` <span class="muted">(${esc(c.confidence)})</span>`;
      return `<tr><td>${esc(name)}${sub ? `<span class="sub">${esc(sub)}</span>` : ''}</td><td>${esc(c.platform)}</td><td>${esc(c.format)}</td><td class="ink2">${esc(c.content)}</td><td class="ink2">${esc(c.notes)}${conf}</td><td class="small muted" style="white-space:nowrap">${esc(c.basis || '—')}</td></tr>`;
    }).join('') + '</tbody>';
  const dot = v => ({'매우 자주':'●●●','자주':'●●','가끔':'●','드묾':'','없음':''}[v] ?? null);
  const cols = INFO.frequency_columns;
  $('#typeTable').innerHTML = `<thead><tr>${cols.map(c => `<th>${esc(c.replace(' (SK·한화·LG 등)', ''))}</th>`).join('')}</tr></thead><tbody>` +
    INFO.type_frequency.map(r => `<tr><td>${esc(r[0])}</td>${r.slice(1).map(v => { const d = dot(v); return `<td class="${d !== null ? 'dots' : 'small ink2'}">${d !== null ? d : esc(v)}</td>`; }).join('')}</tr>`).join('') + '</tbody>';
  $('#toolTable').innerHTML = '<thead><tr><th>이름</th><th>쓰는 곳</th></tr></thead><tbody>' + INFO.tools.map(t => `<tr><td><a href="${t.url}" target="_blank" rel="noopener">${esc(t.name)}</a></td><td class="ink2">${esc(t.use)}</td></tr>`).join('') + '</tbody>';
  renderCode();
  $('#sigTable').innerHTML = '<thead><tr><th>지문의 단서</th><th>떠올릴 방법</th><th>배우는 주차</th></tr></thead><tbody>' + INFO.signals.map(([s, m, n]) => `<tr><td>${esc(s)}</td><td>${esc(m)}</td><td><a href="#w${n}">${pad(n)}주</a></td></tr>`).join('') + '</tbody>';
  $('#cheatTable').innerHTML = '<thead><tr><th>상황</th><th>코드</th><th>설명</th></tr></thead><tbody>' + INFO.cheats.map(([a, c, n]) => `<tr><td>${esc(a)}</td><td><code>${hl(c, 'python')}</code></td><td class="small">${esc(n)}</td></tr>`).join('') + '</tbody>';
  $('#mythList').innerHTML = INFO.myths.map(x => `<li>${esc(x)}</li>`).join('');
  $('#srcList').innerHTML = INFO.sources.map(s => `<li><a href="${s.url}" target="_blank" rel="noopener">${esc(s.title)}</a></li>`).join('');
}

// ---------- refresh ----------
function refresh(){
  const all = WEEKS.flatMap(w => coreKeys(w.n)), done = all.filter(isDone).length;
  $('#stProg').textContent = `✓ ${done} / ${all.length}문제`;
  const left = S.settings.exam ? daysBetween(today(), S.settings.exam) : null;
  $('#stDday').textContent = left === null ? '시험일 미정' : left > 0 ? `D-${left}` : left === 0 ? 'D-day' : '시험일 지남';
  const due = Object.keys(S.review).filter(k => S.review[k].due <= today()).length;
  $('#stReview').textContent = `복습 ${due}`; $('#stReview').hidden = !due;
  renderTheme();
  renderToday();
  if (!$('#v-plan').hidden) renderSide();
}

// ---------- AI (claude.ai only) ----------
const aiCtl = {};
const aiErr = c => ({not_granted:'Claude 사용이 허용되지 않았습니다.', rate_limited:'사용량 한도에 걸렸습니다. 잠시 뒤에 다시 해 보세요.', session_expired:'다시 로그인해 주세요.', refused:'답할 수 없는 요청입니다. 내용을 바꿔 보세요.', prompt_too_large:'붙여 넣은 내용이 너무 깁니다.'})[c] || '답을 받지 못했습니다. 다시 시도해 주세요.';
function aiOff(e){ if (['not_granted','sampling_disabled','not_declared','capability_disabled','capability_removed'].includes(e && e.code)) { sampleFn = null; $('#coachBox').hidden = true; } }
async function askHint(key, level){
  if (!sampleFn) return;
  const P = PROBS[key], sel = s => document.querySelector(`[${s}="${CSS.escape(key)}"]`);
  const ctx = (sel('data-ctx')?.value || '').slice(0, 12000), out = sel('data-out'), stop = sel('data-stop');
  const ask = {1:'문제를 어떤 관점으로 봐야 하는지만 알려 줘. 알고리즘 이름은 말하지 마.', 2:'어떤 알고리즘과 자료구조를 왜 써야 하는지, 입력 크기로 본 시간복잡도까지만 알려 줘.', 3:'핵심 아이디어와 놓치기 쉬운 예외를 알려 줘. 코드는 쓰지 마.', review:'학생 코드의 버그, 시간 초과 위험, 놓친 예외를 짚고 고칠 방향만 말해. 고친 전체 코드는 쓰지 마.'}[level];
  if (level === 'review' && !ctx.trim()) { out.hidden = false; out.textContent = '검토할 코드를 위 칸에 붙여 넣어 주세요.'; return; }
  const prompt = `너는 한국 대기업 코딩테스트를 준비하는 학생의 코치야. 한국어로 5문장 이내로 답해. 정답 코드나 전체 풀이는 쓰지 마.\n문제: ${SRC[P.x.s]} "${P.x.t}" (${P.x.lv}), ${P.w.n}주차 주제: ${P.w.t}\n이 문제를 정확히 모르면 추측하지 말고 그렇다고 말한 뒤 일반적인 접근만 말해.\n요청: ${ask}\n${ctx.trim() ? '학생이 붙여 넣은 내용:\n' + ctx : ''}`;
  aiCtl[key]?.abort(); const ctl = aiCtl[key] = new AbortController();
  out.hidden = false; out.textContent = '생각하는 중…'; stop.hidden = false;
  try { await sampleFn(prompt, {signal: ctl.signal, onText: ({text}) => { out.textContent = text; }}); }
  catch(e) { out.textContent = (e && e.text) || ''; if (e?.code !== 'cancelled') out.textContent += (out.textContent ? '\n\n' : '') + aiErr(e?.code); aiOff(e); }
  finally { stop.hidden = true; }
}
let coachCtl = null;
async function askCoach(){
  if (!sampleFn) return;
  const out = $('#coachOut');
  const weeks = WEEKS.map(w => { const ks = coreKeys(w.n); return `${w.n}주 ${w.t}: ${ks.filter(isDone).length}/${ks.length}`; }).join('\n');
  const stuck = Object.keys(PROBS).filter(k => S.status[k] === 'hint' || S.status[k] === 'fail').slice(0, 25).map(k => `- ${PROBS[k].x.t} (${PROBS[k].w.n}주, ${STATUS[S.status[k]]})${S.notes[k] ? ': ' + S.notes[k].slice(0, 100) : ''}`).join('\n');
  const prompt = `너는 한국 대기업 코딩테스트 코치야. 아래 기록을 보고 이번 주 공부 조언을 한국어로 해 줘. 형식: 현재 상태 한 줄, 이번 주 할 일 3가지(주차와 유형을 구체적으로), 조심할 점 한 줄. 10줄 이내. 새 사이트나 강의는 추천하지 마.\n지원 회사: ${coSel().map(c => CO_NAME[c]).join(', ') || '미정'}\n오늘: ${today()}, 시험일: ${S.settings.exam || '미정'}, 하루 ${S.settings.hours}시간\n주차별 진행:\n${weeks}\n막힌 문제:\n${stuck || '없음'}\n모의고사: ${S.mocks.slice(-5).map(m => `${m.set} ${m.solved}/${m.total}`).join('; ') || '없음'}`;
  coachCtl?.abort(); coachCtl = new AbortController();
  out.hidden = false; out.textContent = '생각하는 중…'; $('#coachBtn').disabled = true; $('#coachStop').hidden = false;
  try { await sampleFn(prompt, {signal: coachCtl.signal, cache: false, onText: ({text}) => { out.textContent = text; }}); }
  catch(e) { out.textContent = (e && e.text) || ''; if (e?.code !== 'cancelled') out.textContent += (out.textContent ? '\n\n' : '') + aiErr(e?.code); aiOff(e); }
  finally { $('#coachBtn').disabled = false; $('#coachStop').hidden = true; }
}

// ---------- mock timer ----------
let tick = null;
const findSet = id => { const [n, i] = id.split('-').map(Number); return SETS[n][i]; };
const elapsed = () => { const t = S.timer; return t ? (t.paused || Date.now()) - t.start - t.pausedTotal : 0; };
function showTimer(){
  if (!S.timer) { $('#stTimer').hidden = true; $('#tmPanel').hidden = true; clearInterval(tick); return; }
  $('#stTimer').hidden = false; $('#tmSet').textContent = S.timer.set;
  $('#tmPause').textContent = S.timer.paused ? '다시 시작' : '일시정지';
  const draw = () => {
    const left = S.timer.min * 60000 - elapsed(), a = Math.abs(left);
    const clock = `${left < 0 ? '+' : ''}${Math.floor(a / 3600000)}:${pad(Math.floor(a % 3600000 / 60000))}:${pad(Math.floor(a % 60000 / 1000))}`;
    $('#tmClock').textContent = clock; $('#tmClock').classList.toggle('over', left < 0);
    $('#stTimer').innerHTML = `모의고사 <span class="clock${left < 0 ? ' over' : ''}">${clock}</span>${S.timer.paused ? ' (정지)' : ''}`;
    $('#tmState').textContent = left < 0 ? '시간 초과' : S.timer.paused ? '일시정지 중' : '';
  };
  draw(); clearInterval(tick); tick = setInterval(draw, 1000);
}
function toast(t){ const el = $('#toast'); el.textContent = t; el.hidden = false; clearTimeout(toast.t); toast.t = setTimeout(() => el.hidden = true, 3000); }
let endArmed = false;
function endMock(save){
  const t = S.timer; if (!t) return;
  if (save) {
    const ks = findSet(t.id).items.map(x => x.s + x.id);
    S.mocks.push({set: t.set, date: today(), minutes: Math.round(elapsed() / 60000), solved: ks.filter(isDone).length, total: ks.length});
    S.mocks = S.mocks.slice(-100);
    toast(`기록했습니다: ${ks.filter(isDone).length}/${ks.length}문제, ${fmtH(elapsed() / 60000)}`);
  }
  S.timer = null; persist(); showTimer(); renderDetail();
}

// ---------- export / import ----------
function exportState(){
  const data = JSON.stringify(Object.assign({app:'coding-test-roadmap', exported:new Date().toISOString()}, S), null, 1);
  if (window.claude) {
    navigator.clipboard?.writeText(data).then(() => { $('#ioMsg').textContent = '기록을 클립보드에 복사했습니다. 메모장에 붙여 넣어 .json 파일로 저장하세요.'; }, () => { $('#ioMsg').textContent = '복사하지 못했습니다.'; });
    return;
  }
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([data], {type:'application/json'}));
  a.download = `coding-test-progress-${today()}.json`; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  $('#ioMsg').textContent = '기록 파일을 내려받았습니다.';
}
async function importFile(input){
  const f = input.files && input.files[0]; if (!f) return;
  try {
    const obj = JSON.parse(await f.text()); if (!obj || typeof obj.status !== 'object') throw 0;
    S = mergeState(obj, S); persist(); refresh(); renderDetail(); showTimer();
    $('#ioMsg').textContent = `기록을 가져왔습니다. 푼 문제 ${Object.values(S.status).filter(s => s !== 'fail').length}개.`;
  } catch(e) { $('#ioMsg').textContent = '이 파일은 읽을 수 없습니다. 이 페이지에서 내보낸 파일인지 확인하세요.'; }
  input.value = '';
}

// ---------- events ----------
document.addEventListener('change', e => {
  const t = e.target;
  if (t.matches('li.row > input[type=checkbox]')) { const k = t.closest('li.row').dataset.key; setStatus(k, t.checked ? (S.status[k] === 'hint' ? 'hint' : 'solved') : null); }
  else if (t.matches('.panel input[type=radio]')) setStatus(t.closest('li.row').dataset.key, t.value || null);
  else if (t.matches('#coChips input')) { S.settings.co = [...document.querySelectorAll('#coChips input:checked')].map(i => i.value); unfolded.clear(); S.plan = null; persist(); refresh(); }
  else if (t.id === 'examDate') { S.settings.exam = t.value; persist(); refresh(); }
  else if (t.id === 'hoursDay') { S.settings.hours = Math.min(12, Math.max(0.5, Number(t.value) || 2)); S.plan = null; persist(); refresh(); }
  else if (t.id === 'fStatus') renderDetail();
  else if (t.id === 'wkSelect') location.hash = 'w' + t.value;
  else if (t.id === 'importFile') importFile(t);
  else if (t.matches('.langsw input')) { lang = t.value; try { localStorage.setItem('cote-lang', lang); } catch(e) {} renderCode(); }
});
let noteTimer = null, searchTimer = null;
document.addEventListener('input', e => {
  const t = e.target;
  if (t.id === 'fText') { clearTimeout(searchTimer); searchTimer = setTimeout(renderDetail, 150); }
  else if (t.matches('textarea[data-note]')) {
    const k = t.dataset.note, v = t.value.slice(0, 2000);
    if (v.trim()) S.notes[k] = v; else delete S.notes[k];
    clearTimeout(noteTimer); noteTimer = setTimeout(persist, 600);
  }
});
document.addEventListener('click', e => {
  const t = e.target.closest('button'); if (!t) return;
  if (t.dataset.more) { const k = t.dataset.more; openPanels.has(k) ? openPanels.delete(k) : openPanels.add(k); refreshRows(k); document.querySelector(`li.row[data-key="${CSS.escape(k)}"] .more`)?.focus(); }
  else if (t.dataset.week) location.hash = 'w' + t.dataset.week;
  else if (t.dataset.rv) reviewDone(t.dataset.key, t.dataset.rv === 'ok');
  else if (t.dataset.unfold) { unfolded.add(t.dataset.unfold); renderDetail(); }
  else if (t.dataset.hint) askHint(t.dataset.key, t.dataset.hint);
  else if (t.dataset.stop) aiCtl[t.dataset.stop]?.abort();
  else if (t.dataset.mock) { if (S.timer) return toast('진행 중인 모의고사를 먼저 끝내 주세요.'); const s = findSet(t.dataset.mock); S.timer = {id: s.id, set: s.title.replace('모의고사 · ', ''), min: s.min, start: Date.now(), paused: null, pausedTotal: 0}; persist(); showTimer(); $('#tmPanel').hidden = false; }
  else if (t.id === 'tmPause') { const x = S.timer; if (x.paused) { x.pausedTotal += Date.now() - x.paused; x.paused = null; } else x.paused = Date.now(); persist(); showTimer(); }
  else if (t.id === 'tmEnd') { if (!endArmed) { endArmed = true; t.textContent = '한 번 더 누르면 기록'; setTimeout(() => { endArmed = false; t.textContent = '끝내고 기록'; }, 4000); return; } endArmed = false; t.textContent = '끝내고 기록'; endMock(true); }
  else if (t.id === 'tmCancel') endMock(false);
  else if (t.id === 'stTimer') $('#tmPanel').hidden = !$('#tmPanel').hidden;
  else if (t.id === 'themeBtn') { theme = THEMES[(THEMES.indexOf(theme) + 1) % 3]; try { localStorage.setItem('cote-theme', theme); } catch(e) {} renderTheme(); }
  else if (t.dataset.copy !== undefined || t.dataset.io !== undefined) { const code = codeOf(t.dataset.io !== undefined ? INFO.io_formats[Number(t.dataset.io)] : INFO.templates_python[Number(t.dataset.copy)]); navigator.clipboard?.writeText(code).then(() => { t.textContent = '복사됨'; setTimeout(() => t.textContent = '복사', 1500); }, () => toast('복사하지 못했습니다. 코드를 직접 선택해 주세요.')); }
  else if (t.id === 'fClear') { $('#fText').value = ''; $('#fStatus').value = ''; renderDetail(); }
  else if (t.id === 'coachBtn') askCoach();
  else if (t.id === 'moreToday') { S.plan.keys = S.plan.keys.concat(pickNext(S.plan.keys, (Number(S.settings.hours) || 2) * 60)); persist(); refresh(); }
  else if (t.id === 'coachStop') coachCtl?.abort();
  else if (t.id === 'exportBtn') exportState();
  else if (t.id === 'resetBtn') {
    if (!t.dataset.armed) { t.dataset.armed = '1'; t.textContent = '한 번 더 누르면 모두 지워집니다'; setTimeout(() => { delete t.dataset.armed; t.textContent = '기록 초기화'; }, 4000); return; }
    const {co, exam, hours} = S.settings; S = blank(); Object.assign(S.settings, {co, exam, hours});
    delete t.dataset.armed; t.textContent = '기록 초기화'; openPanels.clear(); persist(); refresh(); renderDetail(); showTimer();
  }
});

// ---------- boot ----------
renderStatic(); refresh(); route(); showTimer();
(async () => {
  if (!window.claude || !window.claude.use) return;
  const [db, user, sample] = await Promise.all(['db', 'user', 'sample'].map(n => window.claude.use(n).catch(() => null)));
  if (sample) { sampleFn = sample; $('#coachBox').hidden = false; }
  const uid = user ? await user.id() : null;
  if (db && uid) {
    try {
      docRef = db.doc(`data/users/${uid}/progress`);
      const snap = await docRef.get();
      if (snap.exists) { S = mergeState(snap.data(), S); try { localStorage.setItem('cote-state-v2', JSON.stringify(S)); } catch(e) {} }
      else if (Object.keys(S.status).length || Object.keys(S.notes).length) flush();
      setSync('기록: Claude 계정');
    } catch(e) { docRef = null; }
  }
  refresh(); renderDetail(); showTimer();
})();
