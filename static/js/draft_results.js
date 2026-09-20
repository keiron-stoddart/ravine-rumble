(function () {
    const rows = Array.from(document.querySelectorAll('.dr-row'));
    if (!rows.length) return;

    let hovered = null;
    let pinned = null;

    function apply() {
        const linked = hovered || pinned;
        rows.forEach((row) => {
            row.classList.toggle('is-linked', linked !== null && row.dataset.team === linked);
            row.classList.toggle('is-pinned', pinned !== null && row.dataset.team === pinned);
        });
    }

    function togglePin(team) {
        pinned = pinned === team ? null : team;
        apply();
    }

    rows.forEach((row) => {
        const team = row.dataset.team;
        row.addEventListener('pointerenter', () => { hovered = team; apply(); });
        row.addEventListener('pointerleave', () => { hovered = null; apply(); });
        row.addEventListener('focus', () => { hovered = team; apply(); });
        row.addEventListener('blur', () => { hovered = null; apply(); });
        row.addEventListener('click', () => togglePin(team));
        row.addEventListener('keydown', (ev) => {
            if (ev.key === 'Enter' || ev.key === ' ') {
                ev.preventDefault();
                togglePin(team);
            }
        });
    });
})();
