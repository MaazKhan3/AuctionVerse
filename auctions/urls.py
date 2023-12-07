from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("details/<int:id>", views.details, name="details"),
    path("categories", views.categories, name="categories"),
    path("filter/<str:name>", views.filter, name="filter"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("end/<int:itemId>", views.end, name="end"),
    path("all", views.all, name="all"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watch", views.watch, name="watch"),
    path("purchase", views.get_highest_bids, name="purchase"),
    path('purchased', views.purchased, name='purchased'),
    path('complete_purchase/<int:item_id>/', views.complete_purchase, name='complete_purchase'),
    path('delete_listing/<int:item_id>/', views.delete_listing, name='delete_listing')
]
