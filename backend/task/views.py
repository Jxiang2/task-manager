from rest_framework import viewsets, mixins
from .serializers import TaskListSerializer, TaskSerializer, AttachmentSerializer
from .models import Task, TaskList, Attachment
from .permissions import IsAllowedToEditAttachmentOrNone, IsAllowedToEditTaskListElseNone, IsAllowedToEditTaskElseNone

class TaskListViewSet(mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin, 
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = [IsAllowedToEditTaskListElseNone]
    serializer_class = TaskListSerializer
    queryset = TaskList.objects.all()
    
    
class TaskViewSet(mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin, 
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAllowedToEditTaskElseNone]
    queryset = Task.objects.all()
            
    
class AttachmentViewSet(viewsets.GenericViewSet, 
                        mixins.CreateModelMixin, 
                        mixins.RetrieveModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.DestroyModelMixin):

    permission_classes = [IsAllowedToEditAttachmentOrNone]
    serializer_class = AttachmentSerializer
    queryset = Attachment.objects.all()
    