from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Group
from .serializers import GroupSerializer
from .permissions import IsGroupManagerOrNone


class GroupViewSet(viewsets.ModelViewSet):
    
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsGroupManagerOrNone,]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    filterset_fields = ['name', 'points', 'member_set']
    
    # custom action of joining and leaving house, the default oauth2 base permission is applied (if user has token -> has permission)
    @action(detail=True, methods=['POST'], name='Join', permission_classes=[])
    def join(self, request, pk=None):
        try:
            # get the current group
            group = self.get_object()
            user_profile = request.user.profile
            # remember, group is an attribute of profile
            if (user_profile.group == None):
                user_profile.group = group # join the group
                user_profile.save()
                return Response({"detail": f'joined group {group.name}'},status=status.HTTP_204_NO_CONTENT)
            elif user_profile in group.member_set.all():
                return Response({"detail": "already a member"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "already a member in another group"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # custom action of joining and leaving house, the default oauth2 base permission is applied (if user has token -> has permission)
    @action(detail=True, methods=['POST'], name='Leave', permission_classes=[])
    def leave(self, request, pk=None):
        try:
            group = self.get_object()
            user_profile = request.user.profile
            if (user_profile in group.member_set.all()):
                user_profile.group = None
                user_profile.save()
                return Response({"detail": f'leaved group: {group.name}'},status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "not a member yet"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    #permission class inheritated from view permission class
    @action(detail=True, methods=['POST'], name='Remove Member')
    def remove_member(self, request, pk=None):
        try:
            group = self.get_object()
            # user need to input a user_id!
            user_id = request.data.get('user_id', None)
            if user_id == None:
                return Response({"user_id": "not provided"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(pk=user_id)
            user_profile = user.profile
            
            if user_profile in group.member_set.all():
                group.member_set.remove(user_profile)
                group.save()
                return Response({"detail": f'removed {user.username} from {group.name}'},status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": f'{user.username} is not in the group'},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as e:
            return Response({"detail": "user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        