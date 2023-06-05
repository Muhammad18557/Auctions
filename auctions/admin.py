from django.contrib import admin
from .models import Auction, Bid, Comment, Watchlist
# Register your models here.

class Auctions(admin.ModelAdmin):
    list_display = ("seller", "item", "description", "bid", "category", "posted_on", "image", "active")
admin.site.register(Auction)

class Bids(admin.ModelAdmin):
    list_display = ("item_id", "user", "item", "bid")
admin.site.register(Bid)

class Comments(admin.ModelAdmin):
    list_display = ("item_id", "user", "comment", "time")
admin.site.register(Comment)

class Watchlists(admin.ModelAdmin):
    list_display = ("user", "item_id")

admin.site.register(Watchlist)