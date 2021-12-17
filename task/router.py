from rest_framework import routers
from .views import TaskListViewSet, TaskViewSet, AttachmentViewSet

app_name = 'task'
router = routers.DefaultRouter()
router.register('tasklists', viewset=TaskListViewSet)
router.register('tasks', viewset=TaskViewSet)
router.register('attachments', viewset=AttachmentViewSet)