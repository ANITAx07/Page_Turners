document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-bar");

    // Function to filter books or authors based on the query
    function filterItems(query, itemSelector) {
        let lowerQuery = query.toLowerCase();
        const items = document.querySelectorAll(itemSelector);  // Select either book cards or author cards

        items.forEach(item => {
            // For books, search for <h3> (title) and <h4> (author)
            // For authors, search for <h2> (name) and <p> (bio)
            let title = item.querySelector("h3") ? item.querySelector("h3").textContent.toLowerCase() : '';
            let author = item.querySelector("h4") ? item.querySelector("h4").textContent.toLowerCase() : '';
            let name = item.querySelector("h2") ? item.querySelector("h2").textContent.toLowerCase() : '';
            let bio = item.querySelector("p") ? item.querySelector("p").textContent.toLowerCase() : '';

            // Check if either title/author (for books) or name/bio (for authors) matches the search query
            if (title.includes(lowerQuery) || author.includes(lowerQuery) || name.includes(lowerQuery) || bio.includes(lowerQuery)) {
                item.style.display = "block";
            } else {
                item.style.display = "none";
            }
        });
    }

    // Event listener for search input
    searchInput.addEventListener("input", function () {
        let query = searchInput.value.trim();
        
        // First, try to search in the books section (adjust selector as needed)
        filterItems(query, ".tiles article");  // Assuming books are in .tiles article tags

        // Then, search in the authors section (adjust selector as needed)
        filterItems(query, ".author-card");  // Assuming authors have .author-card class
    });
});
