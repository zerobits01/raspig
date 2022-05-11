from rest_framework import serializers
from .models import Goal


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        exclude = ["owner"]

    def create(self, validated_data):
        for k, v in validated_data['tasks']:
            if type(k) is not str and type(v) is not bool:
                raise ValueError('tasks should be in format {task-name: boolean-done}') 
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
