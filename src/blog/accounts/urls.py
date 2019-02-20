from django.urls import path
from django.conf.urls import url, include
from .views import UserCreateAPIView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    
]
