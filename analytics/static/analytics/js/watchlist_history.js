// -------------------- TO DO: MANUAL URL ROUTING --------------------

// -------------------- PUSHSTATE HANDLER --------------------
document.addEventListener("click", (event) => {
  const target = event.target;

  if (target.matches(".watchlist-name")) {
    const watchlistName = target.value.trim();
    const watchlistId = target.id;
    history.pushState({ "page": "dashboard/watchlist", watchlistName, watchlistId }, "", `?name=${watchlistName}`); // second argument is title, which we leave empty
  }

  if (event.target.id === "view-all-watchlists") {
    history.pushState({ "page": "dashboard/all-watchlists" }, "/dashboard/all-watchlists");
  }

  if (event.target.id === "create-watchlist") {
    history.pushState({ "page": "dashboard/create-watchlist" }, "/dashboard/create-watchlist");
  }
});


// -------------------- POPSTATE HANDLER --------------------
window.addEventListener("popstate", (event) => {
  const state = event.state;
  if (!state) return;

  switch (state.page) {
    // Handle different watchlist pages
    case "dashboard/watchlist":
      console.log("Popstate event:", state);
      const targetElement = document.getElementById(state.watchlistId);
      targetElement.click();
      break;
    // Handle all watchlists page
    case "dashboard/all-watchlists":
      document.getElementById("view-all-watchlists").click();
      break;
    // Handle create watchlist page
    case "dashboard/create-watchlist":
      document.getElementById("create-watchlist").click();
      break;
    default:
      console.log("Unknown state:", state);
  }
});