from rest_framework.viewsets import ModelViewSet
from todoapi.models import ToDo
from todoapi.serializers import ToDoSerializer
from rest_framework import permissions




class ToDoAPI(ModelViewSet):
    
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    http_method_names = ['post', 'get', 'delete', 'put']
    permission_classes = [permissions.IsAuthenticated, ]
    