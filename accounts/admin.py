from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(TopBanner)
admin.site.register(Menu)
admin.site.register(SubMenu)

admin.site.register(Slide)

admin.site.register(NewArrivals)
class NewArrivalsAdmin(admin.ModelAdmin):
    list_display = ('ProCategoryID', 'NewAName', 'NewAPrice')
    fields = ('NewAName', 'NewAPrice', 'NewAImage', 'NewADescription', 'NewADetail')

admin.site.register(PopularItems)
class PopularItemsAdmin(admin.ModelAdmin):
    list_display = ('ProCategoryID', 'PopIName', 'PopIPrice')
    fields = ('PopIName', 'PopIPrice', 'PopIImage', 'PopIDescription', 'PopIDetail')

admin.site.register(ProductCategory)

admin.site.register(ProductList)
class ProductListAdmin(admin.ModelAdmin):
    list_display = ('ProCategoryID', 'ProLName', 'ProLPrice')
    fields = ('ProLName', 'ProLPrice', 'ProCategoryID', 'ProLImage', 'ProLDescription', 'ProLDetail')

admin.site.register(ProductDetail)
admin.site.register(Blog)
admin.site.register(BlogDetails)
admin.site.register(ContactUs)
admin.site.register(AboutUs)
admin.site.register(Footer)
admin.site.register(FooterLink)
admin.site.register(QRCode)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(AccessToken)
admin.site.register(CartItem)
admin.site.register(Gallery)
admin.site.register(Privacy)


