"""todo_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from auth_app.views import Logout, ObtainExpiringAuthToken, Ping, ChangePassword

schema_view = get_schema_view(
    openapi.Info(
        title="ToDo API",
        default_version='v1',
        description="ToDo application with authentication based on Token",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mrigank.anand52@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/login/', ObtainExpiringAuthToken.as_view(), name='login'),
    path('api/logout/', Logout.as_view(), name='logout'),
    path('api/change-password/', ChangePassword.as_view(), name='change_password'),
    path('api/ping/', Ping.as_view(), name='ping'),
    path('api/todos/', include('todoapi.urls')),
    path('api/pig/', include('pig.urls')),
]
