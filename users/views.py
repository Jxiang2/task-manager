from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from .models import Profile
from .serializer import ProfileSerializer, UserSerializer
from .permissions import IsUserOwnerOrGetPostOnly, IsProfileOwnerOrReadOnly



class profileViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsProfileOwnerOrReadOnly,]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    filterset_fields = ['user_status']

class userViewSet(viewsets.ModelViewSet):
    
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsUserOwnerOrGetPostOnly,]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filterset_fields = ['first_name', 'last_name']
