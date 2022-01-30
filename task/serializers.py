from re import L
from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField
from .models import Task, TaskList, Attachment
from group.models import Group

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name="profile-detail")
    completed_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name="profile-detail")
    task_list = serializers.HyperlinkedRelatedField(queryset=TaskList.objects.all(), many=False, view_name="tasklist-detail")
    group = serializers.CharField(source="get_group", read_only=True)
    attachments = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name="attachment-detail")
    
    
    # only validate task_list
    def validate_task_list(self, value):
        user_profile = self.context['request'].user.profile
        if value not in user_profile.group.task_lists.all():
            raise serializers.ValidationError({"detail": "task list provided does not belong to group which user is in"})
        return value
    
    # do all validations before using validated data
    def create(self, validated_data):
        user_profile = self.context['request'].user.profile
        task = Task.objects.create(**validated_data)
        task.created_by = user_profile
        task.save()
        return task
            
    class Meta:
        model = Task
        fields = ['url', 'id', 'name', 'description', 'task_status', 'group',
                  'created_on', 'created_by', 'completed_on', 'completed_by', 'task_list', 'attachments']
        read_only_fields = ['created_on', 'completed_on', 'created_by', 'completed_by', 'group', 'task_status']

class TaskListSerializer(serializers.ModelSerializer):
    # users can edit what group the tasklist belonging to
    group = serializers.HyperlinkedRelatedField(queryset=Group.objects.all(), many=False, view_name="group-detail")
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name="profile-detail")
    tasks = HyperlinkedRelatedField(read_only=True, many=True, view_name='task-detail')
    
    # only a group member can create task list
    def validate(self, attrs):
        user_profile = self.context['request'].user.profile
        group = attrs['group']
        if (user_profile.group) == None or (user_profile.group != group):
            raise serializers.ValidationError({"detail" : "you can only create task list for your own group"})
        return attrs
    
    def create(self, validated_data):
        user_profile = self.context['request'].user.profile
        if (user_profile.group) == None or (user_profile.group != validated_data['group']):
            raise serializers.ValidationError({"detail" : "you can only create task list for your own group"})
        else:
            task_list = TaskList.objects.create(**validated_data)
            task_list.created_by = user_profile
            task_list.save()
        return task_list
    
        
    
    class Meta:
        model = TaskList
        fields = ['url', 'id', 'name', 'description', 'status', 'created_on', 'created_by', 'group', 'tasks']
        read_only_fields = ['created_on', 'created_by', 'status']
        
class AttachmentSerializer(serializers.ModelSerializer):
    task = HyperlinkedRelatedField(queryset=Task.objects.all(), many=False, view_name="task-detail")
    
    # validate the task
    def validate(self, attrs):
        user_profile = self.context['request'].user.profile
        task = attrs['task']
        # orm
        task_list = TaskList.objects.get(tasks__id=task.id)
        if task_list not in user_profile.group.task_lists.all():
            raise serializers.ValidationError({"detail" : "task provided does not belong to group which user is in"})
        return attrs
    
    class Meta:
        model = Attachment
        fields = ['url', 'attachment_id', 'created_on', 'data', 'task']
        read_only_fields =["created_on"]