(function () {
    const yearFilter = document.getElementById('year-filter');
    const table = document.getElementById('season-results-table');
    if (!yearFilter || !table) return;

    const rows = table.querySelectorAll('tbody tr');

    function applyFilter() {
        const year = yearFilter.value;
        rows.forEach((row) => {
            row.classList.toggle('d-none', year !== 'all' && row.dataset.year !== year);
        });
    }

    yearFilter.addEventListener('change', applyFilter);
    applyFilter();

    const headers = table.querySelectorAll('th.sortable');
    let currentSort = { index: null, dir: 1 };

    headers.forEach((th, index) => {
        th.addEventListener('click', () => {
            const dir = currentSort.index === index ? -currentSort.dir : 1;
            currentSort = { index, dir };

            headers.forEach((h) => h.classList.remove('sorted-asc', 'sorted-desc'));
            th.classList.add(dir === 1 ? 'sorted-asc' : 'sorted-desc');

            const tbody = table.querySelector('tbody');
            const sortedRows = Array.from(tbody.querySelectorAll('tr')).sort((a, b) => {
                const aVal = a.children[index].dataset.sort;
                const bVal = b.children[index].dataset.sort;
                const aNum = parseFloat(aVal);
                const bNum = parseFloat(bVal);
                const bothNumeric = !isNaN(aNum) && !isNaN(bNum);
                const cmp = bothNumeric ? aNum - bNum : aVal.localeCompare(bVal);
                return cmp * dir;
            });

            sortedRows.forEach((row) => tbody.appendChild(row));
        });
    });
})();
