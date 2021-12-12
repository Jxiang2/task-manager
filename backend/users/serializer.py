from django.contrib.auth.models import User
from django.db.models import fields
from .models import Profile
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='get_display_name', read_only=True)
    user = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='user-detail')
    group = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='group-detail')
    class Meta:
        model = Profile
        fields = ['url', 'user', 'user_status', 'display_name', 'image', 'group',]

class UserSerializer(serializers.ModelSerializer):
    
    # need custom logic for password
    password = serializers.CharField(write_only=True, required=False)
    old_password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(read_only=True)
    # foreign keys
    profile = ProfileSerializer(read_only=True)
    
    # raw data from client
    def validate(self, data):
        request_method = self.context['request'].method
        # data: the raw data passed by client
        password = data.get('password', None)
        # register
        if request_method == "POST":
            if password == None:
                raise serializers.ValidationError({"info":"Plz provide pwd"})
        # updaate
        elif request_method == "PUT" or request_method == "PATCH":
            old_password = data.get("old_password", None)
            if password != None and old_password == None:
                raise serializers.ValidationError({"info": "Plz provide old pwd"})
        return data
            
    
    # register ; validated data = fields with write mode
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        # for security reason, set password here
        user.set_password(password)
        user.save()
        
        return user
    
    # update pwd
    def update(self, instance, validated_data):
        try:
            user = instance
            if 'password' in validated_data:
                password = validated_data.pop('password')
                old_password = validated_data.pop('old_password')
                if user.check_password(old_password):
                    user.set_password(password)
                else:
                    raise Exception("Old Password Incorrect")
                user.save()
        except Exception as err:
            raise serializers.ValidationError(err)
        return super(UserSerializer, self).update(instance, validated_data)
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 
                  'first_name', 'last_name', 'password', 'old_password', 'profile']