from django.urls import path
from django.conf.urls import url, include
from .views import UserCreateAPIView, UserLoginAPIView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    
]
