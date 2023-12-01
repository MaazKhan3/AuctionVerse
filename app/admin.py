from django.contrib import admin
from .models import User, Listing, Bid, Category, Feedback, Product, TransactionHistory, Payment

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Feedback)
admin.site.register(Product)
admin.site.register(TransactionHistory)
admin.site.register(Payment)