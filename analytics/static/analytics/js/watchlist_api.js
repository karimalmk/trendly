
import { getCookie } from "./helpers.js";

// ============================================================
// WATCHLISTS API
// ============================================================

export async function fetchWatchlists() {
    return await fetch("/api/dashboard/watchlist/");
}

export async function fetchWatchlistData(watchlistId) {
    return await fetch(`/api/dashboard/watchlist/data/${watchlistId}/`);
}

export async function fetchCreateWatchlist(watchlistName) {
    return await fetch(`/api/dashboard/watchlist/create/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ name: watchlistName }),
    });
}

export async function fetchDeleteWatchlist(id) {
    return await fetch(`/api/dashboard/watchlist/delete/${id}/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    });
}

export async function fetchRenameWatchlist(id, newName) {
    return await fetch(`/api/dashboard/watchlist/rename/${id}/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ name: newName }),
    });
}


// ============================================================
// STOCK MANAGEMENT API
// ============================================================

export async function fetchAddStockToWatchlist(ticker, id) {
    return await fetch(`/api/dashboard/watchlist/add/stock/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ ticker, watchlist_id: id }),
    });
}

export async function fetchRemoveStockFromWatchlist(stockId, watchlistId) {
    return await fetch(
        `/api/dashboard/watchlist/remove/stock/${stockId}/${watchlistId}/`,
        {
            method: "DELETE",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        }
    );
}