from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from todoapi.models import Goal
from todoapi.serializers import GoalSerializer
from rest_framework import permissions




class GoalAPI(ModelViewSet):
    
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    http_method_names = ['post', 'get', 'delete', 'patch']
    permission_classes = [permissions.IsAuthenticated, ]

    # it doesnt have authorization on create and patch

    def list(self, request):
        # print(request.user)
        data = self.queryset.filter(owner=request.user).values()
        print(20*"#", data)
        return Response(data)

class DoneGoalAPI(ModelViewSet):
    
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticated, ]
    
    def list(self, request):
        data = list(self.queryset.filter(done=True, owner=request.user).values())
        print(20*"#", data)
        return Response(data)