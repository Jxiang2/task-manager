from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    # need custom logic for password
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(read_only=True)
    
    # register ; validated data = fields with write mode
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        # for security reason, set password here
        user.set_password(password)
        user.save()
        
        return user
        
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 
                  'first_name', 'last_name', 'password']