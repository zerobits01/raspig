from rest_framework import serializers
from .models import Goal


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        exclude = ["owner"]

    def create(self, validated_data):
        print(validated_data)
        for k, v in validated_data['tasks'].items():
            if type(k) is not str and type(v) is not bool:
                raise ValueError('tasks should be in format {task-name: boolean-done}') 
        request = self.context.get('request', None)
        if request:
            owner = request.user
            validated_data['owner'] = owner
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for k, v in validated_data['tasks'].items():
            if type(k) is not str and type(v) is not bool:
                raise ValueError('tasks should be in format {task-name: boolean-done}')
            if v is False:
                 validated_data['done'] = False
        request = self.context.get('request', None)       
        if request:
            owner = request.user
            validated_data['owner'] = owner
        return super().update(instance, validated_data)
