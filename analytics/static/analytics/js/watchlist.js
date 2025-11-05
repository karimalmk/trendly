import { formatUSD, formatPercent, formatIntegerComma, setCoordinates, handleOverlay } from "./helpers.js";
import {
    fetchWatchlists, fetchWatchlistData, fetchCreateWatchlist, fetchDeleteWatchlist, fetchRenameWatchlist,
    fetchAddStockToWatchlist, fetchRemoveStockFromWatchlist
} from "./watchlist_api.js";

// ============================================================
// HELPER FUNCTIONS
// ============================================================

function highlightButton(activeButton, previousButton) {
    if (previousButton === null) {
        activeButton.classList.add("active-button");
        previousButton = activeButton;
    } else if (activeButton !== previousButton) {
        previousButton.classList.remove("active-button");
        activeButton.classList.add("active-button");
        previousButton = activeButton;
    }
    return previousButton;
}

const scoped = (key) => {
    const userId = document.body.getAttribute("data-user") || "guest";
    return `user_${userId}_${key}`;
};

function addStockRow(quote) {
    return `
    <td class="ticker-cell" colspan="2">${quote[1].ticker}</td>
            <td class="price-cell">${formatUSD(quote[1].price)}</td>
            <td class="change-cell">${formatPercent(quote[1].daily_return)}</td>
            <td class="bid-cell">${formatUSD(quote[1].bid)}</td>
            <td class="ask-cell">${formatUSD(quote[1].ask)}</td>
            <td class="volume-cell">${formatIntegerComma(quote[1].volume)}</td>
            <td style="display: flex; justify-content: center;"><div class="edit-stock-data dot-container"><div class="dots vertical"><span></span><span></span><span></span></div></div></td>`
}

// -------------------- ADD STOCK HTML --------------------
function addStock() {
    return `
    <p id="add-stock-feedback"></p>
    <div class="button-group">
      <input type="text" id="add-stock-input" placeholder="Enter ticker" />
      <button id="add-stock-button">Add</button>
      <button id="clear-add-stock">Clear</button>
      <button id="close-add-stock">Done</button>
    </div>
  `;
}

// -------------------- CONFIRM DELETE WATCHLIST --------------------
async function deleteWatchlist(confirmationOverlay) {
    confirmationOverlay.querySelectorAll(".confirm-delete-button").forEach((button) => {
        button.onclick = async () => {
            const { id } = AppState.getActiveWatchlist();
            const response = await fetchDeleteWatchlist(id);
            if (response.ok) {
                window.location.reload();
                AppState.removeActiveWatchlist();
                AppState.setActivePage("editWatchlist");
            } else {
                console.error("Failed to delete watchlist");
            }
        };

        confirmationOverlay.querySelectorAll(".cancel-delete-button").forEach((button) => {
            button.onclick = (event) => {
                handleOverlay(event, confirmationOverlay);
            };
        });
    });
}

// =============================================================
// APP STATE MANAGEMENT
// =============================================================

const AppState = {
    // Save watchlist information in session storage
    setActiveWatchlist(id, name) {
        sessionStorage.setItem(scoped("activeWatchlistId"), id);
        sessionStorage.setItem(scoped("activeWatchlistName"), name);
    },
    getActiveWatchlist() {
        return {
            id: sessionStorage.getItem(scoped("activeWatchlistId")),
            name: sessionStorage.getItem(scoped("activeWatchlistName")),
        };
    },
    removeActiveWatchlist() {
        sessionStorage.removeItem(scoped("activeWatchlistId"));
        sessionStorage.removeItem(scoped("activeWatchlistName"));
    },

    // Save current page in session storage
    getActivePage() {
        return sessionStorage.getItem(scoped("activePage"));
    },
    setActivePage(page) {
        sessionStorage.setItem(scoped("activePage"), page);
    },
    // OPTIONS: dataPage, editWatchlist, createWatchlist
};


async function populateWatchlistTable(watchlistId) {
    const response = await fetchWatchlistData(watchlistId);
    const data = await response.json();
    const stockTableBody = document.querySelector("#stock-table-body");
    const metaData = document.querySelector("#meta-data");

    // Clear previous data
    stockTableBody.innerHTML = "";
    metaData.innerHTML = "";

    if (data.quotes.length === 0) {
        const emptyRow = document.createElement("tr");
        emptyRow.innerHTML = `<td colspan="8" style="font-style: italic;">No stocks currently inside this watchlist.</td>`;
        stockTableBody.appendChild(emptyRow);
    } else {
        data.quotes.forEach((quote) => {
            const stockRow = document.createElement("tr");
            stockRow.innerHTML = addStockRow(quote);
            stockTableBody.appendChild(stockRow);
            stockRow.id = quote[0];
        });
    }
    metaData.innerHTML = `
    COUNT : &nbsp; ${data.meta_data.length} <br> LAST MODIFIED : &nbsp; ${data.meta_data.last_modified}`;
}

// =============================================================
// PAGE LOADERS
// =============================================================

export async function loadWatchlistDataPage(watchlistId, watchlistName) {
    document.querySelectorAll(".single-page").forEach(page => page.style.display = "none");
    const name = watchlistName;

    // Clear previous data
    document.querySelector("#stock-table-body").innerHTML = "";
    document.querySelector("#meta-data").innerHTML = "";
    document.querySelector("#watchlist-name").textContent = name;

    // Populate table with new data
    document.querySelector(".watchlist-data-page").style.display = "block";
    await populateWatchlistTable(watchlistId);

    // Save state
    AppState.setActiveWatchlist(watchlistId, watchlistName);
    AppState.setActivePage("dataPage");
}

async function loadEditWatchlistPage() {
    document.querySelectorAll(".single-page").forEach(page => page.style.display = "none");
    document.querySelector(".watchlist-edit-page").style.display = "block";
    const response = await fetchWatchlists();
    const watchlists = await response.json();
    const table = document.querySelector("#watchlist-table-body");

    // Clear previous data
    table.innerHTML = "";

    // Populate table with watchlists
    watchlists.forEach((watchlist) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td class="centered"><button class="delete-watchlist delete-button" data-id="${watchlist.id}"><p>-</p></button></td>
            <td colspan="5" class="watchlist-name-cell">${watchlist.name}</td>
            <td colspan="2">${watchlist.last_modified}</td>
        `;
        table.appendChild(row);
    });

    AppState.setActivePage("editWatchlist");
}

function loadCreateWatchlistPage() {
    document.querySelectorAll(".single-page").forEach(page => page.style.display = "none");
    document.querySelector(".watchlist-create-page").style.display = "block";
    AppState.setActivePage("createWatchlist");
}

// =============================================================
// MAIN
// =============================================================

document.addEventListener("DOMContentLoaded", async () => {

    document.querySelectorAll(".overlay").forEach((overlay) => {
        overlay.style.display = "none";
    });

    // -------------------- INITIAL LOAD --------------------
    let previousButton = null;
    const response = await fetchWatchlists();
    const watchlists = await response.json();

    if (!watchlists || watchlists.length === 0) {
        loadCreateWatchlistPage();
        return;
    }

    // Load saved state
    const savedPage = AppState.getActivePage();

    // dataPage
    if (savedPage === "dataPage") {
        const { id, name } = AppState.getActiveWatchlist();
        previousButton = highlightButton(document.getElementById(id), previousButton);
        await loadWatchlistDataPage(id, name);

        // editWatchlist
    } else if (savedPage === "editWatchlist") {
        previousButton = highlightButton(document.getElementById("view-all-watchlists"), previousButton);
        await loadEditWatchlistPage();


        // createWatchlist
    } else if (savedPage === "createWatchlist") {
        previousButton = highlightButton(document.getElementById("create-watchlist"), previousButton);
        loadCreateWatchlistPage();


        // Default to first watchlist
    } else {
        const { id, name } = watchlists[0];
        await loadWatchlistDataPage(id, name);
    }

    // ============================================================
    // GLOBAL CLICK EVENT LISTENER
    // ============================================================

    document.addEventListener("click", async (event) => {

        // -------------------- NAVIGATION: WATCHLIST SELECTION --------------------
        if (event.target.classList.contains("watchlist-name")) {
            const watchlistId = event.target.id;
            const watchlistName = event.target.value.trim();
            previousButton = highlightButton(event.target, previousButton);
            await loadWatchlistDataPage(watchlistId, watchlistName);
        }

        // -------------------- NAVIGATION: VIEW ALL WATCHLISTS --------------------
        if (event.target.id === "view-all-watchlists") {
            previousButton = highlightButton(event.target, previousButton);
            await loadEditWatchlistPage();

        }

        // -------------------- NAVIGATION: CREATE WATCHLIST --------------------
        if (event.target.id === "create-watchlist") {
            previousButton = highlightButton(event.target, previousButton);
            await loadCreateWatchlistPage();
        }
    });
});


// ============================================================
// EVENT HANDLER: WATCHLIST DATA PAGE
// ============================================================

document.querySelector(".watchlist-data-page").addEventListener("click", async (event) => {
    sessionStorage.setItem("renaming", "false");
    const overlay = document.querySelector(".overlay.edit-watchlist-container");

    // -------------------- EDIT WATCHLIST DATA BUTTON --------------------
    const button = event.target.closest("#edit-watchlist-data");
    const page = document.querySelector(".watchlist-data-page");

    if (button) {
        setCoordinates(overlay, button, page, -130, -150);
        handleOverlay(event, overlay);
    }

    // -------------------- RENAME WATCHLIST --------------------
    if (
        event.target.id === "rename-watchlist" &&
        sessionStorage.getItem("renaming") !== "true"
    ) {
        sessionStorage.setItem("renaming", "true");
        const watchlistName = document.querySelector("#watchlist-name");
        const safeValue = watchlistName.textContent.replace(/"/g, "&quot;");

        watchlistName.innerHTML = `
      <input autofocus type="text" id="rename-input" value="${safeValue}" />
      <button id="clear-rename">Clear</button>
      <button id="save-rename">Save</button>
      <button id="cancel-rename">Cancel</button>
    `;

        const feedbackDiv = document.createElement("p");
        feedbackDiv.className = "error";
        watchlistName.parentElement.prepend(feedbackDiv);

        document.querySelector("#clear-rename").onclick = () => {
            document.querySelector("#rename-input").value = "";
        };

        document.querySelector("#cancel-rename").onclick = () => {
            const { name } = AppState.getActiveWatchlist();
            watchlistName.textContent = name;
            feedbackDiv.remove();
            sessionStorage.setItem("renaming", "false");
        };

        document.querySelector("#save-rename").onclick = async () => {
            const newName = document.querySelector("#rename-input").value;
            const { id, name } = AppState.getActiveWatchlist();

            if (newName.trim() === "") {
                feedbackDiv.textContent = "Name cannot be empty.";
                return;
            }

            if (newName === name) {
                watchlistName.textContent = name;
                feedbackDiv.remove();
                sessionStorage.setItem("renaming", "false");
                return;
            }

            const response = await fetchRenameWatchlist(id, newName);

            if (response.ok) {
                watchlistName.textContent = newName;
                document.getElementById(id).value = newName;
                AppState.setActiveWatchlist(id, newName);
                feedbackDiv.remove();
                sessionStorage.setItem("renaming", "false");
            } else {
                const data = await response.json();
                feedbackDiv.textContent = data.error;
            }
        };
    }

    // -------------------- DELETE WATCHLIST --------------------
    if (event.target.id === "delete-watchlist") {
        console.log("Delete watchlist clicked");
        const confirmationOverlay = document.querySelector(".delete-watchlist-confirm");
        handleOverlay(event, confirmationOverlay);
        await deleteWatchlist(confirmationOverlay);
    }

    // -------------------- ADD STOCK TO WATCHLIST --------------------
    if (event.target.id === "edit-stocks") {
        handleOverlay(event, overlay);

        const addStockContainer = document.querySelector(".add-stock");
        addStockContainer.innerHTML = addStock();

        const feedbackDiv = document.getElementById("add-stock-feedback");
        feedbackDiv.classList.remove("error", "success");
        feedbackDiv.textContent = "";

        document.getElementById("add-stock-button").onclick = async () => {
            const ticker = document.getElementById("add-stock-input").value.trim().toUpperCase();
            const { id, name } = AppState.getActiveWatchlist();

            if (ticker === "") {
                feedbackDiv.classList.add("error");
                feedbackDiv.textContent = "Ticker cannot be empty.";
                return;
            }

            const response = await fetchAddStockToWatchlist(ticker, id);

            const data = await response.json();

            if (response.ok) {
                feedbackDiv.classList.add("success");
                feedbackDiv.textContent = data.loading;
                await populateWatchlistTable(id, name);
                document.querySelector("#add-stock-input").value = "";
                feedbackDiv.textContent = data.message;
            } else {
                feedbackDiv.classList.add("error");
                feedbackDiv.textContent = data.error;
                console.error(data.error);
            }
        };

        document.getElementById("clear-add-stock").onclick = () => {
            document.getElementById("add-stock-input").value = "";
        };

        document.getElementById("close-add-stock").onclick = () => {
            document.querySelector(".add-stock").innerHTML = "";
        };
    }

    // -------------------- EDIT STOCK DATA BUTTON --------------------
    if (event.target.closest(".edit-stock-data")) {
        event.stopPropagation();

        const button = event.target.closest(".edit-stock-data");
        const editStockOverlay = document.querySelector(".edit-stock.overlay");
        const stockRow = button.closest("tr");

        // Pushing stock ID to overlay dataset for later use
        const stockId = stockRow.id;
        editStockOverlay.dataset.stockId = stockId;

        const page = document.querySelector(".watchlist-data-page");

        setCoordinates(editStockOverlay, button, page, -160, -60);
        handleOverlay(event, editStockOverlay);
    }

    // -------------------- DELETE STOCK BUTTON --------------------
    if (event.target.id === "delete-stock-button") {
        event.preventDefault();

        const editStockOverlay = document.querySelector(".edit-stock.overlay");
        const stockId = editStockOverlay.dataset.stockId;
        if (!stockId) return console.error("Missing stock ID in overlay.");

        const { id: watchlistId, name: watchlistName } = AppState.getActiveWatchlist();

        try {
            const response = fetchRemoveStockFromWatchlist(stockId, watchlistId);

            if (response.ok) {
                await populateWatchlistTable(watchlistId, watchlistName);
            } else {
                const data = await response.json();
                console.error(data.error);
            }
        } catch (err) {
            console.error("Error deleting stock:", err);
        }
    }
});

// ============================================================
// EVENT HANDLER: WATCHLIST EDIT PAGE
// ============================================================

document.querySelector(".watchlist-edit-page").addEventListener("click", async (event) => {
    if (event.target.classList.contains("delete-watchlist")) {
        event.preventDefault();
        const confirmationPage = document.querySelector(".delete-watchlist-table");
        handleOverlay(event, confirmationPage);
        await deleteWatchlist(confirmationPage);
    }
});

// ============================================================
// EVENT HANDLER: WATCHLIST CREATE PAGE
// ============================================================

document.querySelector(".watchlist-create-page").addEventListener("click", async (event) => {
    if (event.target.id === "create-watchlist-button") {
        event.preventDefault();

        const feedbackDiv = document.createElement("p");
        feedbackDiv.className = "error";
        const creationPage = document.querySelector(".watchlist-create-page");
        creationPage.prepend(feedbackDiv);

        const watchlistName = document.querySelector("#new-watchlist-name").value.trim();

        if (watchlistName === "") {
            feedbackDiv.textContent = "Watchlist name cannot be empty.";
            return;
        } else {
            const response = await fetchCreateWatchlist(watchlistName);

            if (response.ok) {
                const data = await response.json();
                feedbackDiv.remove();

                AppState.setActiveWatchlist(data.id, data.name);
                AppState.setActivePage("dataPage");
                window.location.href = `/dashboard/`;
            } else {
                const data = await response.json();
                feedbackDiv.textContent = data.error;
                console.error(data.error);
            }
        }
    }
});