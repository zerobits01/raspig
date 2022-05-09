from rest_framework.routers import DefaultRouter
from django.urls import path, include
from pig.views import PigAPI, WeightAPI


pig_router = DefaultRouter()
pig_router.register('pig', PigAPI, basename="pig")
pig_router.register('weight', WeightAPI, basename="pig-weight")

urlpatterns = [
    path('', include(pig_router.urls)),
]
