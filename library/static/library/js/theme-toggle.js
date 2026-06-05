(function () {
    var STORAGE_KEY = "e_blioteka_theme";

    function applyTheme(theme) {
        var body = document.body;
        if (!body) return;
        body.classList.toggle("theme-dark", theme === "dark");
        body.classList.toggle("theme-light", theme !== "dark");
    }

    function getPreferredTheme() {
        var saved = localStorage.getItem(STORAGE_KEY);
        if (saved === "dark" || saved === "light") return saved;
        return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }

    function animateTransition(nextTheme) {
        var body = document.body;
        if (!body) return;
        body.classList.add("theme-animating");
        window.setTimeout(function () {
            applyTheme(nextTheme);
        }, 180);
        window.setTimeout(function () {
            body.classList.remove("theme-animating");
        }, 460);
    }

    function toggleTheme() {
        var nextTheme = document.body.classList.contains("theme-dark") ? "light" : "dark";
        localStorage.setItem(STORAGE_KEY, nextTheme);
        animateTransition(nextTheme);
    }

    document.addEventListener("DOMContentLoaded", function () {
        applyTheme(getPreferredTheme());
        var button = document.getElementById("theme-toggle");
        if (button) {
            button.addEventListener("click", toggleTheme);
        }
    });
})();
