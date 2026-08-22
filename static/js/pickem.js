(function () {
    const NAME_KEY = 'ravine-rumble-name';
    const POLL_MS = 1500;

    const nameSelect = document.getElementById('name-select');
    const needsName = document.getElementById('needs-name');
    const stage = document.getElementById('stage');
    const waiting = document.getElementById('waiting');
    const weekLabel = document.getElementById('week-label');
    const pickerCount = document.getElementById('picker-count');
    const lockBanner = document.getElementById('lock-banner');
    const matchupsBox = document.getElementById('matchups');
    const feedback = document.getElementById('feedback');
    const leaderboardWrap = document.getElementById('leaderboard-wrap');
    const leaderboardList = document.getElementById('leaderboard-list');

    let name = localStorage.getItem(NAME_KEY) || '';
    // Tracks the taps we've sent but not yet seen echoed back, so a 1.5s poll
    // doesn't wipe out a pick the player just made. Keyed by matchup id.
    let pending = {};
    // Structural signature of the drawn cards; we only rebuild the DOM when it
    // changes so a poll never re-renders the buttons under the player's finger.
    let renderedKey = null;

    if (name) nameSelect.value = name;
    if (nameSelect.value !== name) name = '';

    nameSelect.addEventListener('change', () => {
        name = nameSelect.value;
        localStorage.setItem(NAME_KEY, name);
        pending = {};
        renderedKey = null;
        poll();
    });

    function show(el, visible) {
        el.classList.toggle('d-none', !visible);
    }

    function title(n) {
        return n ? n.charAt(0) + n.slice(1).toLowerCase() : n;
    }

    function submit(week, mid, pick) {
        pending[mid] = pick;
        paintSelection(mid, pick);
        fetch('/pickem/pick', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, week, matchup_id: mid, pick }),
        })
            .then((res) => res.json().then((data) => ({ ok: res.ok, data })))
            .then(({ ok, data }) => {
                if (!ok || !data.ok) {
                    delete pending[mid];
                    feedback.textContent = (data && data.error) || 'Could not save that pick.';
                    feedback.className = 'alert alert-warning';
                    show(feedback, true);
                    poll();
                }
            })
            .catch(() => {
                delete pending[mid];
            });
    }

    function paintSelection(mid, pick) {
        matchupsBox
            .querySelectorAll(`button[data-mid="${mid}"]`)
            .forEach((btn) => {
                const chosen = btn.dataset.team === pick;
                btn.classList.toggle('btn-primary', chosen);
                btn.classList.toggle('btn-outline-secondary', !chosen);
            });
    }

    function teamButton(week, mid, teamName, prob, side) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-outline-secondary pick-btn';
        btn.dataset.mid = mid;
        btn.dataset.team = teamName;
        btn.dataset.side = side;
        const label = document.createElement('span');
        label.textContent = title(teamName);
        const p = document.createElement('span');
        p.className = 'prob';
        p.textContent = prob != null ? `${Math.round(prob * 100)}%` : '';
        btn.appendChild(label);
        btn.appendChild(p);
        btn.addEventListener('click', () => {
            if (btn.disabled) return;
            submit(week, mid, teamName);
        });
        return btn;
    }

    function buildCards(state) {
        matchupsBox.innerHTML = '';
        state.matchups.forEach((m) => {
            const card = document.createElement('div');
            card.className = 'matchup-card';
            card.dataset.mid = m.id;
            card.appendChild(teamButton(state.week, m.id, m.away, m.away_prob, 'away'));
            const vs = document.createElement('div');
            vs.className = 'vs-label';
            vs.textContent = 'at';
            card.appendChild(vs);
            card.appendChild(teamButton(state.week, m.id, m.home, m.home_prob, 'home'));
            matchupsBox.appendChild(card);
        });
    }

    function decorate(state) {
        const open = state.status === 'open';
        const scored = state.status === 'scored';
        state.matchups.forEach((m) => {
            const chosen = pending[m.id] || (state.my_picks || {})[m.id];
            matchupsBox
                .querySelectorAll(`button[data-mid="${m.id}"]`)
                .forEach((btn) => {
                    const team = btn.dataset.team;
                    btn.disabled = !open;
                    btn.classList.remove('btn-primary', 'btn-outline-secondary', 'btn-success', 'btn-danger');
                    if (scored && m.winner) {
                        if (team === m.winner || m.winner === 'TIE') {
                            btn.classList.add('btn-success');
                        } else if (team === chosen) {
                            btn.classList.add('btn-danger');
                        } else {
                            btn.classList.add('btn-outline-secondary');
                        }
                    } else if (team === chosen) {
                        btn.classList.add('btn-primary');
                    } else {
                        btn.classList.add('btn-outline-secondary');
                    }
                });
            const card = matchupsBox.querySelector(`.matchup-card[data-mid="${m.id}"]`);
            if (card) {
                const won = scored && chosen && m.winner && (chosen === m.winner || m.winner === 'TIE');
                card.classList.toggle('is-win', !!won);
            }
        });
    }

    function renderLockBanner(state) {
        if (state.status === 'open') {
            if (state.locks_at) {
                lockBanner.textContent = `Picks lock at ${state.locks_at.replace('T', ' ')}.`;
                show(lockBanner, true);
            } else {
                show(lockBanner, false);
            }
        } else if (state.status === 'locked') {
            lockBanner.textContent = 'Picks are locked for this week.';
            show(lockBanner, true);
        } else if (state.status === 'scored') {
            lockBanner.textContent = 'This week is scored. See how you did below.';
            show(lockBanner, true);
        } else {
            show(lockBanner, false);
        }
    }

    function renderLeaderboard(state) {
        const board = state.leaderboard || [];
        if (!board.length) {
            show(leaderboardWrap, false);
            return;
        }
        leaderboardList.innerHTML = '';
        const myWeek = {};
        (state.week_score || []).forEach((r) => { myWeek[r.name] = r; });
        board.forEach((row) => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            if (row.name === name) li.classList.add('fw-bold');
            const left = document.createElement('span');
            left.textContent = title(row.name);
            const meta = document.createElement('small');
            meta.className = 'text-muted ms-2';
            meta.textContent = `${row.correct} correct · ${row.weeks} wk`;
            left.appendChild(meta);
            li.appendChild(left);
            const badge = document.createElement('span');
            badge.className = 'badge bg-secondary rounded-pill';
            badge.textContent = row.points;
            li.appendChild(badge);
            leaderboardList.appendChild(li);
        });
        show(leaderboardWrap, true);
    }

    function render(state) {
        show(needsName, !name);
        if (!name) {
            show(stage, false);
            show(waiting, false);
            return;
        }

        if (!state.matchups || state.week == null) {
            show(stage, false);
            show(waiting, true);
            renderedKey = null;
            return;
        }

        show(waiting, false);
        show(stage, true);

        weekLabel.textContent = `Week ${state.week}`;
        pickerCount.textContent = `${state.picker_count}/${state.player_count} playing`;

        const key = `${state.week}|${state.status}|${state.matchups.map((m) => m.id).join(',')}`;
        if (key !== renderedKey) {
            buildCards(state);
            renderedKey = key;
            if (state.status === 'open') { show(feedback, false); }
        }
        // Drop stale optimistic picks once the server confirms them.
        Object.keys(pending).forEach((mid) => {
            if ((state.my_picks || {})[mid] === pending[mid]) delete pending[mid];
        });
        decorate(state);
        renderLockBanner(state);
        renderLeaderboard(state);
    }

    function poll() {
        const url = name ? `/pickem/state?name=${encodeURIComponent(name)}` : '/pickem/state';
        fetch(url)
            .then((res) => (res.ok ? res.json() : null))
            .then((state) => state && render(state))
            .catch(() => {});
    }

    poll();
    setInterval(poll, POLL_MS);
})();
