// Dark Mode Toggle
document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById('dark-mode-toggle');
    const currentTheme = localStorage.getItem('theme');

    // Apply saved theme on load
    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }

    // Toggle dark mode and save preference
    toggleButton.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.setItem('theme', 'light');
        }
    });
});

// Table Sorting with Initial Sort Indicator
document.addEventListener("DOMContentLoaded", () => {
    const table = document.querySelector("table");
    const headers = table.querySelectorAll("th");
    let sortOrder = 1; // 1 for ascending, -1 for descending

    // Function to sort table by a specific column
    function sortTableByColumn(columnIndex, initial = false) {
        const rows = Array.from(table.querySelectorAll("tbody tr"));
        const sortedRows = rows.sort((a, b) => {
            const cellA = a.children[columnIndex].innerText;
            const cellB = b.children[columnIndex].innerText;
            return cellA.localeCompare(cellB, undefined, {numeric: true}) * sortOrder;
        });

        // Clear existing rows and re-append sorted rows
        while (table.querySelector("tbody").firstChild) {
            table.querySelector("tbody").removeChild(table.querySelector("tbody").firstChild);
        }
        sortedRows.forEach(row => table.querySelector("tbody").appendChild(row));

        // Update sort order if this is a user-triggered sort
        if (!initial) sortOrder *= -1;

        // Update header indicators
        headers.forEach(h => h.classList.remove("sort-asc", "sort-desc"));
        headers[columnIndex].classList.add(sortOrder === 1 ? "sort-asc" : "sort-desc");
    }

    // Set initial sort on the first column
    sortTableByColumn(0, true);

    // Add click event to each header for sorting
    headers.forEach((header, index) => {
        header.style.cursor = "pointer";
        header.addEventListener("click", () => sortTableByColumn(index));
    });
});

// Image Hover Animation
document.querySelectorAll("img").forEach(image => {
    image.addEventListener("mouseenter", () => {
        image.style.transform = "scale(1.1)";
        image.style.transition = "transform 0.3s ease";
    });

    image.addEventListener("mouseleave", () => {
        image.style.transform = "scale(1)";
    });
});
