from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializer import UserSerializer
from .permissions import IsUserOwnerOrGetPostOnly

class userViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsUserOwnerOrGetPostOnly,]
    serializer_class = UserSerializer
    queryset = User.objects.all()
