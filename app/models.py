"""
Definition of models.
"""
# Create your models here.
from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)

class Listing(models.Model):
    listing_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    rating = models.IntegerField()
    comment = models.TextField()
    sender = models.ForeignKey(User, related_name='sent_feedback', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_feedback', on_delete=models.CASCADE)


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class TransactionHistory(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, related_name='transactions_bought', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='transactions_sold', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    #payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    transaction_time = models.DateTimeField()

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_time = models.DateTimeField()
    buyer = models.ForeignKey(User, related_name='payments_made', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='payments_received', on_delete=models.CASCADE)
    transaction = models.ForeignKey(TransactionHistory, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)