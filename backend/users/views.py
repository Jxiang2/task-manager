from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from .models import Profile
from .serializer import ProfileSerializer, UserSerializer
from .permissions import IsUserOwnerOrGetPostOnly, IsProfileOwnerOrReadOnly


class profileViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    
    permission_classes = [IsProfileOwnerOrReadOnly,]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

class userViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsUserOwnerOrGetPostOnly,]
    serializer_class = UserSerializer
    queryset = User.objects.all()
