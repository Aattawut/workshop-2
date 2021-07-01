from django.shortcuts import render
import django_filters.rest_framework
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins, permissions
from rest_framework.views import APIView
from .serializers import *
from .models import *
import django_filters.rest_framework
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from .paginations import CustomPagination
from rest_framework import filters
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register': reverse('register-test', request=request, format=format),
        'category': reverse('category', request=request, format=format),
   
    })

# class APIRoot(generics.GenericAPIView):

class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer



class MyTokenRefreshView(TokenObtainPairView):
    serializer_class = TokenRefreshLifetimeSerializer


class ResponseCategory(object):
    def __init__(self, user=None, **args):
        self.response = {
            "msg": args.get('msg', 'ดึงข้อมูลสำเร็จ'),
            "data": args.get('data', []),
 
        }


class CategoryParamAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filterset_fields = ['is_enabled']
    pagination_class = CustomPagination
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def __init__(self, **kwargs):
        self.response_format = ResponseCategory().response
        super(CategoryParamAPIView, self).__init__(**kwargs)

    def get(self, request, *args,  **kwargs):
        response_data = super(CategoryParamAPIView, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        self.response_format["status"] = True
        if not response_data.data:
            self.response_format["message"] = "List empty"
        return Response(self.response_format)
        # data = self.list(request)
        # return data
       


class CategoryAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    # search_fields = ['id','name']
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    
    def __init__(self, **kwargs):
        self.response_format = ResponseCategory().response
        super(CategoryAPIView, self).__init__(**kwargs)

    

    def get(self, request,id=None, *args,  **kwargs):
        if id:
            response_data = super(CategoryAPIView, self).retrieve(request, *args, **kwargs)
            self.response_format["data"] = response_data.data
            self.response_format["status"] = 200
            if not response_data.data:
                self.response_format["message"] = "List empty"
            return Response(self.response_format)
        
            # return self.retrieve(request)
        elif id == 0:
            response_data = super(CategoryAPIView, self).list(request, *args, **kwargs)
            self.response_format["data"] = response_data.data
            self.response_format["status"] = 200
            if not response_data.data:
                self.response_format["message"] = "List empty"
            return Response(self.response_format)
        #     return self.list(request)
       

    # query_id = self.request.query_params.get('sort','asc')

# class ProductParamAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
class ProductParamAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filterset_fields = ['is_enabled']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['id','name','detail']
    ordering_fields = ['id','name','price']
    pagination_class = CustomPagination
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]



    def get_queryset(self, *args,  **kwargs):
        queryset = Product.objects.all()
        # data = self.list(request)
        sort_by = self.request.query_params.get('sort','asc')

        category_in = self.request.query_params.get('category__in', None)
        category_not_in = self.request.query_params.get('category_not__in', None)

        list_in = []
        list_not_in = []
        # add param to list_in
        if category_in :
            for categ_in in category_in.split(","):
                list_in.append(int(categ_in))
        # add param to list_not_in
        if category_not_in :
            for categ_not_in in category_not_in.split(","):
                list_not_in.append(int(categ_not_in))

        # filter category_in
        if category_in :
            queryset = queryset.filter(category__in=list_in)
        # filter category_not_in
        if category_not_in :
            queryset = queryset.exclude(category__in=list_not_in)

        # sort 
        if sort_by == 'desc':
            queryset = queryset.order_by('-price')
            # print('1')
            # print(queryset)
            # return self.list(querysett)

        else:
            querysett = queryset.order_by('price')
            # print(queryset)
            # print('2')
            # return self.list(queryset)
        return queryset
        
    def __init__(self, **kwargs):
        self.response_format = ResponseCategory().response
        super(ProductParamAPIView, self).__init__(**kwargs)
    
    def get(self, request, *args,  **kwargs):
        response_data = super(ProductParamAPIView, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        self.response_format["status"] = 200
        if not response_data.data:
            self.response_format["message"] = "List empty"
        return Response(self.response_format)
       
       

class ProductAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def __init__(self, **kwargs):
        self.response_format = ResponseCategory().response
        super(ProductAPIView, self).__init__(**kwargs)

    def get(self,request, id=None, *args,  **kwargs):
        if id:
            response_data = super(ProductAPIView, self).retrieve(request, *args, **kwargs)
            self.response_format["data"] = response_data.data
            self.response_format["status"] = 200
            if not response_data.data:
                self.response_format["message"] = "List empty"
            return Response(self.response_format)
        
            # return self.retrieve(request)
        else:
            response_data = super(ProductAPIView, self).list(request, *args, **kwargs)
            self.response_format["data"] = response_data.data
            self.response_format["status"] = 200
            if not response_data.data:
                self.response_format["message"] = "List empty"
            return Response(self.response_format)
        #     return self.list(request)
       
        # if id:
        #     return self.retrieve(request)
        # else:
        #     return self.list(request)
class CartAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    serializer_class = CartSerializer
    queryset = Cart.objects.all()      