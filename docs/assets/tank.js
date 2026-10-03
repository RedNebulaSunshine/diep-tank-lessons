/* tank.js: draws a .diep-pack tank the way the editor draws it, as SVG you can animate.
   A port of the diep-pack skill's render_pack.py (same drawing rules: draw order, the body
   splitting over from under, outlines at 72 % of the fill, polygon hulls at 1.3 x, stars at
   0.4 inner radius) plus a small "live" simulation of the moving tricks the lessons teach:
   spinning parts, turrets that watch, follow the cursor or swing back, barrels that pump and
   fire, stationary shots that trail, recoil dashes and fading. It is a sketch of the game, not
   the game: speeds and timings are approximate. MIT, Sunshine. */
(function (global) {
  'use strict';

  const PALETTE = ['#555555', '#999999', '#00B2E1', '#999999', '#F14E54', '#BF7FF5', '#00E16E', '#8AFF69',
    '#FFE869', '#FC7677', '#768DFC', '#F177DD', '#999999', '#43FF91', '#BBBBBB', '#999999',
    '#FCC376', '#999999', '#35C5DB', '#FFFFFF', '#3D3D3D', '#12A5A5', '#4A57C8', '#A9724A',
    '#B5323A', '#2E9E5B', '#7B4FA8', '#00B2E1', '#999999', '#999999'];
  const COLOR_NAMES = { 0: 'Border (grey)', 1: 'Cannon', 2: 'Blue', 4: 'Red', 5: 'Purple', 6: 'Green', 7: 'Shiny',
    8: 'Yellow', 9: 'Salmon', 10: 'Periwinkle', 11: 'Pink', 13: 'Mint', 14: 'Box', 16: 'Orange', 18: 'Cyan',
    19: 'White', 20: 'Charcoal', 21: 'Teal', 22: 'Indigo', 23: 'Brown', 24: 'Crimson', 25: 'Forest', 26: 'Plum',
    27: 'Same color as the body' };
  const TEAM_HEX = '#00B2E1';     // the owner's blue
  const ENEMY_HEX = '#FFE869';    // a square, the way the arena draws one
  const STROKE = 7.5, HULL_R = 50, POLY_HULL = 1.3, STAR_INNER = 0.4, TICKS = 25;
  const NS = 'http://www.w3.org/2000/svg';

  // ---- helpers ---------------------------------------------------------------------------
  const deg = r => r * 180 / Math.PI;
  const rad = d => d * Math.PI / 180;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const wrap = a => { while (a > Math.PI) a -= 2 * Math.PI; while (a < -Math.PI) a += 2 * Math.PI; return a; };
  const rot = (p, a) => { const c = Math.cos(a), s = Math.sin(a); return [p[0] * c - p[1] * s, p[0] * s + p[1] * c]; };
  const num = (v, d) => (v === undefined || v === null || Number.isNaN(+v)) ? d : +v;
  const hi = v => Array.isArray(v) ? Math.max(...v) : v;   // a [min, max] roll counts its max

  function fillOf(idx, dflt, team) {
    if (idx === undefined || idx === null) idx = dflt;
    if (idx === 27) return team || TEAM_HEX;
    if (!(idx >= 0 && idx < PALETTE.length)) idx = dflt;
    return PALETTE[idx];
  }
  function strokeOf(hex) {
    const n = parseInt(hex.slice(1), 16);
    const f = v => Math.round(v * 0.72).toString(16).padStart(2, '0');
    return '#' + f((n >> 16) & 255) + f((n >> 8) & 255) + f(n & 255);
  }
  function polyPoints(sides, r, star) {
    const pts = [];
    if (star) {
      for (let k = 0; k < sides * 2; k++) {
        const rr = (k % 2 === 0) ? r * STAR_INNER : r, a = Math.PI * k / sides;
        pts.push([rr * Math.cos(a), rr * Math.sin(a)]);
      }
      return pts;
    }
    const base = sides === 4 ? Math.PI / 4 : 0;
    for (let k = 0; k < sides; k++) { const a = base + 2 * Math.PI * k / sides; pts.push([r * Math.cos(a), r * Math.sin(a)]); }
    return pts;
  }
  const fmt = v => (Math.round(v * 100) / 100).toString();
  const fmtPts = pts => pts.map(p => fmt(p[0]) + ',' + fmt(p[1])).join(' ');
  function el(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    if (attrs) for (const k in attrs) if (attrs[k] !== undefined && attrs[k] !== null) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function filled(tag, attrs, hex, parent) {
    return el(tag, Object.assign({ fill: hex, stroke: strokeOf(hex), 'stroke-width': STROKE, 'stroke-linejoin': 'round' }, attrs), parent);
  }
  function partName(kind, i, data) {
    return (data.editor && data.editor.name) || ({ barrel: 'Barrel', shape: 'Part', turret: 'Auto turret' }[kind] + ' ' + (i + 1));
  }

  // ---- building the SVG ----------------------------------------------------------------
  /* Returns {root, parts, byName, hull, team}. parts: [{kind, index, name, data, el, ...}].
     Element layout (all in the tank frame: x forward, y to the tank's right):
       shape : g.part.shape[translate] > g.rot[rotate] > polygon|circle
       barrel: g.part.barrel[rotate]   > g.pump[translate] > (g.mid under | polygon | g.mid above)
       turret: g.part.turret[translate]> g.rot[rotate]     > (under | circle | above)
     under/above = parts mounted on it, in their own g.part groups. */
  function build(tank, opts) {
    opts = opts || {};
    const barrels = tank.barrels || [], shapes = tank.bodyShapes || [], turrets = tank.turrets || [];
    const body = tank.body || {};
    const team = opts.team || ((body.color !== undefined && body.color !== null && body.color !== 27) ? fillOf(body.color, 2) : TEAM_HEX);
    const parts = [], byName = {};
    const root = el('g', { class: 'tank' });
    const gUnder = el('g', { class: 'under' }, root), gHull = el('g', { class: 'hull' }, root), gAbove = el('g', { class: 'above' }, root);

    function reg(kind, i, data, elem) {
      const p = { kind, index: i, name: partName(kind, i, data), data, el: elem };
      elem.setAttribute('data-name', p.name); elem.setAttribute('data-kind', kind);
      parts.push(p); byName[p.name] = p;
      return p;
    }
    function shapeEl(s, i) {
      const size = num(s.size, 25), sides = s.sides | 0;
      const fill = fillOf(s.color, 0, team);
      const g = el('g', { class: 'part shape', transform: `translate(${fmt(num(s.xOffset, 0))} ${fmt(num(s.yOffset, 0))})` });
      const r = el('g', { class: 'rot', transform: `rotate(${fmt(deg(num(s.angle, 0)))})` }, g);
      if (sides <= 2) filled('circle', { r: size }, fill, r);
      else filled('polygon', { points: fmtPts(polyPoints(sides, size, !!s.star)) }, fill, r);
      const p = reg('shape', i, s, g);
      p.rotEl = r; p.baseAngle = num(s.angle, 0); p.spin = num(s.spinSpeed, 0);
      if (s.staysVisible) g.classList.add('stays-visible');
      return p;
    }
    function barrelEl(b, i) {
      const x0 = num(b.startDistance, 0), x1 = x0 + Math.min(num(b.distance, 95), 500), off = num(b.offset, 0);
      const hw0 = 21 * num(b.heightMultiplier, 1), hw1 = hw0 * num(b.muzzleScale, 1);
      const fill = fillOf(b.color, 1, team);
      const g = el('g', { class: 'part barrel', transform: `rotate(${fmt(deg(num(b.angle, 0)))})` });
      const pump = el('g', { class: 'pump' }, g);
      const midU = el('g', { class: 'mid', transform: `translate(${fmt((x0 + x1) / 2)} ${fmt(off)})` }, pump);
      const poly = filled('polygon', { points: fmtPts([[x0, off + hw0], [x1, off + hw1], [x1, off - hw1], [x0, off - hw0]]) }, fill, pump);
      const midA = el('g', { class: 'mid', transform: `translate(${fmt((x0 + x1) / 2)} ${fmt(off)})` }, pump);
      const p = reg('barrel', i, b, g);
      Object.assign(p, { pumpEl: pump, midUnder: midU, midAbove: midA, poly, muzzle: [x1, off], base: [x0, off], angle: num(b.angle, 0), length: x1 - x0 });
      if (b.invisible) g.classList.add('invisible');
      return p;
    }
    const mountedOnBarrel = i => {
      const items = barrels.map((b, j) => b.mount === i && b.mountTurret === undefined ? { o: num(b.order, 0), k: 0, j, kind: 'barrel', above: !!(b.flags && b.flags.aboveBody) } : null)
        .concat(shapes.map((s, j) => s.mount === i && s.mountTurret === undefined ? { o: num(s.order, 0), k: 1, j, kind: 'shape', above: !!s.aboveBody } : null))
        .filter(Boolean);
      return items.sort((a, b) => a.o - b.o || a.k - b.k || a.j - b.j);
    };
    const seen = new Set();
    function emitBarrel(i, container) {
      if (seen.has(i)) return; seen.add(i);
      const p = barrelEl(barrels[i], i);
      const mounted = mountedOnBarrel(i);
      for (const m of mounted) if (!m.above) (m.kind === 'barrel' ? emitBarrel(m.j, p.midUnder) : emitShape(m.j, p.midUnder));
      for (const m of mounted) if (m.above) (m.kind === 'barrel' ? emitBarrel(m.j, p.midAbove) : emitShape(m.j, p.midAbove));
      container.appendChild(p.el);
      return p;
    }
    function emitShape(i, container) { const p = shapeEl(shapes[i], i); container.appendChild(p.el); return p; }
    function emitTurret(i, container) {
      const t = turrets[i];
      const g = el('g', { class: 'part turret', transform: `translate(${fmt(num(t.xOffset, 0))} ${fmt(num(t.yOffset, 0))})` });
      const r = el('g', { class: 'rot', transform: `rotate(${fmt(deg(num(t.angle, 0)))})` }, g);
      const items = barrels.map((b, j) => b.mountTurret === i ? { o: num(b.order, 0), k: 1, j, kind: 'barrel', above: !!(b.flags && b.flags.aboveBody) } : null)
        .concat(shapes.map((s, j) => s.mountTurret === i ? { o: num(s.order, 0), k: 0, j, kind: 'shape', above: !!s.aboveBody } : null))
        .filter(Boolean).sort((a, b) => a.o - b.o || a.k - b.k || a.j - b.j);
      for (const m of items) if (!m.above) (m.kind === 'barrel' ? emitBarrel(m.j, r) : emitShape(m.j, r));
      const disc = filled('circle', { r: num(t.baseSize, 25), class: 'disc' }, fillOf(t.color, 1, team), r);
      for (const m of items) if (m.above) (m.kind === 'barrel' ? emitBarrel(m.j, r) : emitShape(m.j, r));
      const p = reg('turret', i, t, g);
      Object.assign(p, { rotEl: r, disc, rest: num(t.angle, 0), arc: num(t.arc, 0), range: num(t.range, 1700),
        controllable: !!t.controllable, heading: 0, vel: 0, carried: items.map(m => m.kind === 'barrel' ? barrels[m.j] : shapes[m.j]) });
      container.appendChild(g);
      return p;
    }
    // 1. parts under the body, in `order` (ties: barrels, shapes, turrets, then array order)
    const under = [], above = [];
    barrels.forEach((b, i) => { if (b.mountTurret === undefined && b.mount === undefined) (b.flags && b.flags.aboveBody ? above : under).push({ o: num(b.order, 0), k: 0, i, kind: 'barrel' }); });
    shapes.forEach((s, i) => { if (s.mountTurret === undefined && s.mount === undefined) (s.aboveBody ? above : under).push({ o: num(s.order, 0), k: 1, i, kind: 'shape' }); });
    turrets.forEach((t, i) => { ((t.aboveBody === undefined || t.aboveBody) ? above : under).push({ o: num(t.order, 0), k: 2, i, kind: 'turret' }); });
    const cmp = (a, b) => a.o - b.o || a.k - b.k || a.i - b.i;
    under.sort(cmp); above.sort(cmp);
    const emit = (it, c) => it.kind === 'barrel' ? emitBarrel(it.i, c) : it.kind === 'shape' ? emitShape(it.i, c) : emitTurret(it.i, c);
    for (const it of under) emit(it, gUnder);
    // 2. the body
    const sides = body.sides | 0, size = num(body.size, HULL_R);
    const hullFill = fillOf(body.color, 2, team);
    const hullRot = el('g', { class: 'rot', transform: `rotate(${fmt(deg(num(body.angle, 0)))})` }, gHull);
    if (sides <= 2) filled('circle', { r: size }, hullFill, hullRot);
    else filled('polygon', { points: fmtPts(polyPoints(sides, size * POLY_HULL, !!body.star)) }, hullFill, hullRot);
    const hull = { kind: 'body', name: 'Tank body', data: body, el: gHull, rotEl: hullRot, baseAngle: num(body.angle, 0), spin: num(body.spinSpeed, 0), size };
    gHull.setAttribute('data-name', 'Tank body'); gHull.setAttribute('data-kind', 'body');
    // 3. parts over the body
    for (const it of above) emit(it, gAbove);
    return { root, parts, byName, hull, team, tank };
  }

  /* A projectile drawn like the editor's "What a barrel fires" view: its disc as a hull of radius 50. */
  function projectileAsTank(proj, team) {
    const sides = proj.sides === undefined ? -1 : proj.sides | 0;
    return { body: { sides: sides >= 3 ? sides : 0, size: HULL_R, star: !!proj.star, color: proj.color },
      bodyShapes: proj.parts || [], barrels: proj.barrels || [], turrets: proj.turrets || [], _team: team };
  }

  /* Bounding box of everything drawn (tank units), with the outline. */
  function bbox(root) {
    try {
      const b = root.getBBox();
      return { x: b.x - STROKE, y: b.y - STROKE, w: b.width + 2 * STROKE, h: b.height + 2 * STROKE };
    } catch (e) { return { x: -100, y: -100, w: 200, h: 200 }; }
  }

  // ---- the live sketch -----------------------------------------------------------------
  /* new Live(svg, tank, {enemy, drive:'none'|'auto', autofire, team}). The tank sits at the
     origin of its own group inside a camera group; the world (shots, the enemy) is drawn in
     world units around it. Screen y is down, so a heading of -90 deg faces up. */
  function Live(svg, tank, opts) {
    this.svg = svg; this.tank = tank; this.opts = Object.assign({ enemy: false, drive: 'none', autofire: false, view: 560 }, opts || {});
    this.t = 0; this.last = null; this.running = false; this.editor = true;
    this.pos = [0, 0]; this.vel = [0, 0]; this.heading = -Math.PI / 2; this.alpha = 1; this.idleFor = 0;
    this.mouse = null; this.aim = null; this.touched = false; this.fire = false; this.fire2 = false; this.keys = {};
    this.shots = []; this.lastMoveT = 0; this.lastFireT = -9;
    this._setup();
  }
  Live.prototype._setup = function () {
    const svg = this.svg, V = this.opts.view;
    svg.setAttribute('viewBox', `${-V / 2} ${-V / 2} ${V} ${V}`);
    svg.innerHTML = '';
    const defs = el('defs', null, svg);
    const pid = 'grid' + Math.random().toString(36).slice(2, 7);
    const pat = el('pattern', { id: pid, width: 40, height: 40, patternUnits: 'userSpaceOnUse' }, defs);
    el('rect', { width: 40, height: 40, fill: '#cdcdcd' }, pat);
    el('path', { d: 'M40 0H0V40', fill: 'none', stroke: '#c0c0c0', 'stroke-width': 1 }, pat);
    this.grid = pat;
    el('rect', { x: -V, y: -V, width: 2 * V, height: 2 * V, fill: `url(#${pid})`, class: 'grid' }, svg);
    this.camera = el('g', { class: 'camera' }, svg);
    this.world = el('g', { class: 'world' }, this.camera);
    this.tankG = el('g', { class: 'tank-frame' }, this.camera);
    this.model = build(this.tank, { team: this.opts.team });
    this.tankG.appendChild(this.model.root);
    this.overlay = el('g', { class: 'overlay' }, svg);
    this.turrets = this.model.parts.filter(p => p.kind === 'turret');
    this.spinners = this.model.parts.filter(p => p.kind === 'shape' && p.spin).concat(this.model.hull.spin ? [this.model.hull] : []);
    this.guns = this.model.parts.filter(p => p.kind === 'barrel' && p.data.bulletType && p.data.bulletType !== 'none'
      && (Array.isArray(p.data.projectile) || num(p.data.projectile, -1) >= 0));
    for (const g of this.guns) { g.next = null; g.pumpT = -9; }
    for (const t of this.turrets) { t.heading = this.heading + t.rest; t.vel = 0; }
    if (this.opts.enemy) {
      this.enemy = el('g', { class: 'enemy' }, this.world);
      filled('polygon', { points: fmtPts(polyPoints(4, 27, false)) }, ENEMY_HEX, this.enemy);
      this.enemyPos = [190, -40]; this.enemyAng = 0;
    }
    this._bind();
    this._place();
  };
  Live.prototype._bind = function () {
    const svg = this.svg, self = this;
    const toWorld = ev => {
      const pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
      const m = svg.getScreenCTM(); if (!m) return null;
      const p = pt.matrixTransform(m.inverse());
      return [p.x + self.pos[0], p.y + self.pos[1]];
    };
    svg.addEventListener('pointermove', ev => { self.mouse = toWorld(ev); self.touched = true; });
    svg.addEventListener('pointerleave', () => { self.mouse = null; self.fire = false; self.fire2 = false; });
    svg.addEventListener('pointerdown', ev => {
      self.mouse = toWorld(ev); self.touched = true;
      if (ev.button === 2) self.fire2 = true; else self.fire = true;
      try { svg.setPointerCapture(ev.pointerId); } catch (e) { /* ignore */ }
      ev.preventDefault();
    });
    const up = ev => { if (ev.button === 2) self.fire2 = false; else self.fire = false; };
    svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
    svg.addEventListener('contextmenu', ev => ev.preventDefault());
    svg.addEventListener('keydown', ev => { const k = ev.key.toLowerCase(); if ('wasd'.includes(k) || ev.key.startsWith('Arrow')) { self.keys[k] = true; ev.preventDefault(); } });
    svg.addEventListener('keyup', ev => { self.keys[ev.key.toLowerCase()] = false; });
  };
  Live.prototype.setEditor = function (on) {
    this.editor = on;
    this.svg.classList.toggle('editor', on);
    if (on) {
      this.heading = -Math.PI / 2; this.pos = [0, 0]; this.vel = [0, 0]; this.alpha = 1;
      for (const t of this.turrets) { t.heading = this.heading + t.rest; t.vel = 0; t.rotEl.setAttribute('transform', `rotate(${fmt(deg(t.rest))})`); }
      for (const g of this.guns) { g.pumpEl.setAttribute('transform', ''); g.next = null; }
      for (const s of this.shots) s.el.remove();
      this.shots = [];
      this._place();
      this._applyAlpha(1);
    } else { this.last = null; this.t = 0; }
  };
  Live.prototype.start = function () { if (this.running) return; this.running = true; this.last = null; const self = this; const loop = ts => { if (!self.running) return; self._frame(ts); requestAnimationFrame(loop); }; requestAnimationFrame(loop); };
  Live.prototype.stop = function () { this.running = false; };
  Live.prototype._place = function () {
    this.camera.setAttribute('transform', `translate(${fmt(-this.pos[0])} ${fmt(-this.pos[1])})`);
    this.grid.setAttribute('patternTransform', `translate(${fmt(-this.pos[0] % 40)} ${fmt(-this.pos[1] % 40)})`);
    this.tankG.setAttribute('transform', `translate(${fmt(this.pos[0])} ${fmt(this.pos[1])}) rotate(${fmt(deg(this.heading))})`);
    if (this.enemy) this.enemy.setAttribute('transform', `translate(${fmt(this.enemyPos[0])} ${fmt(this.enemyPos[1])}) rotate(${fmt(deg(this.enemyAng))})`);
  };
  Live.prototype._applyAlpha = function (a) {
    const v = a >= 0.999 ? null : fmt(Math.max(0.04, a));
    const set = e => { if (v === null) e.removeAttribute('opacity'); else e.setAttribute('opacity', v); };
    set(this.model.hull.el);
    for (const p of this.model.parts) if (!p.el.classList.contains('stays-visible')) set(p.el);
  };
  Live.prototype.local2world = function (p) { const r = rot(p, this.heading); return [r[0] + this.pos[0], r[1] + this.pos[1]]; };
  Live.prototype.turretWorld = function (t) { return this.local2world([num(t.data.xOffset, 0), num(t.data.yOffset, 0)]); };

  Live.prototype._frame = function (ts) {
    if (this.last === null) { this.last = ts; return; }
    const dt = Math.min(0.05, (ts - this.last) / 1000); this.last = ts; this.t += dt;
    if (this.editor) return;   // like the editor's preview, the mock does not animate
    const tank = this.tank;
    // -- enemy drifts round the tank
    if (this.enemy) {
      const a = this.t * 0.55, r = 180 + 40 * Math.sin(this.t * 0.9);
      this.enemyPos = [this.pos[0] + r * Math.cos(a), this.pos[1] + r * Math.sin(a) * 0.8]; this.enemyAng += 0.4 * dt;
    }
    // -- until the reader touches the canvas, a demo hand sweeps the cursor and works the buttons
    const demo = !this.touched && this.opts.demo !== false;
    if (demo) {
      const a = -Math.PI / 2 + 0.9 * Math.sin(this.t * 0.7);
      this.aim = [this.pos[0] + 230 * Math.cos(a), this.pos[1] + 230 * Math.sin(a)];
      const cyc = this.t % 7;
      this.fire = this.guns.some(g => !(g.data.flags && (g.data.flags.forceFire || g.data.flags.firesOnSecondary))) && cyc > 1.5 && cyc < 4.5;
      this.fire2 = this.guns.some(g => g.data.flags && g.data.flags.firesOnSecondary) && cyc > 5.5 && cyc < 5.7;
    } else this.aim = this.mouse;
    // -- facing: the cursor, or the demo hand
    let target = this.aim ? Math.atan2(this.aim[1] - this.pos[1], this.aim[0] - this.pos[0]) : this.heading;
    this.heading += wrap(target - this.heading) * Math.min(1, 10 * dt);
    // -- movement: keys, an automatic loop, and recoil
    let moving = false, v = [0, 0];
    const speed = 170 * num(tank.speedMultiplier, 1);
    if (this.keys.w || this.keys.arrowup) v[1] -= 1; if (this.keys.s || this.keys.arrowdown) v[1] += 1;
    if (this.keys.a || this.keys.arrowleft) v[0] -= 1; if (this.keys.d || this.keys.arrowright) v[0] += 1;
    if (v[0] || v[1]) { const n = Math.hypot(v[0], v[1]); v = [v[0] / n * speed, v[1] / n * speed]; moving = true; }
    else if (this.opts.drive === 'auto') { const a = this.t * 0.5; v = [120 * Math.cos(a), 120 * Math.sin(2 * a) * 0.9]; moving = true; }
    this.pos[0] += (v[0] + this.vel[0]) * dt; this.pos[1] += (v[1] + this.vel[1]) * dt;
    const damp = Math.exp(-5 * dt); this.vel[0] *= damp; this.vel[1] *= damp;
    if (Math.hypot(this.vel[0], this.vel[1]) > 20) moving = true;
    if (moving) this.lastMoveT = this.t;
    // -- turrets: a spring toward their target, inside their wedge
    for (const t of this.turrets) {
      const restAbs = this.heading + t.rest, wp = this.turretWorld(t);
      let aim = restAbs;
      const inWedge = a => t.arc <= 0 || Math.abs(wrap(a - restAbs)) <= t.arc + 1e-6;
      const firing = this.fire || this.fire2;
      if (t.controllable && firing && this.aim) {
        const a = Math.atan2(this.aim[1] - wp[1], this.aim[0] - wp[0]);
        if (inWedge(a)) aim = a;
      } else if (t.range > 0 && this.enemy) {
        const d = Math.hypot(this.enemyPos[0] - wp[0], this.enemyPos[1] - wp[1]);
        const a = Math.atan2(this.enemyPos[1] - wp[1], this.enemyPos[0] - wp[0]);
        if (d <= t.range && inWedge(a)) aim = a;
      }
      if (t.arc > 0) aim = restAbs + clamp(wrap(aim - restAbs), -t.arc, t.arc);
      const err = wrap(aim - t.heading);
      t.vel += (90 * err - 11 * t.vel) * dt; t.heading += t.vel * dt;
      if (t.arc > 0) { const e2 = wrap(t.heading - restAbs); if (Math.abs(e2) > t.arc) { t.heading = restAbs + clamp(e2, -t.arc, t.arc); t.vel *= -0.3; } }
      t.rotEl.setAttribute('transform', `rotate(${fmt(deg(wrap(t.heading - this.heading)))})`);
    }
    // -- barrels fire
    const reloadTicks = 15;   // an unupgraded tank: 15 ticks per reload period
    for (const g of this.guns) {
      const b = g.data, f = b.flags || {};
      const trig = f.forceFire || (this.fire && !f.firesOnSecondary) || (this.fire2 && f.firesOnSecondary);
      if (!trig) { g.next = null; }
      else {
        const period = reloadTicks / TICKS * num(b.reloadMultiplier, 1);
        if (g.next === null) g.next = this.t + period * num(b.delay, 0);
        let n = 0;
        while (this.t >= g.next && n++ < 4) { this._fire(g); g.next += period; }
      }
      const since = this.t - g.pumpT;
      const k = since < 0.35 ? 10 * Math.exp(-7 * since) * Math.min(1, since * 30) : 0;
      g.pumpEl.setAttribute('transform', k > 0.05 ? `translate(${fmt(-k)} 0)` : '');
    }
    // -- shots
    for (let i = this.shots.length - 1; i >= 0; i--) {
      const s = this.shots[i]; s.age += dt;
      if (s.age >= s.life) { this._expire(s); this.shots.splice(i, 1); continue; }
      const sp = s.launch + (s.cruise - s.launch) * Math.min(1, s.age / 0.35);
      s.pos[0] += s.dir[0] * sp * dt; s.pos[1] += s.dir[1] * sp * dt; s.ang += s.spin * TICKS * dt;
      s.el.setAttribute('transform', `translate(${fmt(s.pos[0])} ${fmt(s.pos[1])}) rotate(${fmt(deg(s.ang))}) scale(${fmt(s.r / HULL_R)})`);
    }
    // -- fading
    const inv = tank.invisibility || {};
    if (inv.enabled) {
      const active = (this.t - this.lastMoveT < 0.25) || (this.t - this.lastFireT < 0.25);
      if (active) this.alpha = Math.min(1, this.alpha + 4 * dt);
      else this.alpha = Math.max(0, this.alpha - num(inv.gain, 2 / 65) * TICKS * dt);
      this._applyAlpha(this.alpha);
    }
    this._spin(dt);
    this._place();
  };
  Live.prototype._spin = function (dt) {
    for (const s of this.spinners) { s.baseAngle += s.spin * TICKS * dt; s.rotEl.setAttribute('transform', `rotate(${fmt(deg(s.baseAngle))})`); }
  };
  Live.prototype._fire = function (g) {
    const b = g.data, tank = this.tank;
    g.pumpT = this.t; if (!(b.flags && b.flags.forceFire)) this.lastFireT = this.t;
    let pi = b.projectile; if (Array.isArray(pi)) pi = pi[Math.floor(Math.random() * pi.length)];
    const proj = (tank.projectiles || [])[pi]; if (!proj) return;
    // where the muzzle is, through whatever the barrel rides on
    let m = g.muzzle, angle = g.angle;
    const t = b.mountTurret !== undefined ? this.turrets.find(x => x.index === b.mountTurret) : null;
    let world, dirA;
    if (t) { const local = rot(m, t.heading - this.heading); world = this.local2world([num(t.data.xOffset, 0) + local[0], num(t.data.yOffset, 0) + local[1]]); dirA = t.heading + angle; }
    else { world = this.local2world(rot(m, 0)); dirA = this.heading + angle; }
    const n = clamp(num(b.numBullets, 1), 1, 10);
    for (let k = 0; k < n; k++) {
      const spread = (num(b.spreadMultiplier, 1) * 0.08) * (Math.random() - 0.5) * (n > 1 ? 3 : 1);
      this._spawn(proj, b, world, dirA + spread, 1);
    }
    // recoil on the tank, opposite to the barrel
    const rec = num(b.recoilMultiplier, 1) * 28;
    this.vel[0] -= Math.cos(dirA) * rec; this.vel[1] -= Math.sin(dirA) * rec;
  };
  Live.prototype._spawn = function (proj, b, world, dirA, parentR) {
    const tank = this.tank;
    const hm = num(b.heightMultiplier, 1), sm = hi(num(b.bulletSizeMultiplier, 1));
    const sides = proj.sides === undefined ? -1 : proj.sides | 0;
    // a tank barrel's shot has radius 21 x width x size; a sub-barrel's is the parent's x size / 2
    const r = parentR === 1 ? 21 * hm * sm : parentR * sm / 2;
    void sides;
    const pseudo = projectileAsTank(proj, this.model.team);
    const built = build(pseudo, { team: this.model.team });
    const g = el('g', { class: 'shot' }, this.world);
    g.appendChild(built.root);
    const cruise = 210 * hi(num(b.speedMultiplier, 1)), launch = 210 * hi(num(b.initialVelocityMultiplier, 1));
    const shot = { el: g, pos: world.slice(), dir: [Math.cos(dirA), Math.sin(dirA)], cruise, launch, life: hi(num(b.lifetime, 3)), age: 0,
      r, ang: dirA, spin: num(proj.spin, 0), proj, built };
    this.shots.push(shot);
    g.setAttribute('transform', `translate(${fmt(world[0])} ${fmt(world[1])}) rotate(${fmt(deg(dirA))}) scale(${fmt(r / HULL_R)})`);
    if (this.shots.length > 140) { const old = this.shots.shift(); old.el.remove(); }
    return shot;
  };
  Live.prototype._expire = function (s) {
    s.el.remove();
    const proj = s.proj, burst = proj.burst || {};
    if (burst.onExpire && proj.barrels) {
      for (const sb of proj.barrels) {
        if (!(sb.flags && sb.flags.firesOnDeath)) continue;
        const child = (this.tank.projectiles || [])[num(sb.projectile, -1)]; if (!child) continue;
        const world = [s.pos[0] + s.dir[0] * num(sb.startDistance, 0) * (s.r / HULL_R), s.pos[1] + s.dir[1] * num(sb.startDistance, 0) * (s.r / HULL_R)];
        this._spawn(child, sb, world, s.ang + num(sb.angle, 0), s.r);
      }
    }
  };

  global.DiepTank = { PALETTE, COLOR_NAMES, TEAM_HEX, build, projectileAsTank, bbox, Live, deg, rad, fillOf, strokeOf, polyPoints, el, filled, fmt, fmtPts, num, partName };
})(window);
