from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction(models.Model):
    seller = models.CharField(max_length=64,default=None)
    item = models.CharField(max_length=64)
    description = models.TextField()
    bid = models.IntegerField()
    category = models.CharField(max_length=64)
    posted_on = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=300)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.seller} {self.item} {self.description} {self.bid} {self.category} {self.posted_on} {self.image} {self.active}"

class Bid(models.Model):
    item_id = models.IntegerField()
    user = models.CharField(max_length=64)
    item = models.CharField(max_length=64)
    bid = models.IntegerField()
    
    def __str__(self):
        return f"{self.item_id} {self.user} {self.item} {self.bid}"

class Comment(models.Model):
    item_id = models.IntegerField()
    user = models.CharField(max_length=64)
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_id} {self.user} {self.comment} {self.time}"


class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    item_id = models.IntegerField()

    def __str__(self):
        return f"{self.user} {self.item_id}"


class Winner(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    item_id = models.IntegerField()
    win_bid = models.IntegerField()
    item = models.CharField(max_length=64)

    
