from django.shortcuts import render
import django_filters.rest_framework
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, generics, mixins, permissions
from rest_framework.mixins import DestroyModelMixin
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
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied,NotFound,ValidationError,ParseError
from decimal import *

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
class ResponseCart(object):
    def __init__(self, user=None, **args):
        self.response = {
            "msg": args.get('msg', 'บันทึกข้อมูลสำเร็จ'),
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

    

    def get(self, request,id, *args,  **kwargs):
        # print("tset")
        # try:
        #     print("tset1")
        #     categ_list = Category.objects.get(id=id)
        #     print("tset2")
           
        # except:
        #     print("tset3")
        #     raise ValidationError({  
        #         "code": "HTTP_404_NOT_FOUND",
        #         "msg": "ไม่พบข้อมูล"
        #         }) 
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
                # return self.list(request)
    

   
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
                print(list_in)
        # add param to list_not_in
        if category_not_in :
            for categ_not_in in category_not_in.split(","):
                list_not_in.append(int(categ_not_in))

   

        # filter category_in
        if category_in :
            queryset = queryset.filter(category__in=list_in)
            print(queryset)
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
    pagination_class = CustomPagination
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

class CartAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    # queryset = Cart.objects.all()      
    serializer_class = CartSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def __init__(self, **kwargs):
        self.response_format = ResponseCategory().response
        super(CartAPIView, self).__init__(**kwargs)


    def get(self, request, *args,  **kwargs):
        user_id = self.request.user
        user = User.objects.get(username=user_id)
        response_data = super(CartAPIView, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        self.response_format["user"] = user.username
        self.response_format["status"] = status.HTTP_200_OK
        if not response_data.data:
            self.response_format["message"] = "List empty"
        return Response(self.response_format)
    
        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        # user_id = self.request.user
        # user = User.objects.get(username=user_id)
        # print(serializer.is_valid())
        # if serializer.is_valid(raise_exception=True):
        
        if serializer.is_valid():
           
            data = {}

            print(serializer['cart_product'])
            product_id = self.request.data['cart_product']
            # product_id = int(serializer.data['product'])
            products = Product.objects.get(pk=int(product_id))
        
            user_id = self.request.user
            
            user = User.objects.get(username=user_id)

            quantities = int(serializer.data['quantity'])
            item = Cart.objects.filter(user=user,cart_product=products.id).first()
            
            if item:

                item.quantity += quantities

                mul = quantities*products.price
                item.total += mul
            
                item.save()
            else:

                item = Cart.objects.create(cart_product=products,user=user,quantity=quantities,total=quantities*products.price)
                item.save()
                # item = Cart.objects.filter(user=user)
            data['id'] = item.id
            data['user'] = user.username
            data['product'] = item.cart_product.name
            data['product_id'] = item.cart_product.id
            data['quantity'] = item.quantity
            data['total'] = item.total
            return Response({
                "msg":"บันทึกสำเร็จ",
                "data":data,
                },status=status.HTTP_201_CREATED)
            # print(int(item.quantity))
            # if item.quantity == 0:

            # response_data = super(CartAPIView, self).list(request, *args, **kwargs)
            # self.response_format["data"] = response_data.data
            # self.response_format["user"] = user.username
            # # print(response_data.data)
            # self.response_format["status"] = True
            # if not response_data.data:
            #     self.response_format["message"] = "List empty"
            # return Response(self.response_format)
        else:
            
            return Response({
                "code" : "ADD TO CART FAIL",
                "msg" : "บันทึกไม่สำเร็จ",
                "error" : [serializer.errors]

            },status=status.HTTP_400_BAD_REQUEST)
    
    


# class CartEditAPIView(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
class CartEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartEditSerializer
    queryset = Cart.objects.all()    
    permission_classes = [permissions.IsAuthenticated] 
    
    # lookup_field = 'id'                  

    def destroy(self, request, *args, **kwargs):
        print(kwargs)
        current_user = self.request.user
        try:
            instance = self.get_object()
            cart_user = Cart.objects.get(pk=kwargs['pk']).user
            
        except:
            raise NotFound()
        
        if cart_user != current_user:
            return Response({
                "code":"HTTP_403_FORBIDDEN",
                "msg":"ไม่มีสิทธิ์การใช้งาน"
            },status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)

        return Response({
            "msg": "ลบข้อมูลสำเร็จ"
        },status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        permission_classes = [permissions.IsAuthenticated]
        queryset = Cart.objects.all()
        serializer_class = CartEditSerializer

        try:
            cartlist = Cart.objects.get(id=pk)
        except:
            raise NotFound()
        if cartlist.quantity == 0:
            cartlist.delete()   
            return Response({
                "msg": "ลบข้อมูลสำเร็จ"
            },status=status.HTTP_200_OK)
        data = request.data
        cartlist.total = int(data['quantity'])*(cartlist.cart_product.price)
        cartlist.quantity = data['quantity']
        cartlist.save()
        return Response(
            {
                "msg": "บันทึกข้อมูลสำเร็จ",
                "data": [(CartSerializer(cartlist).data)],
            }
        )

class CheckoutAPIView(generics.CreateAPIView):
    serializer_class = CheckoutSerializer
    queryset = Cart.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    # invoice = Invoice.objects.all()
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data ={}
        carts = Cart.objects.filter(user=self.request.user) 
        sum_total=0
        print(len(carts))
        if len(carts)!=0:
            for i in carts:
            
                if not i.cart_product.is_enabled:
                    return Response({
                "code": "CHECKOUT_FAIL",
                "msg": "มีสินค้าบางรายการไม่สามารถสั่งซื้อได้",
                },status=status.HTTP_400_BAD_REQUEST)
                else:
                    sum_total += i.total
                    
            invoices = Invoice.objects.create(iv_user=self.request.user,total=sum_total)


            print(invoices)
            if invoices:
                invoices.save()
                for item in carts:
                    invoice_items = Invoice_item.objects.create(iv_product=item.cart_product,invoice=invoices,quantity=item.quantity,total=sum_total)
                    if invoice_items:
                        invoice_items.save()
                        item.delete()
            else:
                return Response({
                "msg":"ไม่มีใบสั่งซื้อสินค้า",
                "code": "CHECKOUT_FAIL",
            },status=status.HTTP_400_BAD_REQUEST)
            data['id']=invoices.id
            return Response({
                "msg":"สร้างรายการสั่งซื้อสำเร็จ",
                "id": data
            })
        else:
            return Response({
            "code": "CART_EMPTY",
            "msg": "กรุณาเลือกสินค้าใส่ตะกร้า",
            },status=status.HTTP_400_BAD_REQUEST)

# class InvoiceAPIView(generics.GenericAPIView, mixins.ListModelMixin):
class InvoiceAPIView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    permission_classes = [permissions.IsAuthenticated] 
    def get_queryset(self):
        return Invoice.objects.filter(iv_user=self.request.user)

    def __init__(self, **kwargs):
        self.response_format = ResponseCategory().response
        super(InvoiceAPIView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        # queryset = Invoice.objects.filter(user=self.request.iv_user)
        
        response_data = super(InvoiceAPIView, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        self.response_format["status"] = 200
        if not response_data.data:
            self.response_format["message"] = "List empty"
        return Response(self.response_format)


        

class InvoiceitemAPIView(generics.RetrieveAPIView):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated] 
    def get_queryset(self):
        return Invoice.objects.filter(iv_user=self.request.user)
        

    def __init__(self, **kwargs):
        self.response_format = ResponseCategory().response
        super(InvoiceitemAPIView, self).__init__(**kwargs)

    def get(self, request, id, *args, **kwargs):
        
        response_data = super(InvoiceitemAPIView, self).retrieve(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        self.response_format["status"] = 200
        if not response_data.data:
            self.response_format["message"] = "List empty"
        return Response(self.response_format)


class Invoice_voidAPIView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            invoices = Invoice.objects.get(id=pk)
        except:
            raise NotFound()
        # data = request.data
        if invoices.status == "S":
            return Response({
                "code": "VOID_INVOICE_FAIL",
                "msg": "ยกเลิกรายการไม่สำเร็จเนื่องจากอยู่ในสถานะ ชำระเงินแล้ว"
            },status=status.HTTP_400_BAD_REQUEST)
        if invoices.status == "C":
            return Response({
                "code": "VOIDED",
                "msg": "รายการสินค้านี้อยู่ในสถานะ 'ยกเลิก' รายการแล้ว"
            },status=status.HTTP_400_BAD_REQUEST)
        invoices.status = "C"
        invoices.save()
        return Response({
            "msg" : "ยกเลิกรายการสำเร็จ",
        },status=status.HTTP_200_OK)

        