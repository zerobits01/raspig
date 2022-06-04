from requests import delete
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from todoapi.models import Goal, GetNewGoal
from todoapi.serializers import GoalSerializer
from rest_framework import permissions


class GoalAPI(ModelViewSet):
    
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    http_method_names = ['post', 'get', 'delete', 'patch']
    permission_classes = [permissions.IsAuthenticated, ]

    # it doesnt have authorization on create and patch

    def list(self, request):
        data = self.queryset.filter(owner=request.user).values()
        print(20*"#", data)
        return Response(data)


class GetNewAPI(ModelViewSet):
    
    queryset = GetNewGoal.objects.all()
    http_method_names = ['get', 'delete']
    permission_classes = [permissions.IsAuthenticated, ]

    # it doesnt have authorization on create and patch

    def list(self, request):
        # print(request.user)
        data = self.queryset.filter(owner=request.user).values()
        print(20*"#", data)
        return Response(data[0])

    # def create(self, request):
    #     data = self.queryset.filter(owner=request.user).values()
    #     if len(data) == 0:
    #         self.queryset.create(
    #             owner = request.user,
    #             getnew=True
    #         )
    #     return Response({
    #         "msg": "request for getting new task sent, please wait"
    #     })

    
    def delete(self, request):
        child_req = self.queryset.filter(owner=request.user)[0]
        child_req.delete()
        return Response({
            "msg": "deleting child request done!"
        })

# class DoneGoalAPI(ModelViewSet):
    
#     queryset = Goal.objects.all()
#     serializer_class = GoalSerializer
#     http_method_names = ['get']
#     permission_classes = [permissions.IsAuthenticated, ]
    
#     def list(self, request):
#         data = list(self.queryset.filter(done=True, owner=request.user).values())
#         print(20*"#", data)
#         return Response(data)