from re import L
from rest_framework.serializers import ModelSerializer
from pig.models import Pig

class PigSerializer(ModelSerializer):
    class Meta:
        model = Pig
        exclude = ["owner"]