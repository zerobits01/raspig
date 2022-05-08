from rest_framework.routers import DefaultRouter
from django.urls import path, include
from pig.views import PigAPI


pig_router = DefaultRouter()
pig_router.register('', PigAPI, basename="pig")

urlpatterns = [
    path('', include(pig_router.urls)),
]
