(function () {
    const yearFilter = document.getElementById('year-filter');
    const tableEl = document.getElementById('season-results-table');
    if (!yearFilter || !tableEl || !window.simpleDatatables) return;

    const dataTable = new simpleDatatables.DataTable(tableEl, {
        perPage: 25,
        perPageSelect: [10, 25, 50, ["All", 0]],
        columns: [
            { select: 0, type: 'number' },
            { select: 1, type: 'string' },
            { select: 2, type: 'string' },
            { select: 3, type: 'number' },
            { select: 4, type: 'string' },
            { select: 5, type: 'number' },
            { select: 6, type: 'number' },
            { select: 7, type: 'number' },
            { select: 8, type: 'string' },
            { select: 9, type: 'string' },
            { select: 10, type: 'number' },
        ],
    });

    function applyYearFilter() {
        const year = yearFilter.value;
        dataTable.search(year === 'all' ? '' : year, [0]);
    }

    yearFilter.addEventListener('change', applyYearFilter);
    applyYearFilter();
})();
