# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User,Group

from simple_history.models import HistoricalRecords

# Create your models here.
class department(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)

class product_category(models.Model):
    category_name = models.CharField(max_length=30, null=True, blank=True)

class customer_category(models.Model):
    category_name = models.CharField(max_length=30, null=True, blank=True)
    start_order_point = models.IntegerField(null=True, blank=True)
    end_order_point = models.IntegerField(null=True, blank=True)

class product_discount(models.Model):
    product_category = models.ForeignKey(product_category, on_delete=models.CASCADE, blank=True, null=True)
    customer_category = models.ForeignKey(customer_category, on_delete=models.CASCADE, blank=True, null=True)
    discount_percent = models.IntegerField()

class Products(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    original_price = models.FloatField(null=True, blank=True)
    product_category = models.ForeignKey(product_category, on_delete=models.CASCADE)


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, editable=True)
    phone_no = models.CharField(max_length=30, null=True, blank=True)
    customer_category = models.ForeignKey(customer_category, on_delete=models.CASCADE, null=True, blank=True)
    department = models.OneToOneField(department, editable=True, blank=True, null=True)


class Order(models.Model):
    order_no = models.CharField(max_length=30, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    discount = models.FloatField(null=True, blank=True)
    order_date = models.DateTimeField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    paid_amount = models.FloatField(null=True, blank=True)
    order_status = models.CharField(max_length=30, null=True, blank=True)
    shipping_address = models.CharField(max_length=255, null=True, blank=True)
    contact_no = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        ordering = ['-order_date']

    history = HistoricalRecords()

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    item_price = models.FloatField(null=True, blank=True)
    qty = models.IntegerField()
    cost = models.FloatField()
    discount_percent = models.IntegerField(null=True, blank=True)

class UserAccountActivation(models.Model):
    user = models.OneToOneField(User, editable=True)
    random_string = models.CharField(max_length=255)
    is_activate = models.BooleanField()
    activate_date = models.DateTimeField(null=True, blank=True)

class Group_ProductCategory_Relationship(models.Model):
    department = models.OneToOneField(department, editable=True, null=True, blank=True)
    product_category = models.ForeignKey(product_category, on_delete=models.CASCADE, null=True, blank=True)










