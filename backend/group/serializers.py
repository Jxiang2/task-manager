from rest_framework import serializers
from .models import Group

class GroupSerializer(serializers.ModelSerializer):
    # (many = true) => the field is a list of json
    member_set = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='profile-detail')
    manager = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    members_count = serializers.IntegerField(read_only=True)
    task_lists = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name="tasklist-detail")
    
    class Meta:
        model = Group
        fields = ['url', 'group_id', 'image', 'name', 'created_on', 
                  'manager', 'description', 'members_count', 'member_set',
                  'points', 'completed_tasks_count', 'not_completed_tasks_count', 'task_lists']
        # a eaiser way to specify read_only fields
        read_only_fields = ['points', 'completed_tasks_count', 'not_completed_tasks_count',]