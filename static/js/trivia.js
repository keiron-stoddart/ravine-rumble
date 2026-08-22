(function () {
    const NAME_KEY = 'ravine-rumble-name';
    const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];
    const POLL_MS = 1500;

    const nameSelect = document.getElementById('name-select');
    const needsName = document.getElementById('needs-name');
    const stage = document.getElementById('stage');
    const waiting = document.getElementById('waiting');
    const progress = document.getElementById('progress');
    const answeredCount = document.getElementById('answered-count');
    const questionText = document.getElementById('question-text');
    const optionsBox = document.getElementById('options');
    const feedback = document.getElementById('feedback');
    const scoreboard = document.getElementById('scoreboard');
    const scoreboardList = document.getElementById('scoreboard-list');

    let name = localStorage.getItem(NAME_KEY) || '';
    // Tracks what we've drawn so a 1.5s poll doesn't wipe out the tap the
    // player just made, or re-render the buttons underneath their finger.
    let rendered = { phase: null, index: null, choice: null };
    let pending = null;

    if (name) nameSelect.value = name;
    if (nameSelect.value !== name) name = '';

    nameSelect.addEventListener('change', () => {
        name = nameSelect.value;
        localStorage.setItem(NAME_KEY, name);
        rendered = { phase: null, index: null, choice: null };
        poll();
    });

    function show(el, visible) {
        el.classList.toggle('d-none', !visible);
    }

    function submit(index, choice) {
        pending = choice;
        paintChoice(choice);
        fetch('/trivia/answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, index, choice }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (!data.ok) {
                    pending = null;
                    feedback.textContent = data.error || 'Could not save that answer.';
                    feedback.className = 'alert alert-warning mt-3';
                }
            })
            .catch(() => {
                pending = null;
            });
    }

    function paintChoice(choice) {
        optionsBox.querySelectorAll('button').forEach((btn, i) => {
            const chosen = i === choice;
            btn.classList.toggle('btn-primary', chosen);
            btn.classList.toggle('btn-outline-secondary', !chosen);
        });
    }

    function renderQuestion(state) {
        questionText.textContent = state.question.text;
        optionsBox.innerHTML = '';

        state.question.options.forEach((label, i) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-outline-secondary option-btn';
            btn.innerHTML = `<span class="option-letter">${LETTERS[i]}</span>`;
            btn.appendChild(document.createTextNode(label));
            btn.addEventListener('click', () => submit(state.index, i));
            optionsBox.appendChild(btn);
        });
    }

    function renderReveal(state) {
        const mine = pending !== null ? pending : state.my_answer;
        optionsBox.querySelectorAll('button').forEach((btn, i) => {
            btn.disabled = true;
            btn.classList.remove('btn-primary', 'btn-outline-secondary');
            if (i === state.correct) {
                btn.classList.add('btn-success');
            } else if (i === mine) {
                btn.classList.add('btn-danger');
            } else {
                btn.classList.add('btn-outline-secondary');
            }
            if (state.tally) {
                const n = state.tally[i];
                const tag = document.createElement('span');
                tag.className = 'float-end small';
                tag.textContent = n === 1 ? '1 pick' : `${n} picks`;
                btn.appendChild(tag);
            }
        });

        const gotIt = mine === state.correct;
        feedback.className = `alert mt-3 alert-${gotIt ? 'success' : mine === undefined || mine === null ? 'secondary' : 'danger'}`;
        const lead = gotIt ? 'Correct! ' : mine === undefined || mine === null ? 'No answer recorded. ' : 'Not quite. ';
        feedback.textContent = lead + state.note;
        show(feedback, true);
    }

    function renderScores(state) {
        if (!state.scores || !state.scores.length) {
            show(scoreboard, false);
            return;
        }
        scoreboardList.innerHTML = '';
        state.scores.forEach((row) => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            if (row.name === name) li.classList.add('fw-bold');
            li.appendChild(document.createTextNode(row.name.charAt(0) + row.name.slice(1).toLowerCase()));
            const badge = document.createElement('span');
            badge.className = 'badge bg-secondary rounded-pill';
            badge.textContent = row.score;
            li.appendChild(badge);
            scoreboardList.appendChild(li);
        });
        show(scoreboard, true);
    }

    function render(state) {
        show(needsName, !name);
        if (!name) {
            show(stage, false);
            show(waiting, false);
            return;
        }

        if (state.phase === 'lobby') {
            show(stage, false);
            show(waiting, true);
            rendered = { phase: null, index: null, choice: null };
            return;
        }

        show(waiting, false);
        show(stage, true);

        if (state.phase === 'finished') {
            progress.textContent = 'Final results';
            answeredCount.textContent = '';
            questionText.textContent = "That's all 10 — thanks for playing.";
            optionsBox.innerHTML = '';
            show(feedback, false);
            renderScores(state);
            return;
        }

        progress.textContent = `Question ${state.index + 1} of ${state.total}`;
        answeredCount.textContent = `${state.answered_count} answered`;

        const fresh = rendered.index !== state.index || rendered.phase !== state.phase;

        if (state.phase === 'question') {
            if (fresh) {
                if (rendered.index !== state.index) pending = null;
                renderQuestion(state);
                show(feedback, false);
                show(scoreboard, false);
            }
            const mine = pending !== null ? pending : state.my_answer;
            if (mine !== null && mine !== undefined && rendered.choice !== mine) {
                paintChoice(mine);
            }
            rendered = { phase: state.phase, index: state.index, choice: mine };
            return;
        }

        if (state.phase === 'revealed') {
            if (fresh) {
                if (!optionsBox.children.length) renderQuestion(state);
                renderReveal(state);
            }
            renderScores(state);
            rendered = { phase: state.phase, index: state.index, choice: rendered.choice };
        }
    }

    function poll() {
        const url = name ? `/trivia/state?name=${encodeURIComponent(name)}` : '/trivia/state';
        fetch(url)
            .then((res) => (res.ok ? res.json() : null))
            .then((state) => state && render(state))
            .catch(() => {});
    }

    poll();
    setInterval(poll, POLL_MS);
})();
