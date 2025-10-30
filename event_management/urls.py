from drf_yasg.views import get_schema_view
from django.urls import path, include
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Event Management API",
        default_version='v1',
        description="Event Management System",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    #existing patterns 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]
