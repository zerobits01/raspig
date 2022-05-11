from rest_framework.routers import DefaultRouter
from django.urls import path, include
from pig.views import PigAPI, PigPointAPI, PigTaskUpdate


pig_router = DefaultRouter()
pig_router.register('pig', PigAPI, basename="pig")
pig_router.register('point', PigPointAPI, basename="pig-point")
pig_router.register('task-update', PigTaskUpdate, basename="task-update")

urlpatterns = [
    path('', include(pig_router.urls)),
]
