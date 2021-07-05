from django.urls import include, path
from rest_framework import routers
from shopapi import views
from .views import *
from .api import RegisterApi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



urlpatterns = [
    path('token/', LoginView.as_view(), name='token'),
    path('register/', RegisterApi.as_view(), name='register-test'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', MyTokenRefreshView.as_view(), name='token_refresh'),
    
    path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
    path('category/', CategoryParamAPIView.as_view(), name='category'),
    path('category/<int:id>/', CategoryAPIView.as_view(), name='category_id'),

    path('product/', ProductParamAPIView.as_view(), name='product'),
    path('product/<int:id>/', ProductAPIView.as_view(), name='product_id'),

    path('cart/', CartAPIView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartEditAPIView.as_view(), name='cart-edit'),
    
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    
    path('invoice/', InvoiceAPIView.as_view(), name='invoice'),
    path('invoice/<int:id>/', InvoiceitemAPIView.as_view(), name='invoice-id'),

    path('invoice/<int:pk>/void/', Invoice_voidAPIView.as_view(), name='invoice-id'),
]