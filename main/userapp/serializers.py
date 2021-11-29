from django.db.models import fields
from rest_framework import serializers
from .models import MyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'






