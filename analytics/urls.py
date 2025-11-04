from .views import index, watchlist, dashboard
from django.urls import path
from django.views.generic import TemplateView
from django.urls import re_path

app_name = "analytics"
urlpatterns = [
    # Index
    path("", index.index, name="index"),
    
    # Dashboard views
    path("dashboard/", dashboard.dashboard, name="dashboard"),

    # Watchlist selection/creation/deletion views
    path("api/dashboard/watchlist/", watchlist.watchlist, name="watchlist"),
    path("api/dashboard/watchlist/select/<int:watchlist_id>/", watchlist.watchlist_select, name="watchlist_select"),
    path("api/dashboard/watchlist/data/<int:watchlist_id>/", watchlist.watchlist_data, name="watchlist_data"),
    path("api/dashboard/watchlist/create/", watchlist.watchlist_create, name="watchlist_create"),
    path("api/dashboard/watchlist/rename/<int:watchlist_id>/", watchlist.watchlist_rename, name="watchlist_rename"),
    path("api/dashboard/watchlist/delete/<int:watchlist_id>/", watchlist.watchlist_delete, name="watchlist_delete"),

    # Stock data/add/delete views
    path("api/dashboard/stock/<int:stock_id>/", watchlist.stock_data, name="stock_data"),
    path("api/dashboard/watchlist/add/stock/", watchlist.watchlist_add_stock, name="watchlist_add"),
    path("api/dashboard/watchlist/remove/stock/<int:stock_id>/<int:watchlist_id>/", watchlist.watchlist_remove_stock, name="watchlist_remove"),

    # -----------------------------
    # FRONT-END SPA ENTRY POINT
    # -----------------------------
    path("dashboard/", TemplateView.as_view(template_name="analytics/dashboard.html")),
    re_path(r"^dashboard/.*$", TemplateView.as_view(template_name="analytics/dashboard.html")),
]