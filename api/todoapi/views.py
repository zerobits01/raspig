from rest_framework.viewsets import ModelViewSet
from todoapi.models import Goal
from todoapi.serializers import GoalSerializer
from rest_framework import permissions




class GoalAPI(ModelViewSet):
    
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    http_method_names = ['post', 'get', 'delete', 'put']
    permission_classes = [permissions.IsAuthenticated, ]
    