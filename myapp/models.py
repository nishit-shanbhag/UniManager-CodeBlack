from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    type = models.IntegerField(blank=False, null=False, default=0)
    college_id = models.CharField(blank=True, null=False, max_length=100)

class LostAndFound(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    information = models.CharField(blank=True, null=False, max_length=1000)
    status = models.IntegerField(blank=False, null=False, default=0)
    submit_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    submit_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_submit")
    takeaway_user = models.ForeignKey(get_user_model(), null=True, default=None, on_delete=models.CASCADE, related_name="user_takeaway")
    takeaway_date = models.DateTimeField(default=None, null=True, blank=False)
    item_received = models.BooleanField(default=False)


class Complaint(models.Model):
    location = models.CharField(blank=False, null=False, max_length=1000)
    info = models.CharField(blank=False, null=False, max_length=1000)
    status = models.IntegerField(blank=False, null=False, default=0)
    submit_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_complaints")
    photo = models.ImageField(upload_to="complaint_images/", null=True)
    requested_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    category = models.CharField(blank=False, null=False, max_length=1000)


class Order(models.Model):
    submit_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_order")
    order_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    delivery_date = models.DateTimeField(null=False, blank=False)
    total_cost = models.IntegerField(blank=False, null=True)
    status = models.IntegerField(blank=False, null=False, default=0)


class Menu(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    price = models.IntegerField(blank=False, null=False)
    photo = models.ImageField(upload_to="item_images/")


class Order_items(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="item_orderid")
    item_id = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.IntegerField(blank=False, null=False)


class Event(models.Model):
    event_name = models.CharField(blank=False, null=False, max_length=100)
    event_desc = models.CharField(blank=False, null=False, max_length=1000)
    organizing_committee = models.CharField(blank=True, null=True, max_length=100)
    location = models.CharField(blank=False, null=False, max_length=100)
    link = models.CharField(blank=True, null=True, max_length=1000)
    event_date = models.DateTimeField(null=False, blank=False)
    duration = models.CharField(blank=False, null=False, max_length=100)



