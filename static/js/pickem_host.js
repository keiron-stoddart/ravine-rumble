(function () {
    const POLL_MS = 1200;

    const statusBadge = document.getElementById('status-badge');
    const weekInput = document.getElementById('week-input');
    const locksInput = document.getElementById('locks-input');
    const hostError = document.getElementById('host-error');
    const hostWeekLabel = document.getElementById('host-week-label');
    const hostMatchups = document.getElementById('host-matchups');
    const pickerFraction = document.getElementById('picker-fraction');
    const pickerNames = document.getElementById('picker-names');
    const hostLeaderboard = document.getElementById('host-leaderboard');
    const joinUrl = document.getElementById('join-url');

    joinUrl.textContent = `${window.location.origin}/pickem`;

    const STATUSES = {
        open: ['Open', 'bg-success'],
        locked: ['Locked', 'bg-warning text-dark'],
        scored: ['Scored', 'bg-primary'],
    };

    let rendered = null;

    function title(n) {
        return n ? n.charAt(0) + n.slice(1).toLowerCase() : n;
    }

    document.querySelectorAll('[data-action]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;
            const week = parseInt(weekInput.value, 10);
            if (!week) return;
            if (action === 'reset' && !window.confirm(`Reset week ${week} and erase its picks?`)) return;

            const body = { action, week };
            if (action === 'open' && locksInput.value) body.locks_at = locksInput.value;

            show(hostError, false);
            btn.disabled = true;
            fetch('/pickem/host/action', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            })
                .then((res) => res.json().then((data) => ({ ok: res.ok, data })))
                .then(({ ok, data }) => {
                    if (!ok || !data.ok) {
                        hostError.textContent = (data && data.error) || 'Action failed.';
                        show(hostError, true);
                    }
                    poll();
                })
                .catch(() => {})
                .finally(() => { btn.disabled = false; });
        });
    });

    function show(el, visible) {
        el.classList.toggle('d-none', !visible);
    }

    function renderMatchups(state) {
        hostMatchups.innerHTML = '';
        if (!state.matchups || !state.matchups.length) {
            hostWeekLabel.textContent = 'No week open.';
            return;
        }
        hostWeekLabel.textContent = `Week ${state.week} — ${state.matchups.length} matchups`;
        state.matchups.forEach((m) => {
            const card = document.createElement('div');
            card.className = 'host-matchup';
            [['away', m.away, m.away_prob], ['home', m.home, m.home_prob]].forEach(([side, tname, prob]) => {
                const row = document.createElement('div');
                row.className = 'team-row';
                if (m.winner && (tname === m.winner || m.winner === 'TIE')) row.classList.add('is-winner');
                const left = document.createElement('span');
                left.textContent = (side === 'away' ? '' : 'at ') + title(tname);
                const right = document.createElement('span');
                right.className = 'prob';
                right.textContent = prob != null ? `${Math.round(prob * 100)}%` : '';
                row.appendChild(left);
                row.appendChild(right);
                card.appendChild(row);
            });
            if (m.winner) {
                const w = document.createElement('div');
                w.className = 'small text-success mt-1';
                w.textContent = m.winner === 'TIE' ? 'Tie' : `Winner: ${title(m.winner)}`;
                card.appendChild(w);
            }
            hostMatchups.appendChild(card);
        });
    }

    function renderLeaderboard(board) {
        hostLeaderboard.innerHTML = '';
        if (!board || !board.length) {
            const li = document.createElement('li');
            li.className = 'list-group-item text-muted border-0 px-0';
            li.textContent = 'No scored weeks yet.';
            hostLeaderboard.appendChild(li);
            return;
        }
        board.forEach((row) => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center px-0';
            li.appendChild(document.createTextNode(title(row.name)));
            const badge = document.createElement('span');
            badge.className = 'badge bg-secondary rounded-pill';
            badge.textContent = row.points;
            li.appendChild(badge);
            hostLeaderboard.appendChild(li);
        });
    }

    function setButtons(status) {
        const enabled = {
            open: status !== 'open' && status !== 'locked',
            lock: status === 'open',
            score: status === 'locked' || status === 'open',
            reset: !!status,
        };
        document.querySelectorAll('[data-action]').forEach((btn) => {
            btn.disabled = !enabled[btn.dataset.action];
        });
    }

    function render(state) {
        const status = state.stored_status || (state.matchups ? state.status : null);
        const [label, cls] = STATUSES[status] || ['No week', 'bg-secondary'];
        statusBadge.className = `badge ${cls}`;
        statusBadge.textContent = label;
        setButtons(status);

        renderMatchups(state);

        const pickers = state.pickers || [];
        pickerFraction.textContent = state.matchups && state.matchups.length
            ? `${state.picker_count || 0}/${state.player_count || 0}`
            : '—';
        pickerNames.textContent = pickers.length ? pickers.map(title).join(', ') : 'Nobody yet';

        renderLeaderboard(state.leaderboard);
    }

    function poll() {
        fetch('/pickem/host/state')
            .then((res) => (res.ok ? res.json() : null))
            .then((state) => {
                if (!state) return;
                const key = JSON.stringify(state);
                if (key === rendered) return;
                rendered = key;
                render(state);
            })
            .catch(() => {});
    }

    poll();
    setInterval(poll, POLL_MS);
})();
