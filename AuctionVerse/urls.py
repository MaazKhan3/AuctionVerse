# auctionverse/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),  # Adjust 'app' to match your app name
    # Add other app URLs as needed
]
