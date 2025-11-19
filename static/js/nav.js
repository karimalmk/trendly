// ============================================================
// CSRF TOKEN FETCHER
// ============================================================

export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// ============================================================
// SET OVERLAY COORDINATES
// ============================================================

export function setCoordinates(overlay, element, parent, xOffset, yOffset) {
  const rect = element.getBoundingClientRect();
  const parentRect = parent.getBoundingClientRect();

  const leftPercent = ((rect.left - parentRect.left + xOffset) / parentRect.width) * 100;
  const topPercent = ((rect.bottom - parentRect.top + yOffset) / parentRect.height) * 100;

  overlay.style.left = `${leftPercent}%`;
    overlay.style.top = `${topPercent}%`;

}

// ============================================================
// HANDLE OVERLAY TOGGLE
// ============================================================

export function handleOverlay(event, overlay) {
  event.stopPropagation();
  const isProfileOverlay = overlay.classList.contains("logout-container");
  const backdrop = document.querySelector("#overlay-backdrop");

  // Close other overlays
  document.querySelectorAll(".overlay").forEach((ov) => {
    if (ov !== overlay) ov.style.display = "none";
  });

  // Toggle visibility
  const isVisible = overlay.style.display === "flex";
  overlay.style.display = isVisible ? "none" : "flex";

  // Backdrop toggle only for profile overlay
  if (isProfileOverlay) {
    backdrop.classList.toggle("active", !isVisible);
  }

  // Handle close button if present
  const closeBtn = overlay.querySelector(".close-button");
  if (closeBtn) {
    closeBtn.onclick = () => {
      overlay.style.display = "none";
      if (isProfileOverlay) backdrop.classList.remove("active");
      console.log("Overlay closed via close button");
    };
  }

  // Remove previous outside-click listener
  if (document.overlayOutsideHandler) {
    document.removeEventListener("click", document.overlayOutsideHandler);
  }

  // Define new outside-click handler
  document.overlayOutsideHandler = (e) => {
    const inside = overlay.contains(e.target);
    if (!inside && overlay.style.display === "flex") {
      overlay.style.display = "none";
      if (isProfileOverlay) backdrop.classList.remove("active");
      console.log("Overlay closed via outside click");
    }
  };

  // Add listener only when just opened
  if (!isVisible) {
    setTimeout(() => {
      document.addEventListener("click", document.overlayOutsideHandler);
    }, 0);
  }
}

/* ===================================
    HANDLE EXPANDABLE SECTION
=================================== */

export function handleExpand(e, element) {
  // Stop any nested click bubbling, just in case
  e.stopPropagation();

  // Toggle between flex and none
  if (element.style.display === "flex") {
    element.style.display = "none";
  } else {
    element.style.display = "flex";
  }
}

/* ===================================
    PROFILE BUTTON HANDLER
=================================== */

const profileButton = document.querySelector("#profile");

document.addEventListener("click", (event) => {
  if (event.target === profileButton) {
    event.preventDefault();
    event.stopImmediatePropagation();
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