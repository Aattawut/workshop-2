from django.contrib import admin
from .models import Category, Product, Product_image, Cart, Invoice, Invoice_item

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name','detail','is_enabled','image']

class ProductImageAdmin(admin.StackedInline):
    model = Product_image
    extra = 2
    # list_display = ['img_product','image']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['id','category','name','detail','price','is_enabled','image']
    inlines = [ProductImageAdmin]

class ProductImageAdmin(admin.ModelAdmin):
    # model = Product_image
    list_display = ['image']

class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ['id','cart_product','user','quantity','total']
    

class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    list_display = ['id','iv_user','created_datetime','updated_datetime','total','status']

class InvoiceItemAdmin(admin.ModelAdmin):
    model = Invoice_item
    list_display = ['iv_product','invoice','created_datetime','quantity','total']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Product_image, ProductImageAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Invoice_item, InvoiceItemAdmin)