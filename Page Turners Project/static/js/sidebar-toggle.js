document.addEventListener("DOMContentLoaded", function () {
    const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";  // Example, replace with your login check
    const userRole = localStorage.getItem("userRole"); // Assume 'userRole' is stored as 'admin' or 'user'

    const registerLink = document.getElementById("register-link");
    const userProfileLink = document.getElementById("user-profile-link");
    const logoutLink = document.getElementById("logout-link");
    const adminPanelLink = document.getElementById("admin-panel-link");

    if (isLoggedIn) {
        // Show User Profile and Logout, Hide Register
        userProfileLink.style.display = "block";
        logoutLink.style.display = "block";
        registerLink.style.display = "none";

        // Show Admin Panel only for Admins
        if (userRole === "admin") {
            adminPanelLink.style.display = "block";
        } else {
            adminPanelLink.style.display = "none";
        }
    } else {
        // Show Register, Hide User Profile, Logout, and Admin Panel
        userProfileLink.style.display = "none";
        logoutLink.style.display = "none";
        registerLink.style.display = "block";
        adminPanelLink.style.display = "none";
    }

    // Add a logout function if you need to log out the user
    logoutLink.addEventListener("click", function () {
        // Clear login status and user role from localStorage or session
        localStorage.setItem("isLoggedIn", "false");
        localStorage.removeItem("userRole");
        
        // Reload the page or redirect to home
        window.location.href = "/";
    });
});
