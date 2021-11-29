from re import I
from django.db.models import fields
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
import requests
from django.contrib.auth.models import User
import json

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'     

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],     password = validated_data['password']  )
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token

import json
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        acc  = requests.get('http://127.0.0.1:5000/api/users/%d/accounts' % self.user.id)
        print(acc)
        # # response_read = acc.read()
        accounts = json.loads(acc.text.replace("\'", '"'))
        data = {
            "username" : self.user.username,
            "id" : self.user.id,
            "accounts": accounts,
        }
        return data

from rest_framework_simplejwt.state import token_backend

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_uid=decoded_payload['user_id']
        username=decoded_payload['username']
        acc  = requests.get('http://127.0.0.1:5000/api/users/%d/accounts' % user_uid)
        accounts = json.loads(acc.text.replace("\'", '"'))
        print(acc)
        # add filter query
        data.update({'id': user_uid})
        data.update({'username': username})
        data.update({'accounts': accounts})
        return data
