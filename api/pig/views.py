from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from pig.serializers import PigSerializer
from pig.models import Pig
from todoapi.models import GetNewGoal
from rest_framework.response import Response
from todoapi.models import Goal

class PigAPI(ModelViewSet):
    
    queryset = Pig.objects.all()
    serializer_class = PigSerializer
    http_method_names = ['post', 'get']
    permission_classes = []
    
    def list(self, request):
        uuid = request.query_params.get('uuid', None)
        print(f"this is the uuid: {uuid}")
        if len(self.queryset.filter(uuid=uuid)) > 0:
            pig = self.queryset.filter(uuid=uuid)[0]
            if pig.owner is None:
                return Response({
                    "msg": f"pig id is {pig.id}"
                })
        else:
            pig = self.queryset.create(
                uuid=uuid
            )
            pig.save()
            return Response({
                "msg": f"pig id is {pig.id}"
            })
            
        tasks = Goal.objects.filter(owner=pig.owner, done=False).values()
        pig.get_new_task_count += 1
        pig.save()
        return Response(tasks)
        

class PigPointAPI(GenericViewSet):
    
    http_method_names = ['get']
    permission_classes = []
    
    def list(self, request):
        uuid = request.query_params.get('uuid', None)

        if len(Pig.objects.filter(uuid=uuid)) > 0:
            pig = Pig.objects.filter(uuid=uuid)[0]
            if pig.owner is None:
                return Response({
                    "msg": "pig owner is not set yet!"
                }, status=status.HTTP_424_FAILED_DEPENDENCY)
        pig.point_count += 1
        pig.save()
        point = 0
        done_tasks = Goal.objects.filter(owner=pig.owner, done=True)
        for task in done_tasks:
            point += task.point
        return Response({
            'msg': f"pig point is {point}"
        })
        

class PigTaskUpdate(GenericViewSet):
    
    http_method_names = ['patch']
    permission_classes = []
    
    def partial_update(self, request, pk):
        uuid = request.data.get('uuid', None)
        goal_id = request.data.get('goal_id', None)
        if uuid is None or goal_id is None:
            return Response({
                "msg": f"task id or uuid can not be empty!"
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(Pig.objects.filter(uuid=uuid)) > 0:
            pig = Pig.objects.filter(uuid=uuid)[0]

        goal = Goal.objects.get(id=goal_id)
        
        if goal.owner != pig.owner:
            return Response({
                'msg': 'you can not update this task, it aint related to you!'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            for k, v in goal.tasks.items():
                if v is False:
                    goal.tasks[k] = True
                    break    
            if all(goal.tasks.values()):
                goal.done = True
            goal.save()
        
        return Response({
            'msg': 'task updated successfully! good luck.'
        })


class GetNew(ModelViewSet):
    
    queryset = GetNewGoal.objects.all()
    http_method_names = ['post']


    def create(self, request):
        uuid = request.query_params.get('uuid', None)
        pig  = self.queryset.filter(uuid=uuid)[0]
        user = pig.owner
        data = self.queryset.filter(owner=user).values()
        if len(data) == 0:
            self.queryset.create(
                owner = user,
                getnew= True
            )
        return Response({
            "msg": "request for getting new task sent, please wait"
        })