(function () {
    const yearFilter = document.getElementById('year-filter');
    if (!yearFilter) return;

    const rows = document.querySelectorAll('#season-results-table tbody tr');

    yearFilter.addEventListener('change', () => {
        const year = yearFilter.value;
        rows.forEach((row) => {
            row.classList.toggle('d-none', year !== 'all' && row.dataset.year !== year);
        });
    });
})();
