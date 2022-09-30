from rest_framework import serializers
from .models import Products, Order
from datetime import datetime

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_CategoryName')

    class Meta:
        model = Products
        fields = ('id', 'name', 'original_price', 'category')

    def get_CategoryName(self, obj):
        name = ''
        try:
            product_category = obj.product_category
            if product_category:
                name = str(product_category.category_name)
        except:
            name = ''
        return name

class OrderSerializer(serializers.ModelSerializer):
    order_datetime = serializers.SerializerMethodField('get_OrderDateTime')

    class Meta:
        model = Order
        fields = ('id', 'order_no', 'total_amount', 'order_status', 'order_datetime')

    def get_OrderDateTime(self, obj):
        order_datetime = ''
        try:
            order_date = obj.order_date
            if order_date:
                order_datetime = datetime.strftime(order_date, '%Y/%m/%d %H:%M')
        except:
            order_datetime = ''
        return order_datetime

