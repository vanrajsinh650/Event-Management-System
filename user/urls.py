"""
URL patterns for user-related endpoints.
"""
from django.urls import path
from .views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
]
