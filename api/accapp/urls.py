from django.urls import path
from .views import *
from .serializers import *

urlpatterns = [
    path('accounts',AccountAPIView.as_view()),
    path('users/<str:pk>/accounts',UserAccountAPIView.as_view()),
    path('api/register', RegisterApi.as_view()),
]
