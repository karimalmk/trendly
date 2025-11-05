// ============================================================
// FORMATTING HELPERS
// ============================================================

// -------------------- FORMAT USD --------------------
export function formatUSD(value) {
  if (value == null || isNaN(value)) return "";
  return value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
  });
}

// -------------------- FORMAT COMMA --------------------
export function formatComma(value, decimals = 2) {
  if (value == null || isNaN(value)) return "";
  return Number(value).toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

// -------------------- FORMAT INTEGER WITH COMMAS --------------------
export function formatIntegerComma(value) {
  if (value == null || isNaN(value)) return "";
  return Math.round(value).toLocaleString("en-US");
}

// -------------------- FORMAT PERCENT --------------------
export function formatPercent(value, decimals = 2) {
  if (value == null || isNaN(value)) return "";
  return (value * 100).toFixed(decimals) + "%";
}


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
