from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todoapi.views import GoalAPI

goal_router = DefaultRouter()
goal_router.register(r'tasks', GoalAPI, basename="goal")

urlpatterns = [
    path('', include(goal_router.urls)),
]