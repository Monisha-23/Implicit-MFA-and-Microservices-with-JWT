from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class MyUser(AbstractUser):
    hashcode = models.CharField(max_length=1000, blank=False)
    mouse = models.CharField(max_length=1000, blank=False)
    otp = models.CharField(max_length=30, blank=True)
    created_on = models.DateField(auto_now_add=True)
    document = models.FileField(upload_to='documents/',null=True)

    def __str__(self):
        return self.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)