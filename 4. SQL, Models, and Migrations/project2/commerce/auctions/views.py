from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.models import listing
from django import forms
from .models import *

class createlisting(forms.Form):
    title = forms.CharField(label = 'Product Name')
    price = forms.FloatField(label = 'Price')
    description = forms.CharField(label = 'Description')

class createbid(forms.Form):
    bid_amt = forms.FloatField(label = 'Enter Bid')

def index(request):
    return render(request, "auctions/index.html", {
        'all_listings': listing.objects.all()
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

    if request.method == 'POST':
        form = createlisting(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            price = form.cleaned_data["price"]
            description = form.cleaned_data["description"]
            user = request.user

            new_listing = listing(title = title, description = description, price = price, owner = user)
            new_listing.save()


    return render(request, "auctions/create.html", {
        "form": createlisting()
    })

def listinfo(request, listing_id):
    return render(request, "auctions/listinfo.html", {
        "listing": listing.objects.get(id=listing_id)
    })

def mylistings(request):
    user_info = User.objects.get(username = request.user)
    username = user_info.username
    listings = user_info.listing_hist.all()
    return render(request, "auctions/mylistings.html", {
        'username': username,
        'listings': listings
    })

def makebid(request, listing_id):

    listing_info = listing.objects.get(id=listing_id)
    bids = listing_info.bids.all()

    if request.method == 'POST':
        form = createbid(request.POST)
        if form.is_valid():
            bid_amt = form.cleaned_data["bid_amt"]
            user = request.user
            new_bid = bid(bidder = user, listing = listing_info, price = bid_amt)
            new_bid.save()


    return render(request, "auctions/makebid.html", {
        "listing_info": listing_info,
        "bids": bids,
        "form": createbid()
    })

