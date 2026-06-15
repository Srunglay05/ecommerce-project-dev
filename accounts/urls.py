from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'Product_List', ProductListViewSet)
router.register(r'Product_Detail', ProductDetailViewSet)
router.register(r'blog', BlogViewSet)
router.register(r'blog_Detail', BlogDetailViewSet)
router.register(r'product_Category', CategoryViewSet)
router.register('qr_codes', QRCodeViewSet)
router.register('orders', OrderViewSet)
router.register(r'Add_tocart', CartItemViewSet)
router.register(r'topbanner', TopBannerView)
router.register(r'menus', MenuView)
router.register(r'submenus', SubMenuView)



urlpatterns = [

    
    path('API/', include(router.urls)),

    path('data/', protected_api),

    path('', views.IndexTZ, name='IndexTZ'),

    path('ShopTZ/', ShopTZ, name='ShopTZ'),

    path('AboutTZ/', views.AboutTZ, name='AboutTZ'),

    path('PrivacyTZ/', views.PrivacyTZ, name='PrivacyTZ'),

    path('product/<str:type>/<int:id>/', views.ProDetailTZ, name='ProDetailTZ'),

    path('BlogTZ/', views.BlogTZ, name='BlogTZ'),

    path('BlogDetailTZ/<int:blog_id>/', views.BlogDetailTZ, name='BlogDetailTZ'),

    path('LoginTZ/', views.LoginTZ, name='LoginTZ'),

    path('RegisterTZ/', views.RegisterTZ, name='RegisterTZ'),

    path('ProfileTZ/', views.ProfileTZ, name='ProfileTZ'),

    path('EditProfileTZ/', views.EditProfileTZ, name='EditProfileTZ'),

    path('MyOrdersTZ/', views.MyOrdersTZ, name='MyOrdersTZ'),

    path('OrderDetailTZ/<int:order_id>/', views.OrderDetailTZ, name='OrderDetailTZ'),

    path('LogoutTZ/', views.LogoutTZ, name='LogoutTZ'),

    path('CartTZ/', views.CartTZ, name='CartTZ'),

    path('CheckoutTZ/', views.CheckoutTZ, name='CheckoutTZ'),

    path('checkout/', views.checkout, name='checkout'),

    path('confirmation/<int:order_id>/', views.ConfirmationTZ, name='ConfirmationTZ'),

    path('SearchTZ/', views.SearchTZ, name='SearchTZ'),
    path('ContactTZ/', views.ContactTZ, name='ContactTZ'),

   
    path('CartTZ/', views.view_cart, name='view_cart'),

    path('api/add_to_cart/<str:product_type>/<int:product_id>/', add_to_cart, name='add_to_cart'),
    
    path('api/remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('cart/', views.view_cart, name='view_cart'),

    path('place_order/', views.place_order_api, name='place_order_api'),

]

# ✅ Append static URLs properly
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
