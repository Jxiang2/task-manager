from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField
from .models import Task, TaskList, Attachment
from group.models import Group

class TaskListSerializer(serializers.ModelSerializer):
    # users can edit what group the tasklist belonging to
    group = serializers.HyperlinkedRelatedField(queryset=Group.objects.all(), many=False, view_name="group-detail")
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name="profile-detail")
    
    class Meta:
        model = TaskList
        fields = ['url', 'id', 'name', 'description', 'task_status', 'created_on', 'created_by', 'group']
        read_only_fields = ['created_on', 'created_by', 'task_status']
        
class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name="profile-detail")
    completed_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name="profile-detail")
    task_list = serializers.HyperlinkedRelatedField(queryset=TaskList.objects.all(), many=False, view_name="tasklist-detail")
    group = serializers.CharField(source="get_group", read_only=True)
    
    class Meta:
        model = Task
        fields = ['url', 'id', 'name', 'description', 'task_status', 'group',
                  'created_on', 'created_by', 'completed_on', 'completed_by', 'task_list']
        read_only_fields = ['created_on', 'completed_on', 'created_by', 'completed_by', 'group']
        
class AttachmentSerializer(serializers.ModelSerializer):
    task = HyperlinkedRelatedField(queryset=Task.objects.all(), many=False, view_name="task-detail")
    
    class Meta:
        model = Attachment
        fields = ['url', 'attachment_id', 'created_on', 'data', 'task']
        read_only_fields =["created_on"]