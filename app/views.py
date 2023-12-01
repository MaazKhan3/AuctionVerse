# yourapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .models import Listing, Bid, TransactionHistory, Payment

def active_listings(request):
    active_listings = Listing.objects.filter(status='active')
    return render(request, 'app/active_listings.html', {'active_listings': active_listings})

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    bids = Bid.objects.filter(listing=listing).order_by('-bid_amount')  # Show bids in descending order
    return render(request, 'app/listing_detail.html', {'listing': listing, 'bids': bids})

@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')
        # Perform validation on the bid_amount, e.g., it should be higher than the current bid.

        Bid.objects.create(
            bid_amount=bid_amount,
            bid_time=timezone.now(),
            bidder=request.user,
            listing=listing
        )

        return redirect('listing_detail', listing_id=listing_id)

    return render(request, 'app/place_bid.html', {'listing': listing})

@login_required
def user_bids(request):
    user_bids = Bid.objects.filter(bidder=request.user).order_by('-bid_time')
    return render(request, 'app/user_bids.html', {'user_bids': user_bids})

@login_required
def user_transactions(request):
    user_transactions = TransactionHistory.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).order_by('-transaction_time')

    user_payments = Payment.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).order_by('-payment_time')

    return render(request, 'app/user_transactions.html', {'user_transactions': user_transactions, 'user_payments': user_payments})