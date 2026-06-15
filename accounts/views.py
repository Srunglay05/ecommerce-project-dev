from urllib import request, response
from django.db.models import Count
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.contrib import messages

from .authentication import QueryParamAccessTokenAuthentication
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.db.models import Q

import json
from django.http import JsonResponse
import qrcode
from io import BytesIO
from rest_framework.decorators import api_view
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response

from django.db import transaction




# Create your views here.

from django.shortcuts import redirect


def ListProductWithAddToCartCheckoutOrder(request):
    return render(request, 'TZ/ListProductWithAddToCartCheckoutOrder.html')



def protected_api(request):
    token = request.GET.get('token')
    if not token:
        return JsonResponse({'error': 'Token is required'}, status=400)

    if not AccessToken.objects.filter(token=token, is_active=True).exists():
        return JsonResponse({'error': 'Invalid or inactive token'}, status=403)
    
    # Query all items
    items = Item.objects.all().values('id', 'name', 'description', 'price')
    return JsonResponse({'items': ProductList(items)})




# Helper: Common context for all views
def get_common_context():
    links = list(FooterLink.objects.all())
    about_links = links[:3]
    customer_links = links[3:6]

    return {
        'Menus': Menu.objects.annotate( sub_count=Count('submenus')).order_by('MenuOrder'),        
        'SubMenus': SubMenu.objects.all(),
        'topBanner': TopBanner.objects.first(),
        'sliders': Slide.objects.all(),
        'footers': Footer.objects.all(),
        'links': links,
        'about_links': about_links,
        'customer_links': customer_links,
    }


def IndexTZ(request):
    context = get_common_context()
    context.update({
        'new_arrivals': NewArrivals.objects.all(),
        'popular_items': PopularItems.objects.all(),
        'gallerys': Gallery.objects.all(),
    })
    return render(request, 'TZ/index.html', context)


def ShopTZ(request):
    context = get_common_context()

    shop_banner = PageBanner.objects.filter(
        PageName='shop'
    ).first()

    context.update({
        'lip_gloss': ProductList.objects.filter(
            ProCategoryID__CategoryName__iexact='Lip Gloss'
        ),

        'blush': ProductList.objects.filter(
            ProCategoryID__CategoryName__iexact='Blush'
        ),

        'lip_liner': ProductList.objects.filter(
            ProCategoryID__CategoryName__iexact='Lip Line'
        ),

        'shimmer': ProductList.objects.filter(
            ProCategoryID__CategoryName__iexact='Shimmer'
        ),

        'shop_banner': shop_banner,
    })

    return render(request, 'TZ/shop.html', context)


def AboutTZ(request):
    context = get_common_context()

    about_banner = PageBanner.objects.filter(
        PageName='about'
    ).first()

    context.update({
        'abtus': AboutUs.objects.all(),
        'about_banner': about_banner,
    })

    return render(request, 'TZ/about.html', context)


def PrivacyTZ(request):
    context = get_common_context()
    context.update({
        'privacys': Privacy.objects.all(),
    })
    return render(request, 'TZ/PrivacyPolicy.html', context)




def ProDetailTZ(request, type, id):
    if type == 'new':
        product = get_object_or_404(NewArrivals, id=id)
        prodetail = ProductDetail.objects.filter(new_arrival_ID=product).first()
    elif type == 'popular':
        product = get_object_or_404(PopularItems, id=id)
        prodetail = ProductDetail.objects.filter(popular_item_ID=product).first()
    elif type == 'list':
        product = get_object_or_404(ProductList, id=id)
        prodetail = ProductDetail.objects.filter(ProListID=product).first()
    else:
        return render(request, '404.html')

    context = get_common_context()
    context.update({
        'product': product,      # Main product info (name, price, image, etc.)
        'prodetail': prodetail,  # Extra product detail (descriptions)
        'type': type,
    })
    return render(request, 'TZ/product_details.html', context)






def BlogTZ(request):
    context = get_common_context()

    blog_banner = PageBanner.objects.filter(
        PageName='blog'
    ).first()

    context.update({
        'blogs': Blog.objects.all(),
        'blog_banner': blog_banner,
    })

    return render(request, 'TZ/blog.html', context)


def BlogDetailTZ(request, blog_id):
    context = get_common_context()
    try:
        blog = Blog.objects.get(id=blog_id)
        blog_detail = blog.detail
    except Blog.DoesNotExist:
        blog = None
        blog_detail = None
    except BlogDetails.DoesNotExist:
        blog_detail = None

    context.update({
        'blog': blog,
        'blogdetail': blog_detail,
    })
    return render(request, 'TZ/blog-details.html', context)

def LoginTZ(request):

    if request.user.is_authenticated:
        return redirect('ProfileTZ')

    context = get_common_context()

    if request.method == 'POST':

        username = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('ProfileTZ')

        else:

            context['error'] = 'Invalid username or password'

    return render(
        request,
        'TZ/login.html',
        context
    )

def RegisterTZ(request):

    context = get_common_context()

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            context['error'] = 'Passwords do not match'
            return render(request, 'TZ/register.html', context)

        if User.objects.filter(username=username).exists():
            context['error'] = 'Username already exists'
            return render(request, 'TZ/register.html', context)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return redirect('LoginTZ')

    return render(request, 'TZ/register.html', context)


def LogoutTZ(request):

    logout(request)

    return redirect('IndexTZ')

def CartTZ(request):
    context = get_common_context()
    cart = CartItem.objects.filter(user=request.user)

    total_price = sum(item.price * item.quantity for item in cart)

    context.update({
        'cart': cart,
        'total_price': total_price,
    })
    return render(request, 'TZ/cart.html', context)




def CheckoutTZ(request):
    cart_items = CartItem.objects.filter(user=request.user)

    cart_items_data = []
    for item in cart_items:
        product = item.content_object
        product_name = getattr(product, 'ProLName', getattr(product, 'name', str(product)))

        cart_items_data.append({
            'productName': product_name,
            'price': float(item.price),
            'qty': item.quantity,
        })

    subtotal = sum(item.price * item.quantity for item in cart_items)
    shipping = 0 if subtotal > 100 else 3
    total = subtotal + shipping

    qr_codes = QRCode.objects.all()

    # Build qr_codes_data list for JS with image URLs
    qr_codes_data = []
    for qr in qr_codes:
        qr_codes_data.append({
            'id': qr.id,
            'name': qr.qrName,
            'image_url': qr.qrImage.url if qr.qrImage else '', 
        })

    context = get_common_context()
    context.update({
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'qr_codes': qr_codes,
        'cart_items_json': json.dumps(cart_items_data), 
        'qr_codes_data': json.dumps(qr_codes_data), 
    })

    return render(request, 'TZ/checkout.html', context)


def SearchTZ(request):

    query = request.GET.get('q', '')

    products = ProductList.objects.all()

    if query:
        products = ProductList.objects.filter(
            Q(ProLName__icontains=query) |
            Q(ProCategoryID__CategoryName__icontains=query)
        ).distinct()

    context = get_common_context()

    context.update({
        'query': query,
        'products': products,
    })

    return render(request, 'TZ/search.html', context)


@transaction.atomic
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('LoginTZ')

    if request.method == "POST":
        customer_name = request.POST.get("customerName")
        customer_phone = request.POST.get("customerPhone")
        customer_address = request.POST.get("customerAddress")
        customer_email = request.POST.get("customerEmail")
        qr_code_id = request.POST.get("QRCodeSelect")

        # 1️⃣ Get cart items for this user
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('CartTZ')  # No items to checkout

        # 2️⃣ Calculate total from cart
        subtotal = sum(item.price * item.quantity for item in cart_items)
        shipping = Decimal('3.00')  # instead of 10.00 (float)
        total_amount = subtotal + shipping

        # 3️⃣ Create the order
        order = Order.objects.create(

            user=request.user,

            customerName=customer_name,
            customerPhone=customer_phone,
            customerAddress=customer_address,
            customerEmail=customer_email,

            totalAmount=total_amount,
            qr_code_id=qr_code_id if qr_code_id else None,

        )


        # 4️⃣ Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                productName=str(cart_item.content_object),  
                price=cart_item.price,
                qty=cart_item.quantity
            )

        # 5️⃣ Clear the cart
        cart_items.delete()

        # 6️⃣ Redirect to confirmation
        return redirect('ConfirmationTZ', order_id=order.id)

    return redirect('CartTZ')


def ContactTZ(request):
    context = get_common_context()

    context.update({
        'contacts': ContactUs.objects.all(),
        'contact_banner': PageBanner.objects.filter(PageName='contact').first(),
    })

    return render(request, 'TZ/contact.html', context)




def ConfirmationTZ(request, order_id):
    links = list(FooterLink.objects.all())
    about_links = links[:3]
    customer_links = links[3:6]
    order = get_object_or_404(Order, id=order_id)
    subtotal = sum(item.price * item.qty for item in order.items.all())
    

    context = {
        'Menus': Menu.objects.annotate(sub_count=Count('submenus')).order_by('MenuOrder'),
        'SubMenus': SubMenu.objects.all(),
        'topBanner': TopBanner.objects.first(),
        'sliders': Slide.objects.all(),
        'footers': Footer.objects.all(),
        'links': links,
        'about_links': about_links,
        'customer_links': customer_links,
        'order': order,
        'subtotal': subtotal,
        'total': subtotal + Decimal('3.00'),
    }
    return render(request, 'TZ/confirmation.html', context)



def place_order_api(request):

    if request.method == "POST":

        try:

            data = request.POST

            # Get selected QR Code
            qr_code_id = data.get("QRCodeSelect")

            qr_code_instance = None

            if qr_code_id:

                from .models import QRCode

                qr_code_instance = QRCode.objects.filter(
                    id=qr_code_id
                ).first()

            # Create Order
            order = Order.objects.create(

                user=request.user if request.user.is_authenticated else None,

                customerName=data.get("customerName"),

                customerPhone=data.get("customerPhone"),

                customerAddress=data.get("customerAddress"),

                customerEmail=data.get("customerEmail"),

                totalAmount=data.get("totalAmount"),

                QRCodeInvoice=request.FILES.get(
                    "QRCodeInvoice"
                ),

                qr_code=qr_code_instance,

            )

            # Create Order Items
            items = json.loads(
                data.get("items", "[]")
            )

            for item in items:

                OrderItem.objects.create(

                    order=order,

                    productName=item.get(
                        "productName"
                    ),

                    price=item.get(
                        "price"
                    ),

                    qty=item.get(
                        "qty"
                    ),

                )

            return redirect(
                'ConfirmationTZ',
                order_id=order.id
            )

        except Exception as e:

            context = get_common_context()

            context.update({

                "error": str(e),

            })

            return render(
                request,
                "TZ/confirmation.html",
                context
            )

    return redirect('CheckoutTZ')








def generate_qrcode_image(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), 'qr_code.png')






def add_to_cart(request, product_type, product_id):
    if not request.user.is_authenticated:
        return redirect('LoginTZ')

    model_map = {
        'list': ProductList,
        'popular': PopularItems,
        'new': NewArrivals,
        'detail': ProductDetail,
    }

    model = model_map.get(product_type)
    if not model:
        return redirect('ShopTZ')

    product = get_object_or_404(model, id=product_id)
    content_type = ContentType.objects.get_for_model(model)

    # Get quantity from the form (default to 1 if missing)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=product_id,
        defaults={
            'quantity': quantity,
            'price': product.get_price,
        }
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('CartTZ')




def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    cart_with_products = []
    for item in cart_items:
        product = item.content_object  # This gets the actual product instance
        cart_with_products.append({
            'id': item.id,
            'product': product,
            'quantity': item.quantity,
            'price': item.price,
            'subtotal': item.price * item.quantity,
        })

    total_price = sum(item['subtotal'] for item in cart_with_products)

    topBanner = TopBanner.objects.first()
    Menus = Menu.objects.annotate(sub_count=Count('submenus')).order_by('MenuOrder')
    SubMenus = SubMenu.objects.all()
    sliders = Slide.objects.all()
    footers = Footer.objects.all()
    links = FooterLink.objects.all()

    context = {
        'sliders': sliders,
        'Menus': Menus,
        'SubMenus': SubMenus,
        'topBanner': topBanner,
        'footers': footers,
        'links': links,
        'cart': cart_with_products,
        'total_price': total_price,
    }
    return render(request, 'TZ/cart.html', context)






def remove_from_cart(request, cart_item_id):
    if request.method == "POST" and request.user.is_authenticated:
        CartItem.objects.filter(id=cart_item_id, user=request.user).delete()
    return redirect('CartTZ') 






def product_list(request):
    products = ProductList.objects.all()
    popular_items = PopularItems.objects.all()
    new_arrivals = NewArrivals.objects.all()

    context = {
        'products': products,
        'popular_items': popular_items,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'TZ/product_list_in_cart.html', context)



class ProductListViewSet(viewsets.ModelViewSet):
    queryset = ProductList.objects.all()
    serializer_class = ProductListSerializer
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # requires token

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
        queryset = super().get_queryset()
        return queryset
   


class ProductDetailViewSet(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # requires token

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
        queryset = super().get_queryset()
        return queryset
    


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # requires token

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
        queryset = super().get_queryset()
        return queryset
    

class BlogDetailViewSet(viewsets.ModelViewSet):
    queryset = BlogDetails.objects.all()
    serializer_class = BlogDetailSerializer
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # requires token

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
        queryset = super().get_queryset()
        return queryset
    


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # requires token

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
        queryset = super().get_queryset()
        return queryset




class QRCodeViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # requires token

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
        queryset = super().get_queryset()
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # requires token

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
        queryset = super().get_queryset()
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    





class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer  # create this serializer if not created
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
        queryset = super().get_queryset()
        return queryset
    

class TopBannerView(viewsets.ModelViewSet):
    queryset = TopBanner.objects.all()
    serializer_class = TopBannerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
        queryset = super().get_queryset()
        return queryset
    



class MenuView(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
        queryset = super().get_queryset()
        return queryset
    



class SubMenuView(viewsets.ModelViewSet):
    queryset = SubMenu.objects.all()
    serializer_class = SubMenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
        queryset = super().get_queryset()
        return queryset
    

from django.contrib.auth.decorators import login_required
from .models import UserProfile, Order, CartItem
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def ProfileTZ(request):

    context = get_common_context()

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    total_orders = Order.objects.filter(
        user=request.user
    ).count()

    cart_count = CartItem.objects.filter(
        user=request.user
    ).count()

    member_since = request.user.date_joined.year

    recent_orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')[:5]

    context.update({

        'user_profile': request.user,

        'profile': profile,

        'total_orders': total_orders,

        'cart_count': cart_count,

        'member_since': member_since,

        'recent_orders': recent_orders,

    })

    return render(
        request,
        'TZ/profile.html',
        context
    )

@login_required
def OrderDetailTZ(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order_items = OrderItem.objects.filter(
        order=order
    )

    context = get_common_context()

    context.update({
        'order': order,
        'order_items': order_items,
    })

    return render(
        request,
        'TZ/order_detail.html',
        context
    )


@login_required
def EditProfileTZ(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        if request.FILES.get('avatar'):

            profile.avatar = request.FILES['avatar']
            profile.save()

        return redirect('ProfileTZ')

    return render(
        request,
        'TZ/edit_profile.html',
        {
            'profile': profile
        }
    )


from django.contrib.auth.decorators import login_required

@login_required(login_url='LoginTZ')
def MyOrdersTZ(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')

    context = get_common_context()

    context.update({
        'orders': orders
    })

    return render(
        request,
        'TZ/my_orders.html',
        context
    )