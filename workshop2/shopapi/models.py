from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CHOICE_STATUS = (
    ('W','waiting for delivery'),
    ('S','Shipped '),
    ('C','Cancel')
)
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='upload', null=True, blank=True)
    detail = models.TextField(null=True, blank=True, max_length=255)
    is_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category ,default=None,blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    detail = models.TextField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to='upload', null=True, blank=True)
    is_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Product'

    def __str__(self):
        return self.name

class Product_image(models.Model):
    img_product = models.ForeignKey(Product ,default=None, related_name='image_product', on_delete=models.CASCADE)
    image = models.FileField(upload_to='upload', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Product Image'

  
class Cart(models.Model):
    cart_product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2,default=0)

    class Meta:
        verbose_name_plural = 'Cart'
    def __int__(self):
        return self.quantity

class Invoice(models.Model):
    iv_user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=6, decimal_places=2,default=0)
    status = models.CharField(max_length=5, null=True, blank=True, choices=CHOICE_STATUS)

    def __str__(self):
        return self.iv_user

class Invoice_item(models.Model):
    iv_product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, default=None, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2,default=0)

    def __str__(self):
        return self.iv_product
