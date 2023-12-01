# app/urls.py
from django.urls import path
from .views import active_listings, listing_detail, place_bid, user_bids, user_transactions

urlpatterns = [
    path('active_listings/', active_listings, name='active_listings'),
    path('listing/<int:listing_id>/', listing_detail, name='listing_detail'),
    path('listing/<int:listing_id>/place_bid/', place_bid, name='place_bid'),
    path('user_bids/', user_bids, name='user_bids'),
    path('user_transactions/', user_transactions, name='user_transactions'),
    # Add other URL patterns as needed
]