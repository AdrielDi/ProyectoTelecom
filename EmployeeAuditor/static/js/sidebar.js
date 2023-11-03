document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("toggle-sidebar-button");
    const sidebar = document.getElementById("sidebar");
    const sidebarMenu = document.getElementById("sidebar-menu");

    toggleButton.addEventListener("click", function () {
        sidebar.classList.toggle("expanded");
        sidebarMenu.classList.toggle("expanded");
    });
});