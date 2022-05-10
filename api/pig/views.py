from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from pig.serializers import PigSerializer
from pig.models import Pig
from rest_framework.response import Response
from todoapi.models import ToDo
from todoapi.serializers import ToDoSerializer

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
            
        tasks = ToDo.objects.filter(owner=pig.owner, done=False).values()
        pig.get_new_task_count += 1
        pig.save()
        return Response(tasks)
        

class WeightAPI(GenericViewSet):
    
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
        pig.weight_count += 1
        pig.save()
        weight = 0
        done_tasks = ToDo.objects.filter(owner=pig.owner, done=True)
        for task in done_tasks:
            weight += task.weight
        return Response({
            'msg': f"pig weight is {weight}"
        })
        

class PigTaskUpdate(GenericViewSet):
    
    http_method_names = ['patch']
    permission_classes = []
    
    def partial_update(self, request, pk):
        uuid = request.data.get('uuid', None)
        task_id = request.data.get('task_id', None)
        if uuid is None or task_id is None:
            return Response({
                "msg": f"task id or uuid can not be empty!"
            }, status=status.HTTP_400_BAD_REQUEST)
    
        if len(Pig.objects.filter(uuid=uuid)) > 0:
            pig = Pig.objects.filter(uuid=uuid)[0]

        task = ToDo.objects.get(id=task_id)
        
        if task.owner != pig.owner:
            return Response({
                'msg': 'you can not update this task, it aint related to you!'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            if task.t1_done == False:
                task.t1_done = True
            elif task.t2_done == False:
                task.t2_done = True
            elif task.t3_done == False:
                task.t3_done = True
            elif task.t4_done == False:
                task.t4_done = True
                task.done = True
            task.save()
        
        return Response({
            'msg': 'task updated successfully! good luck.'
        })

