from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializer import UserSerializer

class userViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
