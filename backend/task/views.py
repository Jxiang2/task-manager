from rest_framework import viewsets, mixins
from .serializers import TaskListSerializer, TaskSerializer, AttachmentSerializer
from .models import Task, TaskList, Attachment
from .permissions import IsAllowedToEditAttachmentOrNone, IsAllowedToEditTaskListElseNone, IsAllowedToEditTaskElseNone

class TaskListViewSet(mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin, 
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = [IsAllowedToEditTaskListElseNone]
    serializer_class = TaskListSerializer
    queryset = TaskList.objects.all()
    
    
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAllowedToEditTaskElseNone]
    queryset = Task.objects.all()
    
    def get_queryset(self):
        queryset = super(TaskViewSet, self).get_queryset()
        user_profile = self.request.user.profile
        updated_queryset = queryset.filter(created_by=user_profile)
        return updated_queryset
            
    
class AttachmentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, 
                        mixins.UpdateModelMixin, mixins.DestroyModelMixin):

    permission_classes = [IsAllowedToEditAttachmentOrNone]
    serializer_class = AttachmentSerializer
    queryset = Attachment.objects.all()
    