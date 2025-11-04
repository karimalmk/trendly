from django.shortcuts import render
from ..models import Watchlist

# dashboard/
def dashboard(request):
    watchlists = Watchlist.objects.filter(user_id=request.user.id)
    return render(request, "dashboard.html", {"watchlists": watchlists})
