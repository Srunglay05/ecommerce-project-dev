from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal

from .models import (
    ProductCategory,
    NewArrivals,
    Order,
    UserProfile,
    CartItem,
)
from django.contrib.contenttypes.models import ContentType


class UserProfileTest(TestCase):

    def test_user_profile_created(self):
        user = User.objects.create_user(
            username="testuser",
            password="123456"
        )

        self.assertTrue(
            UserProfile.objects.filter(user=user).exists()
        )


class ProductCategoryTest(TestCase):

    def test_create_category(self):
        category = ProductCategory.objects.create(
            CategoryName="Skincare"
        )

        self.assertEqual(
            category.CategoryName,
            "Skincare"
        )


class ProductTest(TestCase):

    def test_create_product(self):
        category = ProductCategory.objects.create(
            CategoryName="Makeup"
        )

        product = NewArrivals.objects.create(
            ProCategoryID=category,
            NewAName="Lipstick",
            NewAPrice=Decimal("10.00")
        )

        self.assertEqual(
            product.NewAName,
            "Lipstick"
        )


class OrderTest(TestCase):

    def test_create_order(self):

        user = User.objects.create_user(
            username="customer",
            password="123456"
        )

        order = Order.objects.create(
            user=user,
            customerName="John",
            customerPhone="012345678",
            customerAddress="Phnom Penh",
            customerEmail="john@test.com",
            totalAmount=Decimal("50.00")
        )

        self.assertEqual(
            order.status,
            "Pending"
        )


class CartItemTest(TestCase):

    def test_cart_item_creation(self):

        user = User.objects.create_user(
            username="buyer",
            password="123456"
        )

        category = ProductCategory.objects.create(
            CategoryName="Perfume"
        )

        product = NewArrivals.objects.create(
            ProCategoryID=category,
            NewAName="Dior",
            NewAPrice=Decimal("20.00")
        )

        content_type = ContentType.objects.get_for_model(
            NewArrivals
        )

        cart = CartItem.objects.create(
            user=user,
            content_type=content_type,
            object_id=product.id,
            quantity=2,
            price=Decimal("20.00")
        )

        self.assertEqual(
            cart.subtotal,
            Decimal("40.00")
        )