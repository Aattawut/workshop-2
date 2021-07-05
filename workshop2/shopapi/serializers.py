from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product, Product_image, Cart, Invoice, Invoice_item

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied,NotFound,ValidationError,ParseError
from versatileimagefield.serializers import VersatileImageFieldSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TokenObtainPairSerializer(TokenObtainPairSerializer):

    # default_error_messages = {
    #     'no_active_account': 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
    # }

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            # print(data)
            token = self.get_token(self.user)
            # print(token)  
            # data['user'] = str(self.user)
            # data['id'] = self.user.id

            data['token_type'] = str(token.access_token.token_type)
            data['expires_in'] = int(token.access_token.lifetime.total_seconds())
            return data
        except:
            raise ParseError({'msg':'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง',"code": "LOGIN_FAIL"}) 
        return data
        


class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            refresh = RefreshToken(attrs['refresh'])
            data['access'] = str(refresh.access_token)
            data['token_type'] = str(refresh.access_token.token_type)
            data['refresh'] = str(refresh)
            data['token_type2'] = str(refresh.token_type)
            data['expires_in'] = int(refresh.access_token.lifetime.total_seconds())
            return data
        except:
            raise ParseError({'msg':'Refresh Token ไม่ถูกต้อง',"code": "REFRESH_TOKEN_FAIL"}) 
        return data

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','password')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    
    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError("รหัสผ่านต้องมากกว่า 8 ตัวอักษร")
        return password
     
            


    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
        password = validated_data['password'] ,
        first_name = validated_data['first_name'],
        last_name = validated_data['last_name'])
        
        return user

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Category serializer
class CategorySerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__50x50')
        ]
    )
    class Meta:
        model = Category
        fields = '__all__'

# Product Image serializer
class ProductImageSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__50x50')
        ]
    )
    class Meta:
        model = Product_image
        fields = ['id','image']


# Product serializer
class ProductSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__50x50')
        ]
    )
    # image_product = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id','category','name','price','detail','image','is_enabled']

# Product serializer2
class ProductDetailSerializer(serializers.ModelSerializer):
    image_product = ProductImageSerializer(many=True, read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__50x50')
        ]
    )
    class Meta:
        model = Product
        fields = ['id','category','name','price','detail','image','is_enabled','image_product']

class ProductHyperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'



class CartSerializer(serializers.ModelSerializer):

    cart_product = serializers.CharField(max_length=10, error_messages={"blank": "กรุณากรอกรหัสสินค้า"})
    quantity = serializers.IntegerField(error_messages={"blank": "จำนวนสินค้านี้ต้องมากกว่า 0"})
  
    class Meta:
        model = Cart
        fields =  ['cart_product','quantity','total','user']

    def validate_cart_product(self, cart_product):
        try:
            is_enableds = Product.objects.get(pk = int(cart_product))
        except:
            raise ValidationError('ไม่พบสินค้าชิ้นนี้')
        
        if not is_enableds.is_enabled:
            raise ValidationError('สินค้านี้ถูกปิดการใช้งาน')
        return cart_product
    
    def validate_quantity(self, quantity):
        if quantity == 0:
            raise ValidationError('สำนวนสินค้าต้องมากกว่า 0 ชิ้น')

        return quantity
    
class CartEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['cart_product','quantity','total']

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class InvoiceitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice_item
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_item = InvoiceitemSerializer(many=True)
    class Meta:
        model = Invoice
        fields = ['iv_user','created_datetime','updated_datetime','total','status','invoice_item']
