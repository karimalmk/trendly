from django.db import models
from django.contrib.auth.models import User


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    user = models.ManyToManyField(User, through="WatchlistStock")

    def __str__(self):
        return self.ticker

    class Meta:
        constraints = [
            models.UniqueConstraint("ticker", name="unique_stock_ticker")
        ]


class Watchlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock, through='WatchlistStock')
    last_modified = models.DateTimeField(auto_now=True) # format: YYYY-MM-DD HH:MM:SS, default timezone is UTC

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name='unique_watchlist_per_user')
        ]


class WatchlistStock(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='watchlist_stocks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist_stock_user')

    def __str__(self):
        return f"{self.watchlist.name} - {self.stock.ticker}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['watchlist', 'stock'], name='unique_watchlist_stock')
        ]