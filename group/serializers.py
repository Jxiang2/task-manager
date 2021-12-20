from rest_framework import serializers
from .models import Group

class GroupSerializer(serializers.ModelSerializer):
    # (many = true) => the field is a list of json
    member_set = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='profile-detail')
    manager = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    task_lists = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name="tasklist-detail")
    
    def create(self, validated_data):
        try:
            user_profile = self.context['request'].user.profile
            if Group.objects.filter(manager=user_profile).exists():
                raise serializers.ValidationError({"detail": "one user can only create one group"})
            group = Group.objects.create(**validated_data)
            group.manager = user_profile
            group.save()
            return group
        except Exception as e:
            raise serializers.ValidationError({"detail": e})
    
    class Meta:
        model = Group
        fields = ['url', 'group_id', 'image', 'name', 'created_on', 
                  'manager', 'description', 'member_set',
                  'points', 'task_lists']
        # a eaiser way to specify read_only fields
        read_only_fields = ['points', 'completed_tasks_count', 'not_completed_tasks_count',]