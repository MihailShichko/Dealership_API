"""
URL configuration for dealership_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from dealership_app.consumers.consumers import CarPostConsumer
from dealership_app.views import CarViewSet, RegisterView, LogoutView, notification_view

schema_view = get_schema_view(
    openapi.Info(
        title="Dealership API",
        default_version='v1',
        description="Dealership API description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cars/all', CarViewSet.as_view({'get': 'list'})),
    path("api/cars/add", CarViewSet.as_view({'post': 'create'})),
    path("api/cars/change/<int:pk>/", CarViewSet.as_view({'put': 'update'})),
    path("api/cars/delete/<int:pk>/", CarViewSet.as_view({'delete': 'destroy'})),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('ws/notifications/', notification_view, name='notification_template'),
]
