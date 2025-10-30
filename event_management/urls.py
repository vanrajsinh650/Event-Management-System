"""
URL configuration for event_management project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/ReDoc Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Event Management API",
        default_version='v1',
        description="""
        A comprehensive Event Management System API built with Django REST Framework.
        
        Features:
        - JWT Authentication
        - Event CRUD operations
        - RSVP Management
        - Event Reviews and Ratings
        - User Profiles
        - Private/Public Events with Access Control
        
        Authentication:
        Use the /api/token/ endpoint to obtain access and refresh tokens.
        Include the access token in the Authorization header as: Bearer <token>
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@eventmanagement.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def redirect_to_swagger(request):
    """Redirect root URL to Swagger documentation."""
    return HttpResponseRedirect('/swagger/')

urlpatterns = [
    # Redirect root to Swagger
    path('', redirect_to_swagger, name='home'),
    
    # Admin
    path('admin/', admin.site.urls, name='admin'),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # App URLs
    path('api/', include('user.urls')),
    path('api/', include('events.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
