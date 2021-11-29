from django.shortcuts import render
from rest_framework import  serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *


# Create your views here.

class UserAccountAPIView(APIView):
    def get(self, _, pk=None):
        accounts = account.objects.filter(post_id=pk)
        serializer = AccountSerializer(accounts,many=True)
        return Response(serializer.data)

class AccountAPIView(APIView):
    def get(self,request):
        users = account.objects.all()
        serializer = AccountSerializer(users,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenRefreshView
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

from rest_framework import generics
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


#eaf7f31c29614621af22d4471c441b3362f8fde2