from rest_framework.viewsets import ModelViewSet
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
        return Response({
            'test': 'this is the list of tasks'
        })