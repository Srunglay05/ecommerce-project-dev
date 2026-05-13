from decimal import Decimal, InvalidOperation
from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import NoReverseMatch, reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.core.files.base import ContentFile
import qrcode



# Create your models here.


class AccessToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.token
    

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name






class TopBanner(models.Model):
    Logo= models.ImageField(upload_to='Logo/', null=True, blank=True)
    def __str__(self):
        return f'{self.id} --> {self.Logo}'


class Gallery(models.Model):
    GallImage = models.ImageField(upload_to='Gallery/', null=True, blank=True)
    def __str__(self):
        return f'{self.id} -> {self.GallImage}'



class Menu(models.Model):
    MenuName = models.CharField(max_length=200, null=False, default='Menu')
    url_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.MenuName}'

    @property
    def url(self):
        if not self.url_name:
            return '#'
        try:
            return reverse(self.url_name)
        except NoReverseMatch:
            return '#'


class SubMenu(models.Model):
    SubMenuName = models.CharField(max_length=200, null=True)
    MenuID = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, related_name='submenus')
    url_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.MenuID.MenuName} -> {self.SubMenuName}'

    @property
    def url(self):
        if not self.url_name:
            return '#'
        try:
            return reverse(self.url_name)
        except NoReverseMatch:
            return '#'


class Slide(models.Model):
    SlideName = models.CharField(max_length=200,null=True)
    SildeHead = RichTextUploadingField(null=True)
    SlideBody = RichTextUploadingField(null=True)
    SlideImage = models.ImageField(upload_to='SlideImage/', null=True, blank=True)
    def __str__(self):
            return f'{self.id} -> {self.SlideName}'

class ProductCategory(models.Model):
    CategoryName = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.id} -> {self.CategoryName}'


class NewArrivals(models.Model):
    ProCategoryID = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    NewAImage = models.ImageField(upload_to='ProvideImage/', null=True, blank=True)
    NewAName = models.CharField(max_length=200, null=True)
    NewAPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def get_price(self):
        return Decimal(self.NewAPrice or 0)

    @property
    def get_name(self):
        return self.NewAName or ''

    @property
    def get_image(self):
        return self.NewAImage.url if self.NewAImage else None
    
    def __str__(self):
            return f'{self.NewAName}'



class PopularItems(models.Model):
    ProCategoryID = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    PopIImage = models.ImageField(upload_to='ProvideImage/', null=True, blank=True)
    PopIName = models.CharField(max_length=200, null=True)
    PopIPrice =  models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def get_price(self):
        return Decimal(self.PopIPrice or 0)

    @property
    def get_name(self):
        return self.PopIName or ''

    @property
    def get_image(self):
        return self.PopIImage.url if self.PopIImage else None
    
    def __str__(self):
            return f'{self.PopIName}'


class ProductList(models.Model):
    ProCategoryID = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    ProLName = models.CharField(max_length=200, null=True, blank=True)
    ProLImage = models.ImageField(upload_to='ProLImage/', null=True, blank=True)
    ProLPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def get_price(self):
        return Decimal(self.ProLPrice or 0)

    @property
    def get_name(self):
        return self.ProLName or ''

    @property
    def get_image(self):
        return self.ProLImage.url if self.ProLImage else None
    
    def __str__(self):
            return f'{self.ProLName}'



class ProductDetail(models.Model):
    popular_item_ID  = models.ForeignKey(PopularItems, on_delete=models.CASCADE, null=True, blank=True)
    new_arrival_ID = models.ForeignKey(NewArrivals, on_delete=models.CASCADE, null=True, blank=True)
    ProListID = models.ForeignKey(ProductList, on_delete=models.CASCADE, null=True, blank=True)
    ProDeImage = models.ImageField(upload_to='ProLImage/', null=True, blank=True)
    ProDeName = models.CharField(max_length=200,null=True, blank=True)
    ProDePrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Pro_detail_description_1 = RichTextUploadingField(null=True, blank=True)
    Pro_detail_description_2 = RichTextUploadingField(null=True,blank=True)
    def __str__(self):
            return f'{self.id} -> {self.ProDeName} -> {self.ProDePrice}'




class Blog(models.Model):
    BlogImage = models.ImageField(upload_to='BlogImage/', null=True, blank=True)
    BlogName = models.CharField(max_length=200, null=True)
    BlogDateDay = models.CharField(max_length=200, null=True)
    BlogDateMonth = models.CharField(max_length=200, null=True)
    Blogdescription = RichTextUploadingField(null=True)
    BlogRate = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.id} -> {self.BlogName} -> {self.BlogImage}'


class BlogDetails(models.Model):
    BlogID = models.OneToOneField(Blog, on_delete=models.CASCADE, null=True, related_name='detail')
    BlogDeName = models.CharField(max_length=200, null=True)
    BlogDeImage = models.ImageField(upload_to='BlogImage/', null=True, blank=True)
    BlogDeDescription = RichTextUploadingField(null=True)
    BlogDeRate = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.id} -> {self.BlogDeName} -> {self.BlogDeImage}'  
 

class ContactUs(models.Model):
    Description_1 = models.CharField(max_length=500,null=True)
    Address = models.CharField(max_length=500,null=True, blank=True)
    Description_2 = models.CharField(max_length=500,null=True)
    PhoneNum = models.CharField(max_length=200,null=True, blank=True)
    Description_3 = models.CharField(max_length=500,null=True)
    Email = models.CharField(max_length=200,null=True, blank=True)
    def __str__(self):
            return f'{self.id} -> {self.Address} -> {self.PhoneNum} -> {self.Email} '
 


class AboutUs(models.Model):
    Title_1 = models.CharField(max_length=200,null=True)
    Description_1 = RichTextUploadingField(null=True)
    Title_2 = models.CharField(max_length=200,null=True)
    Description_2 = RichTextUploadingField(null=True)
    def __str__(self):
            return f'{self.id} -> {self.Title_1} -> {self.Description_1} /n {self.Title_2} -> {self.Description_2}'
 


class Privacy(models.Model):
    Title_1 = models.CharField(max_length=200,null=True)
    Description_1 = RichTextUploadingField(null=True)
    Title_2 = models.CharField(max_length=200,null=True)
    Description_2 = RichTextUploadingField(null=True)
    def __str__(self):
            return f'{self.id} -> {self.Title_1} -> {self.Description_1} /n {self.Title_2} -> {self.Description_2}'



class Footer(models.Model):
    Footer_image = models.ImageField(upload_to='footer_images/', null=True, blank=True)

    def __str__(self):
        return f'{self.id} --> {self.Footer_image}'



class FooterLink(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)              
    url_name = models.CharField(max_length=100, null=True, blank=True)         
    def __str__(self):
        return self.name

    @property
    def url(self):
        try:
            return reverse(self.url_name)
        except NoReverseMatch:
            return '#'


    

class QRCode(models.Model):
    qrName = models.CharField(max_length=100)
    qrImage = models.ImageField(upload_to='images/qrcodes/')

    def __str__(self): return self.qrName

    

class Order(models.Model):
    customerName = models.CharField(max_length=255, null=True)
    customerPhone = models.CharField(max_length=20, null=True)
    customerAddress = models.CharField(max_length=555, null=True)
    customerEmail = models.CharField(max_length=555, null=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    qr_code = models.ForeignKey(QRCode, on_delete=models.SET_NULL, null=True, blank=True)
    QRCodeInvoice = models.ImageField(upload_to='qrcodes/', null=True, blank=True)

    def generate_qrcode(self):
        qr_data = f"Order ID: {self.id}\nCustomer: {self.customerName}\nTotal: {self.totalAmount}"
        qr_img = qrcode.make(qr_data)

        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        file_name = f"order_{self.id}_qr.png"
        self.QRCodeInvoice.save(file_name, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save to get an ID if new

        if is_new:
            self.generate_qrcode()
            super().save(update_fields=['QRCodeInvoice'])

    def __str__(self): return f'{self.customerName} --> {self.customerPhone} --> {self.customerAddress} --> {self.customerEmail} '



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    productName = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField()

    def __str__(self): return f'{self.order} --> {self.productName} --> {self.price} --> {self.qty} '



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    @property
    def image_url(self):
        obj = self.content_object
        if not obj:
            return None
        
        # Try known image fields in order
        for field in ['NewAImage', 'PopIImage', 'ProLImage', 'ProDeImage']:
            if hasattr(obj, field):
                img = getattr(obj, field)
                if img and hasattr(img, 'url'):
                    return img.url
        return None

    @property
    def product_name(self):
        obj = self.content_object
        if not obj:
            return ''
        for field in ['NewAName', 'PopIName', 'ProLName', 'ProDeName']:
            if hasattr(obj, field):
                name = getattr(obj, field)
                if name:
                    return name
        return ''
    
    @property
    def subtotal(self):
        return self.price * self.quantity
    