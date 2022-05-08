from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todoapi.views import ToDoAPI

todo_router = DefaultRouter()
todo_router.register(r'tasks', ToDoAPI, basename="todo")

urlpatterns = [
    path('', include(todo_router.urls)),
]