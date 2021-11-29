from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('users',UserAPIView.as_view()),
    path("",home,name="home"),
    path("home/<int:id>",index,name="index"),
    path("login",login1,name="login1"),
    path("login-mouse/<int:id>",login2,name="login2"),
    path("Signup",signup1,name="signup1"),
    path("Signup/<int:id>",signup2,name="signup2"),
    path("mouse_movements/<int:id>",mouse,name="mouse_movement"),
    path("mouse_movements_check/<int:id>",mouse_check,name="mouse_movement_check"),
    path("fill/<int:id>",fill,name="fill"),
    path("check/<int:id>",check,name="check"),
    path("logoutuser/<int:id>",logoutuser,name="logoutuser"),
    path("pattern/<int:id>",pattern,name="pattern"),
    path("sending_mail/<int:id>",send_email,name="send_email"),
    path("verify_mail/<int:id>",verify_mail,name="verify_mail"),
    # path('login',obtain_auth_token,name="login"),
    path('user_create/<int:pk>',user_create,name="user_create"),
    path('user_post/<int:pk>',user_post,name="user_post"),
    path('login_acc/<int:pk>',login_acc,name="login_acc"),
    path('login-image/<int:id>',login3,name="login3")
]

