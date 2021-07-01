from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product, Product_image, Cart

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
from rest_framework.exceptions import AuthenticationFailed


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
            raise AuthenticationFailed({'msg':'ชื่อผู้ใช้เเละรหัสผ่านไม่ถูกต้อง',"code": "LOGIN_FAIL"}, 400) 
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
            raise AuthenticationFailed({'msg':'Refresh Token ไม่ถูกต้อง',"code": "REFRESH_TOKEN_FAIL"}, 400) 
        return data

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','password')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    
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
 
    class Meta:
        model = Category
        fields = '__all__'

# Product Image serializer
class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product_image
        fields = ['id','image']


# Product serializer
class ProductSerializer(serializers.ModelSerializer):
    # image_product = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id','category','name','price','detail','image','is_enabled']

# Product serializer2
class ProductDetailSerializer(serializers.ModelSerializer):
    image_product = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id','category','name','price','detail','image','is_enabled','image_product']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
