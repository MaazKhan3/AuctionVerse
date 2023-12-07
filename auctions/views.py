from django.urls import reverse
from django.db.models import Max
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import re

from .models import User, Category, AuctionListing, Bid, Comment, PurchaseHistory


def index(request):
    obj = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "objects": obj
    })


def all(request):
    obj = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "objects": obj
    })
def purchase(request):
    obj = AuctionListing.objects.all()
    return render(request, "auctions/purchase.html", {
        "objects": obj
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


@login_required
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


@login_required
def createListing(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        startBid = request.POST["startBid"]
        category = Category.objects.get(id=request.POST["category"])
        user = request.user
        imageUrl = request.POST["url"]
        if imageUrl == '':
            imageUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png"
        listing = AuctionListing.objects.create(
            name=title, category=category, date=timezone.now(), startBid=startBid, description=description, user=user, imageUrl=imageUrl, active=True)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/createListing.html", {
        'categories': Category.objects.all()
    })


def details(request, id):
    item = AuctionListing.objects.get(id=id)
    bids = Bid.objects.filter(auctionListing=item)
    comments = Comment.objects.filter(auctionListing=item)
    value = bids.aggregate(Max('bidValue'))['bidValue__max']
    bid = None
    if value is not None:
        bid = Bid.objects.filter(bidValue=value)[0]
    return render(request, "auctions/details.html", {
        'item': item,
        'bids': bids,
        'comments': comments,
        'bid': bid
    })


def categories(request):
    if request.method == 'POST':
        category = request.POST["category"]
        new_category, created = Category.objects.get_or_create(
            name=category.lower())
        if created:
            new_category.save()
        else:
            messages.warning(request, "Category already Exists!")
        return HttpResponseRedirect(reverse("categories"))
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.all()
    })


def filter(request, name):
    category = Category.objects.get(name=name)
    obj = AuctionListing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "objects": obj
    })


@login_required
def comment(request, id):
    if request.method == 'POST':
        auctionListing = AuctionListing.objects.get(id=id)
        user = request.user
        commentValue = request.POST["content"].strip()
        if(commentValue != ""):
            comment = Comment.objects.create(date=timezone.now(
            ), user=user, auctionListing=auctionListing, commentValue=commentValue)
            comment.save()
        return HttpResponseRedirect(reverse("details", kwargs={'id': id}))
    return HttpResponseRedirect(reverse("index"))


@login_required
def bid(request, id):
    if request.method == 'POST':
        auctionListing = AuctionListing.objects.get(id=id)
        bidValue = request.POST["bid"]
        args = Bid.objects.filter(auctionListing=auctionListing)
        value = args.aggregate(Max('bidValue'))['bidValue__max']
        if value is None:
            value = 0
        if float(bidValue) < auctionListing.startBid or float(bidValue) <= value:
            messages.warning(
                request, f'Bid Higher than: {max(value, auctionListing.startBid)}!')
            return HttpResponseRedirect(reverse("details", kwargs={'id': id}))
        user = request.user
        bid = Bid.objects.create(
            date=timezone.now(), user=user, bidValue=bidValue, auctionListing=auctionListing)
        bid.save()
    return HttpResponseRedirect(reverse("details", kwargs={'id': id}))


@login_required
def end(request, itemId):
    auctionListing = AuctionListing.objects.get(id=itemId)
    user = request.user
    if auctionListing.user == user:
        auctionListing.active = False
        auctionListing.save()
        messages.success(
            request, f'Auction for {auctionListing.name} successfully closed!')
    else:
        messages.info(
            request, 'You are not authorized to end this listing!')
    return HttpResponseRedirect(reverse("details", kwargs={'id': itemId}))


@login_required
def watchlist(request):
    if request.method == 'POST':
        user = request.user
        auctionListing = AuctionListing.objects.get(id=request.POST["item"])
        if request.POST["status"] == '1':
            user.watchlist.add(auctionListing)
        else:
            user.watchlist.remove(auctionListing)
        user.save()
        return HttpResponseRedirect(
            reverse("details", kwargs={'id': auctionListing.id}))
    return HttpResponseRedirect(reverse("index"))


@login_required
def watch(request):
    user = request.user
    obj = user.watchlist.all()
    return render(request, "auctions/index.html", {
        "objects": obj
    })
    
import re

@login_required
def get_highest_bids(request):
    user = request.user

    # Assuming you have a Bid model with a foreign key to AuctionListing
    highest_bids_data = user.get_highest_bids()

    # Extracting the listing IDs from the bid data
    listing_ids = [listing_id for listing_id, data in highest_bids_data.items()]

    # Fetching the corresponding AuctionListing objects
    auction_listings = AuctionListing.objects.filter(id__in=listing_ids, sold=False)

    # Creating a list of dictionaries with listing id, AuctionListing object, and bid information
    obj = []
    for listing, data in zip(auction_listings, highest_bids_data.values()):
        current_user_bid_str = str(data['bid'])  # Convert to string in case it's not already a string

        # Extracting the bid value from the string
        match = re.search(r'bid (\d+\.\d+)', current_user_bid_str)
        current_user_bid = float(match.group(1)) if match else None

        # Fetch the current highest bid for the listing
        current_highest_bid_query = Bid.objects.filter(auctionListing=listing).aggregate(Max('bidValue'))
        current_highest_bid = current_highest_bid_query['bidValue__max']

        # If there are no bids yet, set current_highest_bid to starting bid
        if current_highest_bid is None:
            current_highest_bid = listing.startBid

        obj.append({
            "id": listing.id,
            "name": listing.name,
            "imageUrl": listing.imageUrl,
            "startBid": listing.startBid,
            "date": listing.date,
            "active": listing.active,
            "watchlist": listing in user.watchlist.all(),
            "current_user_bid": current_user_bid,
            "current_highest_bid": current_highest_bid,
        })

    return render(request, "auctions/purchase.html", {
        "objects": obj,
    })
    
@login_required
def complete_purchase(request, item_id):
    # Retrieve the auction listing based on the provided item_id
    item = get_object_or_404(AuctionListing, pk=item_id)

    if request.method == 'POST':
        # Get additional information from the form
        phone_number = request.POST.get('phone_number')
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')

        # Fetch the highest bid for the item
        highest_bid_query = Bid.objects.filter(auctionListing=item).aggregate(Max('bidValue'))
        highest_bid_value = highest_bid_query['bidValue__max']

        # If there are no bids yet, set highest_bid_value to starting bid
        if highest_bid_value is None:
            highest_bid_value = item.startBid

        # Create a new PurchaseHistory instance with the collected data
        purchase_history = PurchaseHistory(
            user=request.user,
            item=item,
            phone_number=phone_number,
            full_name=full_name,
            address=address,
            city=city,
            country=country,
            purchase_price=highest_bid_value,  # Use the highest bid value
            category=item.category,
            name=item.name,
            date=item.date,
            startBid=item.startBid,
            description=item.description,
            imageUrl=item.imageUrl,
            active=item.active
        )

        # Save the PurchaseHistory instance to the database
        purchase_history.save()
        #q

# Redirect to the delete_listing view to remove the item from AuctionListing
        return redirect('delete_listing', item_id=item.id)

    return render(request, 'auctions/completepurchase.html', {'item': item})
@login_required
def purchased(request):
    # Retrieve all PurchaseHistory instances for the logged-in user
    purchase_history_items = PurchaseHistory.objects.filter(user=request.user)

    # Create a list of dictionaries with the relevant information including shipping details
    obj = []
    for purchase_history_item in purchase_history_items:
        item_info = {
            'name': purchase_history_item.name,
            'purchase_price': purchase_history_item.purchase_price,
            'date': purchase_history_item.date,
            'phone_number': purchase_history_item.phone_number,
            'full_name': purchase_history_item.full_name,
            'address': purchase_history_item.address,
            'city': purchase_history_item.city,
            'country': purchase_history_item.country,
            'category': purchase_history_item.category.name,  # Assuming Category has a 'name' field
            'startBid': purchase_history_item.startBid,
            'description': purchase_history_item.description,
            'imageUrl': purchase_history_item.imageUrl,
            'active': purchase_history_item.active,
            # Add other fields as needed
        }
        obj.append(item_info)

    return render(request, 'auctions/purchased.html', {'obj': obj})

@login_required
def delete_listing(request, item_id):
    item = get_object_or_404(AuctionListing, pk=item_id)

    # Perform any additional checks or validations if needed before marking as sold

    # Mark the item as sold in AuctionListing
    item.sold = True
    item.save()

    # Redirect to the desired page (e.g., back to the home page)
    return redirect('purchased')