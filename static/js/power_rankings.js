(function () {
    const dataEl = document.getElementById('pr-data');
    const host = document.getElementById('pr-chart');
    const detail = document.getElementById('pr-detail');
    const highlights = document.getElementById('pr-highlights');
    if (!dataEl || !host || !detail) return;

    const data = JSON.parse(dataEl.textContent);
    const SVG_NS = 'http://www.w3.org/2000/svg';
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isDesktop = window.matchMedia('(min-width: 992px)');

    const teams = data.teams.map((t) => ({
        ...t,
        key: t.manager.toLowerCase(),
        entries: t.entries.slice().sort((a, b) => a.week - b.week),
    }));
    const weekNumbers = [...new Set(teams.flatMap((t) => t.entries.map((e) => e.week)))].sort((a, b) => a - b);
    const weekIndex = new Map(weekNumbers.map((w, i) => [w, i]));
    const rankCount = teams.length;

    let selectedKey = null;
    let hoverKey = null;
    let svg = null;
    let groups = new Map();
    let firstDraw = true;

    function el(tag, attrs, text) {
        const node = document.createElementNS(SVG_NS, tag);
        for (const [k, v] of Object.entries(attrs || {})) node.setAttribute(k, v);
        if (text !== undefined) node.textContent = text;
        return node;
    }

    function html(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text !== undefined) node.textContent = text;
        return node;
    }

    function teamByKey(key) {
        return teams.find((t) => t.key === key) || null;
    }

    function latest(team) {
        return team.entries[team.entries.length - 1];
    }

    // ---- chart -------------------------------------------------------------

    function layout() {
        const width = Math.max(host.clientWidth, 280);
        const narrow = width < 520;
        const side = narrow ? 92 : 176;
        const rowH = narrow ? 38 : 44;
        const top = 40;
        const firstY = top + 22;
        return {
            width,
            narrow,
            side,
            top,
            height: firstY + (rankCount - 1) * rowH + 30,
            x: (i) => (weekNumbers.length === 1
                ? width / 2
                : side + (i * (width - 2 * side)) / (weekNumbers.length - 1)),
            y: (rank) => firstY + (rank - 1) * rowH,
        };
    }

    function pathFor(team, L) {
        const pts = team.entries.map((e) => [L.x(weekIndex.get(e.week)), L.y(e.rank)]);
        let d = `M${pts[0][0]},${pts[0][1]}`;
        for (let i = 1; i < pts.length; i++) {
            const [x0, y0] = pts[i - 1];
            const [x1, y1] = pts[i];
            const mid = (x0 + x1) / 2;
            d += ` C${mid},${y0} ${mid},${y1} ${x1},${y1}`;
        }
        return d;
    }

    function ariaLabel(team) {
        const trail = team.entries.map((e) => `week ${e.week} rank ${e.rank}`).join(', ');
        return `${team.manager}, ${team.team}: ${trail}. Show write-ups.`;
    }

    function draw() {
        const L = layout();
        const animate = firstDraw && !reducedMotion;
        host.textContent = '';
        groups = new Map();

        svg = el('svg', {
            viewBox: `0 0 ${L.width} ${L.height}`,
            width: L.width,
            height: L.height,
            role: 'group',
            'aria-label': 'Power rankings by week. Each line is a manager.',
        });
        svg.style.display = 'block';
        svg.style.maxWidth = '100%';

        weekNumbers.forEach((w, i) => {
            const x = L.x(i);
            svg.appendChild(el('line', { class: 'pr-guide', x1: x, x2: x, y1: L.top - 6, y2: L.height - 12 }));
            svg.appendChild(el('text', { class: 'pr-week', x, y: 18 }, `Week ${w}`));
        });

        // Draw in ranking order so keyboard tab order follows the latest rankings.
        const ordered = teams.slice().sort((a, b) => latest(a).rank - latest(b).rank);
        ordered.forEach((team) => {
            const g = el('g', {
                class: 'pr-team',
                tabindex: 0,
                role: 'button',
                'aria-label': ariaLabel(team),
                'aria-pressed': String(team.key === selectedKey),
                'data-key': team.key,
            });
            g.appendChild(el('title', {}, `${team.manager} — ${team.team}`));

            const d = pathFor(team, L);
            g.appendChild(el('path', { class: 'pr-hit', d }));
            const line = el('path', { class: 'pr-line', d, stroke: team.color, 'stroke-width': 4 });
            g.appendChild(line);

            if (animate) {
                const len = line.getTotalLength();
                line.style.strokeDasharray = len;
                line.style.strokeDashoffset = len;
                const delay = (latest(team).rank - 1) * 40;
                line.getBoundingClientRect();
                line.style.transition = `stroke-dashoffset 0.9s ease ${delay}ms, stroke-width 0.2s ease`;
                requestAnimationFrame(() => { line.style.strokeDashoffset = 0; });
            }

            team.entries.forEach((e) => {
                const cx = L.x(weekIndex.get(e.week));
                const cy = L.y(e.rank);
                g.appendChild(el('circle', { cx, cy, r: 13, fill: team.color, stroke: '#fff', 'stroke-width': 2 }));
                g.appendChild(el('text', { class: 'pr-node-label', x: cx, y: cy + 4 }, e.rank));
            });

            addLabel(g, team, team.entries[0], 'end', L.x(weekIndex.get(team.entries[0].week)) - 20, L);
            if (team.entries.length > 1) {
                const last = latest(team);
                addLabel(g, team, last, 'start', L.x(weekIndex.get(last.week)) + 20, L);
            }

            g.addEventListener('click', (ev) => { ev.stopPropagation(); toggle(team.key); });
            g.addEventListener('keydown', (ev) => {
                if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); toggle(team.key); }
            });
            g.addEventListener('pointerenter', () => { hoverKey = team.key; applyState(); });
            g.addEventListener('pointerleave', () => { hoverKey = null; applyState(); });
            g.addEventListener('focus', () => { hoverKey = team.key; applyState(); });
            g.addEventListener('blur', () => { hoverKey = null; applyState(); });

            groups.set(team.key, g);
            svg.appendChild(g);
        });

        svg.addEventListener('click', () => select(null));
        host.appendChild(svg);
        firstDraw = false;
        applyState();
    }

    function addLabel(g, team, entry, anchor, x, L) {
        const y = L.y(entry.rank);
        const name = el('text', { class: 'pr-name', x, y: L.narrow ? y + 4 : y - 1, 'text-anchor': anchor }, team.manager);
        g.appendChild(name);
        if (!L.narrow) {
            g.appendChild(el('text', { class: 'pr-sub', x, y: y + 14, 'text-anchor': anchor }, entry.team || team.team));
        }
    }

    function applyState() {
        if (!svg) return;
        const active = hoverKey || selectedKey;
        host.classList.toggle('is-dimming', Boolean(active));
        groups.forEach((g, key) => {
            g.classList.toggle('is-active', key === active);
            g.setAttribute('aria-pressed', String(key === selectedKey));
        });
    }

    // ---- selection ---------------------------------------------------------

    function toggle(key) {
        select(key === selectedKey ? null : key);
    }

    function select(key) {
        selectedKey = key;
        applyState();
        renderDetail();
        try {
            history.replaceState(null, '', key ? `#${key}` : location.pathname + location.search);
        } catch (e) { /* history API unavailable; selection still works */ }
        if (key && !isDesktop.matches) {
            detail.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
        }
    }

    // ---- detail panel ------------------------------------------------------

    function moveInfo(team, i) {
        if (i === 0) return null;
        const delta = team.entries[i - 1].rank - team.entries[i].rank;
        if (delta > 0) return { cls: 'pr-move-up', text: `▲ ${delta} (from #${team.entries[i - 1].rank})` };
        if (delta < 0) return { cls: 'pr-move-down', text: `▼ ${-delta} (from #${team.entries[i - 1].rank})` };
        return { cls: 'pr-move-flat', text: `— holds at #${team.entries[i].rank}` };
    }

    function renderDetail() {
        detail.textContent = '';
        const team = teamByKey(selectedKey);
        const body = html('div', 'card-body');
        detail.appendChild(body);

        if (!team) {
            const empty = html('div', 'pr-empty');
            empty.appendChild(html('h2', 'h5 text-body', 'Pick a manager'));
            empty.appendChild(html('p', 'mb-0', 'Click a line or name on the chart to read every write-up about them, newest first.'));
            body.appendChild(empty);
            return;
        }

        const head = html('div', 'd-flex justify-content-between align-items-start gap-2 mb-3');
        const title = html('div');
        const h = html('h2', 'h4 mb-0');
        const swatch = html('span', 'pr-swatch');
        swatch.style.backgroundColor = team.color;
        h.appendChild(swatch);
        h.appendChild(document.createTextNode(team.manager));
        title.appendChild(h);
        title.appendChild(html('div', 'text-muted', `${team.team} · ${team.entries.map((e) => '#' + e.rank).join(' → ')}`));
        head.appendChild(title);

        const clear = html('button', 'btn btn-outline-secondary btn-sm flex-shrink-0', 'Clear');
        clear.type = 'button';
        clear.addEventListener('click', () => select(null));
        head.appendChild(clear);
        body.appendChild(head);

        for (let i = team.entries.length - 1; i >= 0; i--) {
            const e = team.entries[i];
            const entry = html('article', 'pr-entry');

            const meta = html('div', 'd-flex flex-wrap align-items-baseline gap-2 mb-1');
            meta.appendChild(html('span', 'badge text-bg-dark', `Week ${e.week}`));
            meta.appendChild(html('span', 'pr-rank', `#${e.rank}`));
            const move = moveInfo(team, i);
            if (move) meta.appendChild(html('span', `fw-semibold ${move.cls}`, move.text));
            entry.appendChild(meta);

            if (e.team && e.team !== team.team) {
                entry.appendChild(html('div', 'small text-muted mb-1', `Then known as ${e.team}`));
            }
            if (e.tagline) entry.appendChild(html('p', 'pr-tagline fw-semibold mb-2', e.tagline));
            e.writeup.split(/\n\n+/).forEach((para) => entry.appendChild(html('p', 'mb-2', para)));
            body.appendChild(entry);
        }

        const foot = html('p', 'small text-muted mt-3 mb-0');
        foot.appendChild(document.createTextNode(`Written by ${data.author}. `));
        const link = html('a', null, 'Original doc');
        link.href = data.source_url;
        link.target = '_blank';
        link.rel = 'noopener';
        foot.appendChild(link);
        body.appendChild(foot);
    }

    // ---- biggest movers ----------------------------------------------------

    function renderHighlights() {
        if (!highlights || weekNumbers.length < 2) return;
        const [prevWeek, lastWeek] = weekNumbers.slice(-2);
        const moves = teams
            .map((t) => {
                const before = t.entries.find((e) => e.week === prevWeek);
                const after = t.entries.find((e) => e.week === lastWeek);
                return before && after ? { team: t, before: before.rank, after: after.rank, delta: before.rank - after.rank } : null;
            })
            .filter(Boolean);
        if (!moves.length) return;

        const chip = (label, sign, picks) => {
            const btn = html('button', 'btn btn-outline-secondary btn-sm pr-highlight');
            btn.type = 'button';
            const strong = html('strong', sign > 0 ? 'pr-move-up' : 'pr-move-down', `${sign > 0 ? '▲' : '▼'} ${label}: `);
            btn.appendChild(strong);
            btn.appendChild(document.createTextNode(
                picks.map((m) => `${m.team.manager} ${m.before}→${m.after}`).join(' & ')
            ));
            btn.addEventListener('click', () => select(picks[0].team.key));
            highlights.appendChild(btn);
        };

        const best = Math.max(...moves.map((m) => m.delta));
        const worst = Math.min(...moves.map((m) => m.delta));
        if (best > 0) chip(`Biggest riser (Week ${lastWeek})`, 1, moves.filter((m) => m.delta === best));
        if (worst < 0) chip(`Biggest faller (Week ${lastWeek})`, -1, moves.filter((m) => m.delta === worst));
    }

    // ---- boot --------------------------------------------------------------

    document.addEventListener('keydown', (ev) => {
        if (ev.key === 'Escape' && selectedKey) select(null);
    });

    let resizeTimer = null;
    let lastWidth = host.clientWidth;
    new ResizeObserver(() => {
        if (host.clientWidth === lastWidth) return;
        lastWidth = host.clientWidth;
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(draw, 120);
    }).observe(host);

    const initial = location.hash.slice(1).toLowerCase();
    if (teamByKey(initial)) selectedKey = initial;

    // Back/forward or a hand-edited hash; our own replaceState calls don't fire this.
    window.addEventListener('hashchange', () => {
        const key = location.hash.slice(1).toLowerCase();
        const next = teamByKey(key) ? key : null;
        if (next === selectedKey) return;
        selectedKey = next;
        applyState();
        renderDetail();
    });

    renderHighlights();
    draw();
    renderDetail();
})();
