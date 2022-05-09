from imp import get_magic
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from pig.serializers import PigSerializer
from pig.models import Pig
from rest_framework.response import Response


class PigAPI(ModelViewSet):
    
    queryset = Pig.objects.all()
    serializer_class = PigSerializer
    http_method_names = ['post', 'get', 'delete', 'put']
    permission_classes = []
    
    def list(self, request):
        # this gonna return all tasks related to this pig
        # if this is empty it gonna return something to the pig which alert it for post and register
        # increment get_new_task_count by 1
        uuid = request.query_params.get('uuid', None)
        print(f"this is the uuid: {uuid}")
        return Response({
            'test': f'this is the list of tasks for <uuid:{uuid}>'
        })


class WeightAPI(GenericViewSet):
    
    # queryset = Pig.objects.all()
    # serializer_class = PigSerializer
    http_method_names = ['get']
    permission_classes = []
    
    def list(self, request):
        # return whole weight and add 1 number to count
        print("this is a test")
        uuid = request.query_params.get('uuid', None)
        if uuid is not None:
            
            return Response({
                'test': f'this is the get request with {uuid}'
            })
    

        return Response({
            'errors': ["uuid can not be empty"]
        })