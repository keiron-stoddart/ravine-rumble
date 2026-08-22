(function () {
    const yearFilter = document.getElementById('year-filter');
    const tableEl = document.getElementById('season-results-table');
    if (!yearFilter || !tableEl || !window.simpleDatatables) return;

    const dataTable = new simpleDatatables.DataTable(tableEl, {
        perPage: 25,
        perPageSelect: [10, 25, 50, ["All", 0]],
        // Only the plain numeric columns need a type. Text columns are left
        // as the default 'html' so cell markup (the truncating span on Team)
        // survives rendering, and columns 3, 4, 7 and 9 carry a data-order
        // attribute that overrides type-based sorting anyway.
        columns: [
            { select: [0, 5, 6, 10], type: 'number' },
        ],
    });

    function applyYearFilter() {
        const year = yearFilter.value;
        dataTable.search(year === 'all' ? '' : year, [0]);
    }

    yearFilter.addEventListener('change', applyYearFilter);
    applyYearFilter();
})();
