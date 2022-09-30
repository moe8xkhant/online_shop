# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import product_category, customer_category, product_discount, CustomerProfile, department, Order, OrderItems, UserAccountActivation, Group_ProductCategory_Relationship

# Register your models here.
# Register your models here.
@admin.register(department)
class department(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)

@admin.register(product_category)
class product_category(admin.ModelAdmin):
    list_display = ('category_name',)
    ordering = ('category_name',)
    search_fields = ('category_name',)

@admin.register(customer_category)
class customer_category(admin.ModelAdmin):
    list_display = ('category_name','start_order_point', 'end_order_point')
    ordering = ('start_order_point',)
    search_fields = ('category_name',)

@admin.register(product_discount)
class product_discount(admin.ModelAdmin):
    list_display = ('product_category_name','customer_category_name', 'discount_percent')
    ordering = ('product_category__category_name',)
    search_fields = ('customer_category__category_name', 'discount_percent','product_category__category_name',)

    def customer_category_name(self, obj):
        return obj.customer_category.category_name

    def product_category_name(self, obj):
        return obj.product_category.category_name

    def get_form(self, request, obj=None, **kwargs):
        form = super(product_discount, self).get_form(request, obj, **kwargs)
        form.base_fields['customer_category'].label_from_instance = lambda inst: "{}".format(inst.category_name)
        form.base_fields['product_category'].label_from_instance = lambda inst: "{}".format(inst.category_name)
        return form

@admin.register(CustomerProfile)
class CustomerProfile(admin.ModelAdmin):
    list_display = ('user','phone_no', 'customer_category_name', 'department_name')
    ordering = ('user',)
    list_filter = ('user', 'customer_category__category_name', 'department__name')
    search_fields = ('user__username','phone_no', 'customer_category__category_name', 'department__name')

    def department_name(self, obj):
        if obj.department:
            return obj.department.name
        return None

    def customer_category_name(self, obj):
        return obj.customer_category.category_name

    def get_form(self, request, obj=None, **kwargs):
        form = super(CustomerProfile, self).get_form(request, obj, **kwargs)
        form.base_fields['customer_category'].label_from_instance = lambda inst: "{}".format(inst.category_name)
        form.base_fields['department'].label_from_instance = lambda inst: "{}".format(inst.name)
        return form

@admin.register(UserAccountActivation)
class UserAccountActivation(admin.ModelAdmin):
    list_display = ('user','random_string', 'is_activate', 'activate_date')
    ordering = ('user',)
    search_fields = ('user','is_activate', 'activate_date',)


@admin.register(Group_ProductCategory_Relationship)
class Group_ProductCategory_Relationship(admin.ModelAdmin):
    list_display = ('department_name','product_category_name')
    ordering = ('department__name',)
    search_fields = ('product_category__category_name', 'department__name',)

    def product_category_name(self, obj):
        return obj.product_category.category_name

    def department_name(self, obj):
        if obj.department:
            return obj.department.name
        return None


    def get_form(self, request, obj=None, **kwargs):
        form = super(Group_ProductCategory_Relationship, self).get_form(request, obj, **kwargs)
        form.base_fields['product_category'].label_from_instance = lambda inst: "{}".format(inst.category_name)
        form.base_fields['department'].label_from_instance = lambda inst: "{}".format(inst.name)
        return form
