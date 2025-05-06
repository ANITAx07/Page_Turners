document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    // Load saved theme or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    body.classList.add(`theme-${savedTheme}`);
    body.classList.add(`text-${savedTheme}`);  // Add text color class
    updateIcon(savedTheme);

    // Toggle theme on button click
    themeToggle.addEventListener('click', () => {
        const currentTheme = body.classList.contains('theme-dark') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        // Switch theme and text color
        body.classList.remove(`theme-${currentTheme}`);
        body.classList.remove(`text-${currentTheme}`);
        body.classList.add(`theme-${newTheme}`);
        body.classList.add(`text-${newTheme}`);
        
        localStorage.setItem('theme', newTheme);
        updateIcon(newTheme);
    });

    // Update theme icon
    function updateIcon(theme) {
        if (theme === 'dark') {
            themeToggle.src = '/static/images/light_mode.png'; // Light mode icon for dark theme
            themeToggle.alt = 'Light Mode';
        } else {
            themeToggle.src = '/static/images/moon_icon.png'; // Dark mode icon for light theme
            themeToggle.alt = 'Dark Mode';
        }
    }
});
