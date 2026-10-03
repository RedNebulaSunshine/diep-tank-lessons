/* editor.js: a mock of the diep.io tank editor around the live sketch in tank.js. Layers on the
   left, the canvas in the middle, the inspector on the right, the editor's own field names and
   units, a caption pill at the top of the canvas, and a step-through that adds the parts of a
   lesson one at a time. MIT, Sunshine. */
(function () {
  'use strict';
  const T = window.DiepTank;
  const num = T.num;
  const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined && text !== null) e.textContent = text; return e; };
  const fmtN = v => Math.abs(v - Math.round(v)) < 0.005 ? String(Math.round(v)) : String(Math.round(v * 100) / 100);
  const degF = r => fmtN(T.deg(num(r, 0)));
  const PROJ_BASE = { bullet: 'Bullet', drone: 'Drone', trap: 'Trap' };

  // ---- the inspector's fields, in the editor's order ----------------------------------
  function F(label, value, kind, tip) { return { label, value: (kind === undefined || kind === 'num') && typeof value === 'number' ? fmtN(value) : value, kind: kind || 'num', tip }; }
  function colorRow(label, idx, dflt) { const i = (idx === undefined || idx === null) ? dflt : idx; return { label, kind: 'color', idx: i, value: T.COLOR_NAMES[i] || ('Color ' + i) }; }
  function check(label, on, tip) { return { label, kind: 'check', on: !!on, tip }; }

  function fieldsFor(part, model, tank) {
    const d = part.data || {}, S = [];
    const sameColor = idx => idx === 27 || idx === undefined || idx === null;
    if (part.kind === 'body') {
      S.push({ head: 'Body', fields: [F('Body sides', num(d.sides, 0)), check('Drawn as a star', d.star), F('Angle', degF(d.angle)),
        F('Body size', num(d.size, 50), 'num', 'Radius at level 1. The whole tank grows as it levels.'),
        check('Team color', sameColor(d.color), 'Blue to its owner and red to everyone else, or the team’s color in team modes.'),
        sameColor(d.color) ? null : colorRow('Body color', d.color, 27)].filter(Boolean) });
      S.push({ head: 'Movement and durability', fields: [F('Move speed', num(tank.speedMultiplier, 1)), F('Field of view', num(tank.zoomMultiplier, 1)),
        F('Right-click scope', num(tank.scopeDistance, 0)), F('Knockback taken', num(tank.knockbackMultiplier, 1)), F('Auto rotate', num(d.spinSpeed, 0)),
        F('Base health', num(tank.baseHealth, 50)), F('Body damage', num(tank.baseBodyDamage, 5))] });
      const inv = tank.invisibility || {};
      const gain = num(inv.gain, 2 / 65), loh = num(inv.lossOnHit, 0.05);
      S.push({ head: 'Invisibility', fields: [check('Invisible', inv.enabled), F('Time to vanish', fmtN(1 / (25 * gain)) + ' s', 'text', 'Seconds from fully visible to gone while idle. Moving or firing shows it again.'),
        F('Reveal distance', num(inv.revealDistance, 0), 'num', 'Enemies this close see it faintly. 0 never reveals.'),
        F('Hits to reveal', loh > 0 ? fmtN(0.3 / loh + 1) : 'Never', 'text')] });
      if (tank.helpText) S.push({ head: 'Tip', fields: [F('Tip', tank.helpText, 'text', 'Shown to a player for ten seconds when they switch to this tank.')] });
      S.push({ head: 'Stat points (max per stat)', fields: [F('Movement Speed · Reload · Bullet Damage · Bullet Penetration · Bullet Speed · Body Damage · Max Health · Health Regen', (tank.statsMaxLevel || [7, 7, 7, 7, 7, 7, 7, 7]).join(' · '), 'text')] });
    } else if (part.kind === 'barrel') {
      const fl = d.flags || {};
      const geo = [F('Angle', degF(d.angle)), F('Offset', num(d.offset, 0)), F('Length', num(d.distance, 95)),
        F('Width at base', num(d.heightMultiplier, 1), 'num', 'Times a standard barrel’s width (42 units).'),
        F('Width at tip', fmtN(num(d.heightMultiplier, 1) * num(d.muzzleScale, 1)), 'num', 'Also times a standard barrel’s width. Smaller than the base tapers, larger flares.'),
        F('Gap', num(d.startDistance, 0), 'num', 'Distance between the body and where the barrel starts. Negative starts it behind the centre.'),
        check('Same color as the body', sameColor(d.color) && d.color === 27), sameColor(d.color) && d.color === 27 ? null : colorRow('Color', d.color, 1),
        check('Invisible', d.invisible, 'Invisible: it fires, nobody sees it. The editor shows it faded.')].filter(Boolean);
      S.push({ head: 'Barrel', fields: geo });
      const projs = tank.projectiles || [];
      let fires = 'Nothing';
      if (fl.holdsRaised) fires = 'Raised shapes';
      else if (Array.isArray(d.projectile)) fires = d.projectile.map(i => (projs[i] || {}).name || '?').join(' / ');
      else if (num(d.projectile, -1) >= 0 && d.bulletType !== 'none') fires = (projs[d.projectile] || {}).name || '?';
      const fireFields = [F('Fires', fires, 'text')];
      if (fires !== 'Nothing') {
        const r = (k, dflt) => { const v = d[k]; return Array.isArray(v) ? v.join(' – ') : fmtN(num(v, dflt)); };
        fireFields.push({ sub: 'Bullet stats' },
          F('Damage', r('damageMultiplier', 1)), F('Penetration', r('penetrationMultiplier', 1)), F('Bullet speed', r('speedMultiplier', 1)),
          F('Bullet size', r('bulletSizeMultiplier', 1)), F('Reload', r('reloadMultiplier', 1)), F('Spread', r('spreadMultiplier', 1)),
          F('Recoil', r('recoilMultiplier', 1)), F('Knockback', r('knockbackMultiplier', 1)), F('Launch speed', r('initialVelocityMultiplier', 1)),
          F('Lifetime', d.lifetime === undefined ? 'As usual' : r('lifetime', 3) + ' s', 'text', 'Seconds before it disappears on its own.'),
          F('Bullets per shot', num(d.numBullets, 1)), F('Fire delay', num(d.delay, 0), 'num', 'Where in its own reload cycle this barrel fires. 0.5 apart, two barrels take turns.'),
          check('Always fire', fl.forceFire), check('Fires on right click', fl.firesOnSecondary, 'Left click leaves it alone; right click fires it.'),
          check('Fires when it bursts', fl.firesOnDeath));
        if (d.bulletType === 'drone') fireFields.push({ sub: 'Drones' }, F('Max drones', num(d.numDrones, 24)), F('Crash radius', num(d.droneAggressiveCrashRadius, 900)));
      }
      S.push({ head: 'Fires', fields: fireFields });
      const ride = rideHint(part, model);
      if (ride) S.push({ head: 'Rides on', hint: ride });
    } else if (part.kind === 'shape') {
      S.push({ head: 'Part', fields: [F('Sides', num(d.sides, 0), 'num', 'Under 3 draws a circle.'), check('Drawn as a star', d.star), F('Size', num(d.size, 25)),
        F('Angle', degF(d.angle)), F('Offset X', num(d.xOffset, 0), 'num', 'Along the tank’s facing.'), F('Offset Y', num(d.yOffset, 0), 'num', 'Across the tank’s facing.'),
        F('Spin speed', num(d.spinSpeed, 0), 'num', 'Rotation per tick, in world space. 0 holds the part at its angle; negative spins the other way. The preview does not animate.'),
        check('Same color as the body', d.color === 27), d.color === 27 ? null : colorRow('Color', d.color, 0),
        check('Collidable (hitbox + body damage)', d.collidable), check('Visible while invisible', d.staysVisible)].filter(Boolean) });
      const ride = rideHint(part, model);
      if (ride) S.push({ head: 'Rides on', hint: ride });
    } else if (part.kind === 'turret') {
      S.push({ head: 'Auto turret', fields: [F('Offset X', num(d.xOffset, 0)), F('Offset Y', num(d.yOffset, 0)), F('Base size', num(d.baseSize, 25)),
        F('Facing', degF(d.angle), 'num', 'Where its arc is centred, and where it rests with nothing to shoot.'),
        F('Range', num(d.range, 1700), 'num', 'How far out it looks for a target. 0 never looks.'),
        F('Arc', num(d.arc, 0) > 0 ? degF(d.arc) : '0 · all the way round', num(d.arc, 0) > 0 ? 'num' : 'text', 'How far either side of its facing it may turn.'),
        check('Same color as the body', d.color === 27), d.color === 27 ? null : colorRow('Base color', d.color, 1),
        check('Aims with the cursor (Auto Smasher)', d.controllable)].filter(Boolean) });
      const riders = (part.carried || []).map(x => T.partName(x.bulletType !== undefined ? 'barrel' : 'shape', 0, x));
      if (riders.length) S.push({ head: 'What rides on it', hint: riders.join(', ') });
    } else if (part.kind === 'projectile') {
      const base = PROJ_BASE[d.base] || d.base;
      const own = d.sides !== undefined && d.sides !== -1;
      S.push({ head: 'Projectile', fields: [F('Name', d.name || 'Bullet', 'text'), F('Based on', base, 'text'),
        F('Shape', own ? 'Its own' : 'As usual for the kind', 'text'), own ? F('Sides', num(d.sides, 0)) : null, check('Drawn as a star', d.star),
        F('Spin', num(d.spin, 0), 'num', 'Turns as it flies. Rotation per tick.'), check('Team color', d.color === undefined || d.color === 27),
        (d.color === undefined || d.color === 27) ? null : colorRow('Color', d.color, 27)].filter(Boolean) });
      const b = d.burst || {};
      S.push({ head: 'Burst', fields: [check('Right click sets it off', b.onSecondary), check('Getting destroyed sets it off', b.onDestroyed), check('Running out of time sets it off', b.onExpire)] });
    }
    return S;
  }
  function rideHint(part, model) {
    const d = part.data;
    if (d.mountTurret !== undefined) {
      const t = model.parts.find(p => p.kind === 'turret' && p.index === d.mountTurret);
      return `Rides on ${t ? t.name : 'auto turret ' + (d.mountTurret + 1)}: angle, gap and offset are from the turret’s centre, the way a barrel sits on the body.` + (part.kind === 'barrel' ? ' It fires when the turret does.' : '');
    }
    if (d.mount !== undefined) {
      const b = model.parts.find(p => p.kind === 'barrel' && p.index === d.mount);
      return `Rides on ${b ? b.name : 'barrel ' + (d.mount + 1)}: offsets and angle are from its gun’s centre, along it.`;
    }
    return null;
  }

  // ---- DOM for the inspector ----------------------------------------------------------
  function renderInspector(box, part, model, tank) {
    box.innerHTML = '';
    if (!part) { box.appendChild(h('div', 'te-hint', 'Click a layer to edit it.')); return; }
    for (const sec of fieldsFor(part, model, tank)) {
      const s = h('div', 'te-section');
      s.appendChild(h('div', 'te-section-head', sec.head));
      if (sec.hint) s.appendChild(h('div', 'te-hint', sec.hint));
      for (const f of sec.fields || []) {
        if (f.sub) { s.appendChild(h('div', 'te-sub', f.sub)); continue; }
        if (f.kind === 'check') {
          const row = h('label', 'te-check' + (f.on ? ' on' : '')); row.appendChild(h('i', null, f.on ? '✓' : '')); row.appendChild(h('span', null, f.label));
          if (f.tip) row.title = f.tip; s.appendChild(row); continue;
        }
        const row = h('div', 'te-field'); row.appendChild(h('span', null, f.label));
        if (f.kind === 'color') { const v = h('div', 'te-value te-color'); const sw = h('i', 'te-swatch'); sw.style.background = T.PALETTE[f.idx] || '#999'; v.appendChild(sw); v.appendChild(h('b', null, f.value)); row.appendChild(v); }
        else row.appendChild(h('div', 'te-value', String(f.value)));
        if (f.tip) row.title = f.tip;
        s.appendChild(row);
      }
      box.appendChild(s);
    }
  }

  // ---- DOM for the layers list --------------------------------------------------------
  const GLYPH = { barrel: '▬', shape: '⬢', turret: '◉', body: '●', projectile: '●' };
  function renderLayers(box, model, visible, focus, onPick, subjectName) {
    box.innerHTML = '';
    const parts = model.parts.filter(p => visible.has(p.name));
    const carriedBy = p => p.data.mountTurret !== undefined ? ['turret', p.data.mountTurret] : p.data.mount !== undefined ? ['barrel', p.data.mount] : null;
    const top = parts.filter(p => !carriedBy(p));
    const isAbove = p => p.kind === 'turret' ? (p.data.aboveBody === undefined || p.data.aboveBody) : p.kind === 'barrel' ? !!(p.data.flags && p.data.flags.aboveBody) : !!p.data.aboveBody;
    const order = p => [num(p.data.order, 0), { barrel: 0, shape: 1, turret: 2 }[p.kind], p.index];
    const cmp = (a, b) => { const x = order(a), y = order(b); return (y[0] - x[0]) || (y[1] - x[1]) || (y[2] - x[2]); };   // last drawn first
    const row = (p, nested) => {
      const r = h('div', 'te-layer-row' + (nested ? ' nested' : '') + (focus && p.name === focus ? ' sel' : ''));
      const n = h('button', 'te-node');
      n.appendChild(h('i', 'te-glyph ' + p.kind, GLYPH[p.kind]));
      const sw = h('i', 'te-swatch'); sw.style.background = swatchOf(p, model); n.appendChild(sw);
      n.appendChild(h('span', 'te-layer-name', p.name));
      if (p.kind === 'barrel' && p.data.invisible) n.appendChild(h('small', 'te-tag', 'invisible'));
      if (p.kind === 'barrel' && !(p.data.bulletType && p.data.bulletType !== 'none')) n.appendChild(h('small', 'te-tag', 'looks only'));
      n.addEventListener('click', () => onPick(p));
      r.appendChild(n);
      return r;
    };
    const addWithRiders = (p, container) => {
      container.appendChild(row(p, false));
      const riders = parts.filter(q => { const c = carriedBy(q); return c && c[0] === p.kind && c[1] === p.index; }).sort(cmp);
      for (const q of riders) container.appendChild(row(q, true));
    };
    const over = top.filter(isAbove).sort(cmp), under = top.filter(p => !isAbove(p)).sort(cmp);
    const sec = (label) => { const e = h('div', 'te-layer-sec', label); box.appendChild(e); };
    sec('Over body');
    if (!over.length) box.appendChild(h('div', 'te-layer-empty', 'nothing yet'));
    for (const p of over) addWithRiders(p, box);
    const body = h('div', 'te-layer-row te-body-row' + (focus === 'Tank body' ? ' sel' : ''));
    const bn = h('button', 'te-node'); bn.appendChild(h('i', 'te-glyph body', GLYPH.body));
    const bsw = h('i', 'te-swatch'); bsw.style.background = model.team; bn.appendChild(bsw);
    bn.appendChild(h('span', 'te-layer-name', subjectName || 'Tank body'));
    bn.addEventListener('click', () => onPick(model.hull));
    body.appendChild(bn); box.appendChild(body);
    sec('Under body');
    if (!under.length) box.appendChild(h('div', 'te-layer-empty', 'nothing yet'));
    for (const p of under) addWithRiders(p, box);
  }
  function swatchOf(p, model) {
    const d = p.data;
    const dflt = p.kind === 'shape' ? 0 : 1;
    return T.fillOf(d.color, dflt, model.team);
  }

  // ---- the scene: mock editor + steps ---------------------------------------------------
  function Scene(container, cfg) {
    this.c = container; this.cfg = cfg; this.step = -1; this.auto = null;
    this.tank = cfg.tank;
    container.__scene = this;
    this._dom();
    this._subject('tank');
    this.applyStep(0);
    this._observe();
  }
  Scene.prototype._dom = function () {
    const c = this.c; c.classList.add('te');
    const head = h('div', 'te-head');
    head.appendChild(h('span', 'te-title', 'TANK EDITOR'));
    head.appendChild(h('span', 'te-crumb', (this.cfg.packName || 'Lesson pack') + ' › ' + this.tank.name));
    const tools = h('span', 'te-tools');
    this.fitBtn = h('button', 'te-tool', 'Fit'); this.fitBtn.addEventListener('click', () => this.live && this.live.fit && this.fit());
    this.playBtn = h('button', 'te-tool te-play', 'Play');
    this.playBtn.addEventListener('click', () => this.togglePlay());
    tools.appendChild(this.fitBtn); tools.appendChild(this.playBtn); head.appendChild(tools);
    c.appendChild(head);
    const body = h('div', 'te-body');
    this.left = h('aside', 'te-panel te-left'); this.left.appendChild(h('div', 'te-panel-head', 'Layers'));
    const acts = h('div', 'te-panel-actions');
    for (const a of ['+ barrel', '+ part', '+ auto turret']) acts.appendChild(h('span', 'te-adder', a));
    this.left.appendChild(acts);
    this.layers = h('div', 'te-panel-body te-layers'); this.left.appendChild(this.layers);
    this.canvas = h('div', 'te-canvas');
    this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    this.svg.setAttribute('tabindex', '0'); this.svg.setAttribute('class', 'te-svg editor');
    this.canvas.appendChild(this.svg);
    this.status = h('div', 'te-status'); this.canvas.appendChild(this.status);
    this.sel = h('div', 'te-sel'); this.canvas.appendChild(this.sel);
    const ctl = h('div', 'te-stepbar');
    this.prevBtn = h('button', 'te-btn', '‹'); this.nextBtn = h('button', 'te-btn', '›');
    this.counter = h('span', 'te-counter', ''); this.autoBtn = h('button', 'te-btn te-auto', 'Auto');
    this.prevBtn.addEventListener('click', () => { this.stopAuto(); this.applyStep(this.step - 1); });
    this.nextBtn.addEventListener('click', () => { this.stopAuto(); this.applyStep(this.step + 1); });
    this.autoBtn.addEventListener('click', () => this.auto ? this.stopAuto() : this.startAuto());
    ctl.appendChild(this.prevBtn); ctl.appendChild(this.counter); ctl.appendChild(this.nextBtn); ctl.appendChild(this.autoBtn);
    this.canvas.appendChild(ctl);
    this.right = h('aside', 'te-panel te-right'); this.inspHead = h('div', 'te-panel-head', 'Inspector'); this.right.appendChild(this.inspHead);
    this.insp = h('div', 'te-panel-body te-insp'); this.right.appendChild(this.insp);
    body.appendChild(this.left); body.appendChild(this.canvas); body.appendChild(this.right);
    c.appendChild(body);
    const foot = h('div', 'te-foot');
    if (this.cfg.packFile) { const a = h('a', 'te-btn te-download', 'Download ' + this.cfg.packFile); a.href = 'packs/' + this.cfg.packFile; a.setAttribute('download', this.cfg.packFile); foot.appendChild(a); }
    const copy = h('button', 'te-btn', 'Copy tank JSON');
    copy.addEventListener('click', () => {
      const pack = JSON.stringify({ version: 2, name: this.tank.name, author: this.cfg.author || undefined, tanks: [this.tank] });
      const done = () => { copy.textContent = 'Copied. Paste it onto a pack with Ctrl+V'; setTimeout(() => copy.textContent = 'Copy tank JSON', 2500); };
      if (navigator.clipboard) navigator.clipboard.writeText(pack).then(done, () => prompt('Copy this:', pack)); else prompt('Copy this:', pack);
    });
    foot.appendChild(copy);
    foot.appendChild(h('span', 'te-foot-hint', 'In the editor: Import pack → choose the file → Import as new pack. Or paste the JSON onto a pack with Ctrl+V.'));
    c.appendChild(foot);
    window.addEventListener('resize', () => this._selectionBox());
  };
  Scene.prototype._subject = function (name) {
    if (this.subject === name) return;
    this.subject = name;
    if (this.live) this.live.stop();
    let tankLike = this.tank, team;
    if (name !== 'tank') {
      const proj = (this.tank.projectiles || []).find(p => p.name === name);
      tankLike = T.projectileAsTank(proj, null); this.proj = proj;
      tankLike.name = proj.name;
    }
    this.live = new T.Live(this.svg, tankLike, Object.assign({ view: 560 }, this.cfg.live || {}));
    this.model = this.live.model;
    this.fit();
  };
  Scene.prototype.fit = function () {
    const b = T.bbox(this.model.root);
    const ext = Math.max(Math.abs(b.x), Math.abs(b.y), Math.abs(b.x + b.w), Math.abs(b.y + b.h), 110);
    const V = Math.max(440, Math.ceil(ext * 2.35));
    this.live.opts.view = V;
    this.svg.setAttribute('viewBox', `${-V / 2} ${-V / 2} ${V} ${V}`);
    this._selectionBox();
  };
  Scene.prototype.steps = function () { return this.cfg.steps || [{ show: 'all', say: '' }]; };
  Scene.prototype.applyStep = function (i) {
    const steps = this.steps(); i = Math.max(0, Math.min(steps.length - 1, i));
    this.step = i; const st = steps[i];
    this._subject(st.subject || 'tank');
    if (st.live) { this.setLive(true); } else { this.setLive(false); }
    const all = this.model.parts.map(p => p.name);
    const show = st.show === 'all' || st.live || st.show === undefined ? new Set(all) : new Set(st.show);
    for (const p of this.model.parts) p.el.classList.toggle('hidden', !show.has(p.name));
    this.visible = show;
    this.focus = st.focus || (st.live ? null : (st.show && st.show.length ? st.show[st.show.length - 1] : 'Tank body'));
    const subjectName = this.subject === 'tank' ? 'Tank body' : this.proj.name;
    renderLayers(this.layers, this.model, show, this.focus, p => this.pick(p), subjectName);
    this._inspect();
    this.status.innerHTML = markup(st.say || '');
    this.status.classList.toggle('hide', !st.say);
    this.counter.textContent = (i + 1) + ' / ' + steps.length;
    this.prevBtn.disabled = i === 0; this.nextBtn.disabled = i === steps.length - 1;
    this._selectionBox();
  };
  Scene.prototype.pick = function (p) { this.stopAuto(); this.focus = p.name; this._inspect(); const st = this.steps()[this.step]; renderLayers(this.layers, this.model, this.visible, this.focus, q => this.pick(q), this.subject === 'tank' ? 'Tank body' : this.proj.name); this._selectionBox(); void st; };
  Scene.prototype._inspect = function () {
    let part = null;
    if (this.focus === 'Tank body') part = this.model.hull;
    else if (this.focus === 'Projectile' && this.proj) part = { kind: 'projectile', data: this.proj, name: this.proj.name };
    else if (this.focus) part = this.model.byName[this.focus] || null;
    if (part && part.kind === 'body' && this.subject !== 'tank') part = { kind: 'projectile', data: this.proj, name: this.proj.name };
    this.inspHead.textContent = part ? ({ body: 'Tank', barrel: 'Barrel', shape: 'Part', turret: 'Auto turret', projectile: 'Projectile' }[part.kind] + ' · ' + part.name) : 'Inspector';
    renderInspector(this.insp, part, this.model, this.tank);
  };
  Scene.prototype._selectionBox = function () {
    const p = this.focus === 'Tank body' ? this.model.hull : (this.focus ? this.model.byName[this.focus] : null);
    if (!p || this.isLive || !p.el || p.el.classList.contains('hidden')) { this.sel.style.display = 'none'; return; }
    const r = p.el.getBoundingClientRect(), c = this.canvas.getBoundingClientRect();
    if (!r.width && !r.height) { this.sel.style.display = 'none'; return; }
    Object.assign(this.sel.style, { display: 'block', left: (r.left - c.left - 6) + 'px', top: (r.top - c.top - 6) + 'px', width: (r.width + 12) + 'px', height: (r.height + 12) + 'px' });
  };
  Scene.prototype.setLive = function (on) {
    this.isLive = on;
    this.live.setEditor(!on);
    if (on) { this.live.touched = false; this.live.start(); this.playBtn.textContent = 'Back to the editor'; this.c.classList.add('live'); this.sel.style.display = 'none'; }
    else { this.live.start(); this.playBtn.textContent = 'Play'; this.c.classList.remove('live'); }
  };
  Scene.prototype.togglePlay = function () {
    this.stopAuto();
    const steps = this.steps();
    if (this.isLive) { this.applyStep(Math.max(0, steps.findIndex(s => s.live) - 1)); return; }
    const li = steps.findIndex(s => s.live);
    if (li >= 0) this.applyStep(li);
    else { this.setLive(true); this.status.innerHTML = markup(this.cfg.liveSay || 'Hold the mouse button to fire · right button for the right-click move · WASD moves.'); }
  };
  Scene.prototype.startAuto = function () {
    this.stopAuto(); this.autoBtn.classList.add('on');
    const tick = () => { const n = this.step + 1; if (n >= this.steps().length) { this.stopAuto(); return; } this.applyStep(n); this.auto = setTimeout(tick, 4200); };
    this.auto = setTimeout(tick, 3600);
  };
  Scene.prototype.stopAuto = function () { if (this.auto) clearTimeout(this.auto); this.auto = null; this.autoBtn.classList.remove('on'); };
  Scene.prototype._observe = function () {
    if (!('IntersectionObserver' in window)) { this.startAuto(); return; }
    let started = false;
    const io = new IntersectionObserver(es => {
      for (const e of es) {
        if (e.isIntersecting && !started) { started = true; this.startAuto(); }
        if (!e.isIntersecting && this.live) this.live.stop(); else if (e.isIntersecting && this.live) this.live.start();
      }
    }, { threshold: 0.35 });
    io.observe(this.c);
  };
  function markup(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/`(.+?)`/g, '<code>$1</code>');
  }

  // ---- boot every scene on the page -----------------------------------------------------
  function boot() {
    document.querySelectorAll('[data-scene]').forEach(box => {
      const script = box.querySelector('script[type="application/json"]');
      if (!script) return;
      let cfg;
      try { cfg = JSON.parse(script.textContent); } catch (e) { box.textContent = 'This lesson’s demo could not be read.'; return; }
      script.remove();
      try { new Scene(box, cfg); } catch (e) { box.textContent = 'This browser could not draw the demo: ' + e.message; console.error(e); }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  window.DiepEditor = { Scene, fieldsFor, renderInspector, renderLayers };
})();
