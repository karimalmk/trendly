import { handleOverlay } from "../../../../static/js/helpers.js";

/* ===================================
    PROFILE BUTTON HANDLER
=================================== */

const profileButton = document.querySelector("#profile");

document.addEventListener("click", (event) => {
  if (event.target === profileButton) {
    console.log("profile button clicked");
    const profileOverlay = document.querySelector(".logout-container");
    handleOverlay(event, profileOverlay);
  }
});


// ===================================
// THEME TOGGLE HANDLER (stable)
// ===================================

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".theme-input");
  const label = document.querySelector(".theme-label");
  if (!toggle) return;

  // Disable transitions during sync to prevent flicker
  document.documentElement.classList.add("disable-transitions");

  // Read the theme applied early
  const currentTheme = document.documentElement.getAttribute("data-theme");
  toggle.checked = currentTheme === "dark";
  if (label) label.textContent = toggle.checked ? "Dark Mode" : "Light Mode";

  // Re-enable transitions shortly after load
  requestAnimationFrame(() => {
    document.documentElement.classList.remove("disable-transitions");
  });

  // Handle user toggle
  toggle.addEventListener("change", () => {
    const isDark = toggle.checked;
    const newTheme = isDark ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);

    if (label) label.textContent = isDark ? "Dark Mode" : "Light Mode";
  });
});