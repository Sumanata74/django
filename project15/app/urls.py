from django.urls import path
from .views import *
urlpatterns=[
    path('register',register,name='register'),
    path('user_login',user_login,name='user_login'),
    path('home',home,name='home'),
    path('user_profile',user_profile,name='user_profile'),
    path('user_logout',user_logout,name='user_logout'),
    path('forget_password',forget_password,name='forget_password'),
    path('otp',otp,name='otp'),
    path('new_password',new_password,name='new_password'),
    path('change_password',change_password,name='change_password'),

]