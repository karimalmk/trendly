from django.contrib import admin
from .models import Stock, Watchlist, WatchlistStock

# Register your models here.

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('last_modified', 'id', 'name')
    search_fields = ('name',)

admin.site.register(Stock)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(WatchlistStock)