from rest_framework import viewsets
from .models import Group
from .serializers import GroupSerializer
from .permissions import IsGroupManagerOrNone


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsGroupManagerOrNone,]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()