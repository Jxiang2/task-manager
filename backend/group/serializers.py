from rest_framework import serializers
from .models import Group

class GroupSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Group
        fields = ['url', 'group_id', 'image', 'name', 'created_on', 
                  'manager', 'description', 'members_count',
                  'points', 'completed_tasks_count', 'not_completed_tasks_count']
        # a eaiser way to specify read_only fields
        read_only_fields = ['points', 'completed_tasks_count', 'not_completed_tasks_count',]