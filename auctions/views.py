from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, Watchlist
from .forms import Add_listing


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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


def listings(request, product_id):
    bids = Bid.objects.filter(product=product_id)
    user = User.objects.get(pk=request.user.id)
    listing = Listing.objects.get(pk=product_id)
    if request.method == "POST" and request.user.is_authenticated:
        if request.POST['action'] == "Watchlist":
            watchls = Watchlist.objects.create(watchlist = True, user=user, product=listing)
            return render(request, "auctions/listings.html", {
                "message": "Added to watchlist",
                "listing": Listing.objects.get(id=product_id),
                "bids": f"{bids.count()}",
                "comments": Comment.objects.filter(id=product_id)
            })
        elif request.POST['action'] == "Place Bid":
            newbid = Bid.objects.create(bid=int(request.POST['bid_price']), bidder=user, product=listing)
            return render(request, "auctions/listings.html", {
                "listing": listing,
                "bids": f"{bids.count()}",
                "newbid": f"{newbid.bid}"
            })
    return render(request, "auctions/listings.html", {
        "listing": Listing.objects.get(id=product_id),
        "bids": f"{bids.count()}",
        "comments": Comment.objects.filter(id=product_id)
    })


def add_listing(request):
    if request.method == "POST":
        form = Add_listing(request.POST, request.FILES)
        if form.is_valid():
            new = Listing()
            new.product = form.cleaned_data["product"]
            new.price = form.cleaned_data["price"]
            new.description = form.cleaned_data["description"]
            new.lister = request.user
            new.product_image = form.cleaned_data["product_image"]
            new.image_url = form.cleaned_data["image_url"]
            new.category = form.cleaned_data["category"]
            new.save()
            return render(request, "auctions/add_listing.html", {
                "message": "Your Listing has been added!"
            })
    
    return render(request, "auctions/add_listing.html", {
        "form": Add_listing()
    })


def categories(request):
    ls = Listing.objects.values("category").exclude(category=None).distinct()
    return render(request, "auctions/categories.html", {
        "categories": ls,
    })

def category(request, category):
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": Listing.objects.filter(category=category),
    })


@login_required
def watchlist(request, user):
    person = User.objects.get(username = user)
    return render(request, "auctions/watchlist.html", {
        "listings": person.watchlist.all()
    })
