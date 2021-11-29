from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class account(models.Model):
    post_id = models.IntegerField()
    acc_holder = models.CharField(max_length=1000)
    email = models.EmailField(null=True)
    proof = models.CharField(max_length=1000,null=True)
    phone = models.CharField(max_length=20,null=True)
    type = models.CharField(max_length=100,null=True)
    address = models.TextField(null=True)

    def __str__(self):
        return self.acc_holder






# everytime a account is created a token is generated
