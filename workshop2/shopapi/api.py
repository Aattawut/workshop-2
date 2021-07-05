from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied,NotFound,ValidationError,ParseError
from rest_framework import status

#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "access_token": str(refresh.access_token),
                "token_type": str(refresh.access_token.token_type),
                "expires_in": int(refresh.access_token.lifetime.total_seconds()),
                "refresh_token":str(refresh),
                # "user": UserSerializer(user,context=self.get_serializer_context()).data,
                # "msg": [
                #     {
                #     "message": "User Created Successfully.  Now perform Login to get your token",

                #     }
                # ]
            },status=status.HTTP_201_CREATED)

            
        else:
            raise ParseError({
                 'msg' : 'ลงทะเบียนไม่สำเร็จ',
                 'code': 'REGISTER_FAIL',
                 'errors':serializer.errors,
            })
            # return Response({
            #      "msg" : "ลงทะเบียนไม่สำเร็จ",
            #      "code": "REGISTER_FAIL",
            #      "errors": serializer.errors,
            # })
        # creta user and validate and save data
        def create(self, validated_data):
            user = User.objects.create_user(
                username= validated_data['username'],     
                password = validated_data['password']  ,
                first_name=validated_data['first_name'],  
                last_name=validated_data['last_name'])
            # token = super().get_token(user)
            # token['name'] = user.name
            user.save()
        return user
        # serializer.is_valid(raise_exception=True)
        # user = serializer.save()
        # return Response({

        #     "user": UserSerializer(user,    context=self.get_serializer_context()).data,
        #     "message": "User Created Successfully.  Now perform Login to get your token",
        # })