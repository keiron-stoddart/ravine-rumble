(function () {
    const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];
    const POLL_MS = 1200;

    const phaseBadge = document.getElementById('phase-badge');
    const hostProgress = document.getElementById('host-progress');
    const hostQuestion = document.getElementById('host-question');
    const hostOptions = document.getElementById('host-options');
    const hostNote = document.getElementById('host-note');
    const answeredFraction = document.getElementById('answered-fraction');
    const answeredNames = document.getElementById('answered-names');
    const hostScores = document.getElementById('host-scores');
    const joinUrl = document.getElementById('join-url');

    joinUrl.textContent = `${window.location.origin}/trivia`;

    const PHASES = {
        lobby: ['Waiting to start', 'bg-secondary'],
        question: ['Question open', 'bg-success'],
        revealed: ['Answer revealed', 'bg-primary'],
        finished: ['Finished', 'bg-dark'],
    };

    let rendered = null;

    document.querySelectorAll('[data-action]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;
            if (action === 'reset' && !window.confirm('Reset the game and erase all answers?')) return;
            fetch('/trivia/host/action', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action }),
            })
                .then(poll)
                .catch(() => {});
        });
    });

    function setButtons(phase) {
        const enabled = {
            start: phase === 'lobby',
            reveal: phase === 'question',
            next: phase === 'revealed',
            reset: true,
        };
        document.querySelectorAll('[data-action]').forEach((btn) => {
            btn.disabled = !enabled[btn.dataset.action];
        });
    }

    function renderOptions(state) {
        hostOptions.innerHTML = '';
        if (!state.question) return;

        state.question.options.forEach((label, i) => {
            const row = document.createElement('div');
            row.className = 'host-option';
            // The host screen always marks the answer so you know it before
            // revealing; players never receive it until the reveal.
            if (i === state.correct) row.classList.add('is-correct');

            const left = document.createElement('span');
            const letter = document.createElement('span');
            letter.className = 'letter';
            letter.textContent = LETTERS[i];
            left.appendChild(letter);
            left.appendChild(document.createTextNode(label));

            const count = document.createElement('span');
            count.className = 'count';
            if (state.phase === 'revealed' && state.tally) {
                const n = state.tally[i];
                count.textContent = n === 1 ? '1 pick' : `${n} picks`;
            }

            row.appendChild(left);
            row.appendChild(count);
            hostOptions.appendChild(row);
        });
    }

    function renderScores(scores) {
        hostScores.innerHTML = '';
        if (!scores || !scores.length) {
            const li = document.createElement('li');
            li.className = 'list-group-item text-muted border-0 px-0';
            li.textContent = 'No answers yet.';
            hostScores.appendChild(li);
            return;
        }
        scores.forEach((row) => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center px-0';
            li.appendChild(document.createTextNode(row.name.charAt(0) + row.name.slice(1).toLowerCase()));
            const badge = document.createElement('span');
            badge.className = 'badge bg-secondary rounded-pill';
            badge.textContent = row.score;
            li.appendChild(badge);
            hostScores.appendChild(li);
        });
    }

    function render(state) {
        const [label, cls] = PHASES[state.phase] || ['', 'bg-secondary'];
        phaseBadge.className = `badge ${cls}`;
        phaseBadge.textContent = label;
        setButtons(state.phase);

        if (state.phase === 'lobby') {
            hostProgress.textContent = 'Not started';
            hostQuestion.innerHTML = 'Press <strong>Start</strong> when everyone has joined.';
            hostOptions.innerHTML = '';
            hostNote.classList.add('d-none');
            answeredFraction.textContent = '—';
            answeredNames.textContent = '';
        } else if (state.phase === 'finished') {
            hostProgress.textContent = 'Complete';
            hostQuestion.textContent = 'All 10 questions done. Final leaderboard on the right.';
            hostOptions.innerHTML = '';
            hostNote.classList.add('d-none');
            answeredFraction.textContent = '—';
            answeredNames.textContent = '';
        } else {
            hostProgress.textContent = `Question ${state.index + 1} of ${state.total}`;
            hostQuestion.textContent = state.question.text;
            renderOptions(state);

            hostNote.textContent = state.note || '';
            hostNote.classList.toggle('d-none', state.phase !== 'revealed');

            answeredFraction.textContent = `${state.answered_count}/${state.player_count}`;
            const names = (state.answered_by || []).map(
                (n) => n.charAt(0) + n.slice(1).toLowerCase()
            );
            answeredNames.textContent = names.length ? names.join(', ') : 'Nobody yet';
        }

        renderScores(state.scores);
    }

    function poll() {
        fetch('/trivia/host/state')
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
