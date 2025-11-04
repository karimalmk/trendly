from datetime import datetime
import json
from django.http import JsonResponse

from ..models import Watchlist, WatchlistStock, Stock
from ..utils.quotes_api import check_stock, lookup

## ============================================================
## WATCHLIST SELECTION/CREATION/DELETION VIEWS
## ============================================================

# api/dashboard/watchlist/
from django.http import JsonResponse

def watchlist(request):
    if request.method == "GET":
        watchlists = Watchlist.objects.filter(user=request.user).values_list("id", "name", "last_modified")

        # Build a list of properly formatted dicts
        data = []
        for wid, name, last_modified in watchlists:
            data.append({
                "id": wid,
                "name": name,
                "last_modified": last_modified.strftime("%Y-%m-%d %H:%M:%S")
            })

        return JsonResponse(data, safe=False)
    
# api/dashboard/watchlist/select/
def watchlist_select(request, watchlist_id):
    watchlist_id = int(watchlist_id)

    # Get stocks quotes for selected watchlist
    watchlist_stocks = WatchlistStock.objects.filter(
        watchlist_id=watchlist_id,
        watchlist__user_id=request.user.id
    )
    stocks = []
    for ws in watchlist_stocks:
        stock = Stock.objects.filter(id=ws.stock_id, user_id=request.user.id).first()
        if stock:
            stocks.append({
                    "id": stock.id,
                    "ticker": stock.ticker
            })
    return JsonResponse(stocks, safe=False)

# api/dashboard/watchlist/data/<watchlist_id>/
def watchlist_data(request, watchlist_id):

    watchlist_id = int(watchlist_id)
    watchlist = Watchlist.objects.filter(
        id=watchlist_id,
        user__id=request.user.id
    )
    
    # Get date of last modification and stock tickers
    modification_date = watchlist.filter(id=watchlist_id).first().last_modified
    modification_date = modification_date.strftime("%Y-%m-%d %H:%M:%S")

    watchlist_stocks = list(WatchlistStock.objects.filter(watchlist__id=watchlist_id).values_list("stock_id", "stock__ticker"))

    if watchlist_stocks == []:
        return JsonResponse({"quotes": [], "meta_data": {"length": 0, "last_modified": modification_date}}, safe=False)

    # Meta data on watchlist
    meta_data = {"length": len(watchlist_stocks), "last_modified": modification_date}

    # Get stock quotes and ID's
    quotes = []
    for ws in watchlist_stocks:
        quotes.append([ws[0], lookup(ws[1])])

    return JsonResponse({"quotes": quotes, "meta_data": meta_data}, safe=False)


# api/dashboard/stock/<stock_id>
def stock_data(request, stock_id):
    stock = Stock.objects.filter(id=stock_id, user_id=request.user.id).first()
    if not stock:
        return JsonResponse({"error": "Stock not found"}, status=404)

    quote = lookup(stock.ticker)
    return JsonResponse(quote, safe=False)

# api/dashboard/watchlist/rename/<watchlist_id>/
def watchlist_rename(request, watchlist_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        new_name = data.get("name", "").strip()
        if new_name == "":
            return JsonResponse({"error": "Invalid name"}, status=400)

        # Check if new name already exists for this user
        if Watchlist.objects.filter(name=new_name, user_id=request.user.id).exists():
            return JsonResponse({"error": "Watchlist name already exists"}, status=400)

        watchlist = Watchlist.objects.filter(
            id=watchlist_id,
            user_id=request.user.id
        ).first() # the .first() ensures we get a single object or None - not a QuerySet
        if not watchlist:
            return JsonResponse({"error": "Watchlist not found"}, status=404)

        watchlist.name = new_name
        watchlist.save()
        return JsonResponse({"message": "Watchlist renamed successfully"}, status=200)


# api/dashboard/watchlist/create/
def watchlist_create(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name", "").strip()
        if name == "":
            return JsonResponse({"error": "Invalid name."}, status=400)

        # Check if name already exists for this user
        if Watchlist.objects.filter(name=name, user_id=request.user.id).exists():
            return JsonResponse({"error": "Watchlist name already exists."}, status=400)

        watchlist = Watchlist.objects.create(
            name=name,
            user_id=request.user.id
        )
        return JsonResponse({"id": watchlist.id, "name": watchlist.name},status=201)

    return JsonResponse({"error": "Invalid request method."}, status=400)
    
# api/dashboard/watchlist/delete/<watchlist_id>/
def watchlist_delete(request, watchlist_id):
    if request.method == "DELETE":
        watchlist = Watchlist.objects.filter(
            id=watchlist_id,
            user_id=request.user.id
        ).first()
        if not watchlist:
            return JsonResponse({"error": "Watchlist not found"}, status=404)

        watchlist.delete()
        return JsonResponse({"message": "Watchlist deleted successfully"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)


## ============================================================
## STOCK DATA/ADD/DELETE VIEWS
## ============================================================

# /api/dashboard/watchlist/add/stock/
def watchlist_add_stock(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    data = json.loads(request.body)
    ticker = data.get("ticker", "").strip().upper()
    watchlist_id = data.get("watchlist_id")

    if not ticker or not watchlist_id:
        return JsonResponse({"error": "Missing ticker or watchlist ID."}, status=400)

    if not check_stock(ticker):
        return JsonResponse({"error": "Invalid stock symbol."}, status=400)

    # Get the watchlist
    try:
        watchlist = Watchlist.objects.get(id=watchlist_id, user=request.user)
    except Watchlist.DoesNotExist:
        return JsonResponse({"error": "Watchlist not found."}, status=404)

    # Check if stock exists, else create it
    stock, created = Stock.objects.get_or_create(ticker=ticker)

    # Check if already in the watchlist
    if watchlist.stocks.filter(id=stock.id).exists():
        return JsonResponse({"error": "Stock already in watchlist."}, status=400)
    
    # Create WatchlistStock entry
    addStock = WatchlistStock.objects.create(
        watchlist=watchlist,
        stock=stock,
        user=request.user
    )

    # Add stock to the watchlist
    watchlist.stocks.add(stock)

    # Change last modified date
    watchlist.last_modified = datetime.now()
    watchlist.save()

    return JsonResponse({"message": f"{ticker} added successfully.", "loading": f"{ticker} is being added..."}, status=200)


# /api/dashboard/watchlist/remove/stock/<stock_id>&<watchlist_id>/
def watchlist_remove_stock(request, stock_id, watchlist_id):
    if request.method == "DELETE":
        if not stock_id or not watchlist_id:
            return JsonResponse({"error": "Missing stock ID or watchlist ID."}, status=400)

        # Get the watchlist
        try:
            watchlist = Watchlist.objects.get(id=watchlist_id, user=request.user)
        except Watchlist.DoesNotExist:
            return JsonResponse({"error": "Watchlist not found."}, status=404)

        # Get the stock
        try:
            stock = Stock.objects.get(id=stock_id)
        except Stock.DoesNotExist:
            return JsonResponse({"error": "Stock not found."}, status=404)

        # Remove the stock from the watchlist
        watchlist.stocks.remove(stock)

        # Change last modified date
        watchlist.last_modified = datetime.now()
        watchlist.save()

        return JsonResponse({"message": f"Stock {stock.ticker} removed successfully."}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)
