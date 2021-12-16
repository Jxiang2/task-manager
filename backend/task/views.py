from django.utils import timezone
from rest_framework import viewsets, mixins, response
from rest_framework import status as s
from rest_framework.decorators import action
from .serializers import TaskListSerializer, TaskSerializer, AttachmentSerializer
from .models import COMPLETED, NOT_COMPLETED, Task, TaskList, Attachment
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
    
    # only update the field of task status
    @action(detail=True, methods=["PATCH"])
    def update_task_status(self, request, pk=None):
        try:
            task = self.get_object()
            profile = request.user.profile
            status = request.data['task_status']
            
            # if task is not completed, mark it as not completed
            if status == NOT_COMPLETED:
                if task.task_status == COMPLETED:
                    task.task_status = status
                    task.completed_on = None
                    task.completed_by = None
                else:
                    raise Exception("Task is already marked as not complete")
            
            # if task is not completed, mark it as not completed  
            elif status == COMPLETED:
                if task.task_status == NOT_COMPLETED:
                    task.task_status = status
                    task.completed_on = timezone.now()
                    task.completed_by = profile
                else:
                    raise Exception("Task is already marked as complete")
            else:
                raise Exception("data must be COMPLETED or NOT_COMPLETED")
            
            task.save()
            serializer = TaskSerializer(instance = task, context={'request': request})
            return response.Response(serializer.data, status=s.HTTP_200_OK)
        
        except Exception as e:
            return response.Response({"detail": str(e)}, status=s.HTTP_400_BAD_REQUEST)
            
            
        
            
    
class AttachmentViewSet(viewsets.GenericViewSet, 
                        mixins.CreateModelMixin, 
                        mixins.RetrieveModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.DestroyModelMixin):

    permission_classes = [IsAllowedToEditAttachmentOrNone]
    serializer_class = AttachmentSerializer
    queryset = Attachment.objects.all()
    