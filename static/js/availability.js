(function () {
    const NAME_STORAGE_KEY = 'ravine-rumble-name';
    const nameSelect = document.getElementById('name-select');
    const saveBtn = document.getElementById('save-btn');
    const alertBoxes = document.querySelectorAll('.save-alert');

    function allCells() {
        return document.querySelectorAll('.slot-cell');
    }

    function setCellState(cell, available) {
        cell.classList.toggle('selected', available);
        const badge = cell.querySelector('.slot-badge');
        if (badge) {
            const full = badge.querySelector('.label-full');
            const short = badge.querySelector('.label-short');
            if (full) full.textContent = available ? 'Available' : 'Unavailable';
            if (short) short.textContent = available ? 'Free' : 'Busy';
            badge.classList.toggle('bg-success', available);
            badge.classList.toggle('bg-danger', !available);
        }
    }

    // Everything defaults to Available; you click to opt out of blocks you can't do.
    function resetToDefault() {
        allCells().forEach((cell) => setCellState(cell, true));
    }

    function applyMine(data) {
        if (!data || !data.submitted) {
            resetToDefault();
            return;
        }
        const slots = new Set(data.slots || []);
        allCells().forEach((cell) => {
            setCellState(cell, slots.has(cell.dataset.slot));
        });
    }

    function loadMine(name) {
        if (!name) {
            resetToDefault();
            return;
        }
        fetch(`/availability/mine?name=${encodeURIComponent(name)}`)
            .then((res) => (res.ok ? res.json() : null))
            .then(applyMine)
            .catch(() => {});
    }

    function showAlert(message, ok) {
        alertBoxes.forEach((box) => {
            box.textContent = message;
            box.classList.remove('d-none', 'alert-success', 'alert-danger');
            box.classList.add(ok ? 'alert-success' : 'alert-danger');
        });
    }

    if (nameSelect) {
        const stored = localStorage.getItem(NAME_STORAGE_KEY);
        if (stored) {
            nameSelect.value = stored;
            loadMine(stored);
        }

        nameSelect.addEventListener('change', () => {
            const name = nameSelect.value;
            localStorage.setItem(NAME_STORAGE_KEY, name);
            loadMine(name);
        });
    }

    // Click-to-toggle is the primary interaction; a drag-to-paint mouse
    // enhancement is layered on top for desktop users.
    let painting = false;
    let paintValue = true;

    document.addEventListener('mousedown', (e) => {
        const cell = e.target.closest('.slot-cell');
        if (!cell) return;
        painting = true;
        paintValue = !cell.classList.contains('selected');
        setCellState(cell, paintValue);
    });

    document.addEventListener('mouseover', (e) => {
        if (!painting) return;
        const cell = e.target.closest('.slot-cell');
        if (!cell) return;
        setCellState(cell, paintValue);
    });

    document.addEventListener('mouseup', () => {
        painting = false;
    });

    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const name = nameSelect ? nameSelect.value : '';
            if (!name) {
                showAlert('Pick your name first.', false);
                return;
            }

            const body = {
                name,
                slots: Array.from(document.querySelectorAll('.slot-cell.selected')).map(
                    (cell) => cell.dataset.slot
                ),
            };

            fetch('/availability', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            })
                .then((res) => res.json().then((data) => ({ ok: res.ok, data })))
                .then(({ ok, data }) => {
                    if (ok && data.ok) {
                        showAlert('Saved!', true);
                    } else {
                        showAlert(data.error || 'Something went wrong.', false);
                    }
                })
                .catch(() => showAlert('Something went wrong.', false));
        });
    }
})();
