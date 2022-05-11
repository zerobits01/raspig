from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todoapi.views import GoalAPI, DoneGoalAPI

goal_router = DefaultRouter()
goal_router.register(r'goals', GoalAPI, basename="goal")
goal_router.register(r'done-goals', DoneGoalAPI, basename="done-goal")

urlpatterns = [
    path('', include(goal_router.urls)),
]