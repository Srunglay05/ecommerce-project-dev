import json
from rest_framework import serializers
from .models import *
from rest_framework.permissions import IsAuthenticated
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Order, OrderItem


class TopBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopBanner
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:        
        model =  ProductList
        fields = ['id', 'ProLName', 'ProCategoryID','ProLPrice', 'ProLImage']


class ProductDetailSerializer(serializers.ModelSerializer):
    productID = ProductListSerializer(read_only=True)
    productID_id = serializers.PrimaryKeyRelatedField(queryset=ProductList.objects.all(), source='productID', write_only=True)

    class Meta:
        model = ProductDetail
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Blog
        fields = ['id', 'BlogName', 'BlogRate', 'BlogImage']


class BlogDetailSerializer(serializers.ModelSerializer):
    blogID = BlogSerializer(read_only=True)
    blogID_id = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), write_only=True)

    class Meta:
        model = BlogDetails
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta:        
        model =  ProductCategory
        fields = ['id', 'CategoryName']


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['productName', 'price', 'qty']


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customerName', 'customerPhone', 'orderDate', 'totalAmount', 'QRCodeInvoice', 'items']

    def get_items(self, obj):
        items = obj.items.all()
        return OrderItemSerializer(items, many=True).data

    def create(self, validated_data):
        request = self.context['request']
        items_json = request.data.get('items')
        items_data = json.loads(items_json) if items_json else []

        # Pop items key out, rest is for Order creation (QRCodeInvoice will be in validated_data as file)
        validated_data.pop('items', None)

        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'price', 'quantity', 'subtotal']


        




