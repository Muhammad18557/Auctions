from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Bid, Comment, Watchlist


def flag_watchlisted(request, item_id):
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user.username, item_id=item_id)
        if watchlist:
            return True
        return False

    return False

def canClose(request, item_id):
    if request.user.is_authenticated:
        if Auction.objects.filter(id=item_id).exists():
            item = Auction.objects.get(id=item_id)
            if item.seller == request.user.username:
                return True
    return False

def index(request):
    available_items = Auction.objects.all()
    active = False
    for each in available_items:
        active = each.active or active
    return render(request, "auctions/index.html", {
        'available_items': available_items, 
        'active': active
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def create(request):
    if request.method == "POST":
        new = Auction()

        new.seller = request.user.username
        new.item  = request.POST["item"]
        new.description = request.POST["description"]
        new.bid = request.POST["bid"]
        new.category = request.POST["category"]
        if request.POST["image"] == "":
            new.image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAh1BMVEXv8PL6+/35+vyAiZDw8fPz9Pbv8PDt8fLe3+Tk5uqQmJyBjI+Nlpni5OZ8h4yMk5iHkJh8ho/c3eOorrPt7ez09PODiY6OlZyvtLh+hIqGj5a6v8Po7O/P1Nju7vN6gIWhpqpkbXBpcXhxe4DT2dyZn6TDyMxwfX+vsrfLy81zeH3q8PW2vMA2PLLIAAAGXklEQVR4nO2djXaiOBSAA0kA2wWkgAhGmF0Ztz/7/s+3N8G21oodxDI3zP3OaXuOCOTjJrkhRMucucN+dwG+HTK0HzK0HzK0HzK0HzK0HzK0HzK0HzK0HzK0HzK0nz/a0LWJqwwtwj38nONiDL+jMN/CpZL2GcI+0iLc4TF0HVcwexD9TfFSDH93sX8VIZi8Ioaua40h04bDY0iGmCBDMsQPGfYY2pMPKYZkaAFkSIb4IcM/1pAyPiLIkAzxQ4ZkiB8y7DGkjI8IMiRD/JAhGeKHDHsMKeMjggzJED9kSIb4IcMeQ8r4iCBDMsQPGZLhr55Fr0a+QWmlMAcbdu6JDA/FG48cWH2myvhgp5Q3FtAbfJWmi6EQYryhOdgwy6l6Gl2o8TG8pn+byNAEcfynX8QVXc2EtVQFowmDMBvaKU9j+AJdzUMa/zWWOI7TVnoIDaXwFmlzP5pVxZtU5QgNFcuCgm8X49lWRYsxhj4TQRX7o4d6gi2WVegO3GeKjO9nEgxDM3gbM3zL2KKIH+pB+0wUw0w+LO9C/1rY4a8nwjhuMWYLKNrD0sTQnHM4Xb5hng+GwdBMNb3hRbpxC8h4Z+pzDoZVgLGnYV5+aIdfAlVSvy3LM8nEp+EL1NJlIAYp4jP0hKr1CE2xM33mHAx1iWTYtspR5zbOwFAyX63vyrLYg6J36jIHQ3D80US8SpoNKP6+djj0Hn+AobP5G/ySZfJPKOcZQzeOuBbk5drJ5tiX5oonnK/gV/PDqU8HaLMwlKsy4RVPqt3aVaenmYNh5q53OooV37Uym2M79NywAkEe7VJf5tlpcWdgCAPT4Geza/hap8PT2/k5GCq5kGq737fw9/P752AolAzzPJeSQUcqT0du1mR8c7Pv+6Ku4Te7eCz5YX7UkhhqP8lU5tVC1MxjivXO00MoxfEcsCWG3WSN/vKf/VrJWmjB/tkbPa55O5slhp4we9f19v7ftK5NRug5Xvfg8d3eEsNDydlTHN3vHmvJvngUcTSdYY2hkEoIEITM3kBF1a/3BRFel8q2WmqqnXwy9xA8ih6VTgrnoyi3T1JfD6sMpYDRpnK2q5J3lOmLZF72sUMVSuiX2rtyc6ijYFrbYCiF0tXO2b76dYpMmKTxflTlw4VwA4hzs3e0nvR1ILFnfF0/dYJT7vb52LBJX0yM5HvSMO2vrUoelc/r7hv+XLgG2GP4OkCR26biR6xA0T90sK87ZMJteanfVj7vJQx+mLkI2A27fv9lu4JGeORYrkwUjxfdZPpZTqm7In0BNkLWrJY+ekPRzYbuqxJuAc1doEG77tKup3lzlG38WpGjiG9e6to8wsdvCGd8ivkZmkflHiUN3YvCq0l3GaL7japNmsFq6OV5W8ULGGXDWNQk+s+UKSR2PX0o9bKS9md5vBGiaMavnjEcdO6J1mJkIoh1O1RQRc8LQnNLIQfCTX2eacHkQ0vVURQwCM9UXD1gfLomDs+AF+57oj8bReFJDwQDqKLJ8aYqKsuNflITxkUw6NRTrVQ49KWQ6Fe9gtGqTH0/y4QMioZ/iKAJMSjWLIBaOslajKEZP/e0obN95v0hBEVIGp5yg6o53ZRUOi/+54A8DzGuNukM1bYpefkpOG81seSrXQqJvko+b0x0U9xtXFUVSJ8B69Umm3ue9PodNjWPgRY8jXRimmUU7RfF8iFHmC20YcFXphe9UE3N5qI8E0JDBPV4XSxRxlCvVCj6Cj4AfTsZo8yHtzIE/gRDlBn/tjEkw5sYDl25N/t2aLLFrA09wVRaJkk0EjiAHp6jNFQySO9GU9zdpYHwERrqKW6hwvGL9YNgIYWPcNSmlxlm4z9uISVzZeZ9WkeEwLCbDB02njxf2g/PaX5xn0nu8XWh/Bt8dE2wM4tOv9plms89QesRL1ev8z4C9CZZyU6fx0cEGZIhfsiQDPFDhj2GlPERQYZkiB8yJEP8kGGPIWV8RJAhGeKHDMkQP2TYY0gZHxFkSIb4IUMyxA8Z9hhSxkcEGZIhfsiQDPFDhj2GlPERQYZkiJ/59zQMDJ2rDG/yL1W+H3Gloa6lV3wt9/RoSekONnRsaofacHA7hEvi3uA/jkyFe5Vhb9zR0WunuWzo2sDVhpYx3HA2kKH9kKH9kKH9kKH9kKH9kKH9kKH9kKH9kKH9kKH9kKH9/A/YxOI/ygJFZAAAAABJRU5ErkJggg=="
        else:
            new.image = request.POST["image"]

        new.save()

        return HttpResponseRedirect(reverse("index")) # can be changed to listing page (better)
    else:
        return render(request, "auctions/create.html")


def listing(request, id):
    authority = canClose(request, id)
    watch = flag_watchlisted(request, id)
    if request.method == "POST":
        if "bid" in request.POST:
            offer = int(request.POST["bid"])
            if offer <= int(Auction.objects.get(id=id).bid):
                return render(request, "auctions/listing.html", {
                    'product': Auction.objects.get(id=id),
                    'watch': watch,
                    'authority': authority,
                    'warning': "Your bid must be higher than the current bid."})
            else:
                Bid.objects.filter(item_id=id).delete()
                new = Bid()
                new.user = request.user.username
                new.item_id = id
                new.bid = request.POST["bid"]
                new.save()
                Auction.objects.filter(id=id).update(bid=request.POST["bid"])
                return HttpResponseRedirect(reverse("listing", args=(id,)))

        if "comment" in request.POST:
            print("yes 1")
            new = Comment()
            new.user = request.user.username
            new.item_id = id
            new.comment = request.POST["comment"]
            new.save()
            return HttpResponseRedirect(reverse("listing", args=(id,)))
    else:
        if Bid.objects.filter(item_id=id).exists():
            b = Bid.objects.latest('id')
            user = str(b.user)
            message = "The most recent bid was placed by User: " + user
        else:
            message = "No bids have been placed yet."

        if Comment.objects.filter(item_id=id).exists():
            comments = Comment.objects.filter(item_id=id)
        else:
            print("problematic")
            comments = None

        return render(request, "auctions/listing.html",{
            'product': Auction.objects.get(id=id), 
            'watch': watch,
            'authority': authority,
            'message':message, 
            'comments': comments})


def watchlist(request, id):

    if flag_watchlisted(request, id):
        Watchlist.objects.filter(item_id=id).delete()
        
    else:
        new = Watchlist()
        new.user = request.user.username
        new.item_id = id
        new.save()

    products = [] #list of products in watchlist
    for each in Watchlist.objects.all():
        if each.user == request.user.username:
            try:
                if Auction.objects.get(id=each.item_id) and Auction.objects.get(id=each.item_id) not in products:
                    products.append(Auction.objects.get(id=each.item_id))
            except:
                continue
    if id == 0:
        return render(request, "auctions/watchlist.html", {
        'watchlist': products})
    else:
        return HttpResponseRedirect(reverse("watchlist", args=(0,)))
    


def close(request, id):
    if canClose(request, id):
        sold = Auction.objects.get(id=id)
        Auction.objects.filter(id=id).update(active=False)
        if Watchlist.objects.filter(id=id).exists:
            Watchlist.objects.filter(id=id).delete()
        return render(request, "auctions/close.html", {
            "sold": sold, 
            "buyer": Bid.objects.latest('id').user
        })
        
    else:
        return HttpResponseRedirect(reverse("listing", args=(id,)))

category_map = {1:'Grocery and Food', 2:'Clothes', 3:'Books', 4:'Household', 5:'Other'}

def categories(request, category):
    products = Auction.objects.all()
    categories_products = {}
    for each in products:
        if each.category in categories_products:
            categories_products[each.category].append(each)
        else:
            categories_products[each.category] = [each]
    if category == 0:
        return render(request, "auctions/categories.html", {
        'category_products': categories_products, 
        'category':category, 
        'map_category':category_map
    })
    else:
        products = Auction.objects.filter(category=category_map[category])
        return render(request, "auctions/categories.html", {
            'products': products,
            'category': category, 
            'category_name':category_map[category]
        })