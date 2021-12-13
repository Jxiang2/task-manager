from django.db import models
from django.utils.deconstruct import deconstructible
from django.db.models.deletion import CASCADE, SET_NULL
import uuid
import os

NOT_COMPLETED = 'NC'
COMPLETED = 'C'
    
TASK_STATUS_CHOICES = [
        (NOT_COMPLETED, 'Not Completed'),
        (COMPLETED, 'Completed')
]

@deconstructible
class GenerateAttachmentFilePath(object):
    def __init__(self):
        pass
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/tasks/{instance.task.id}/attachments/'
        name = f'{instance.attachment_id}.{ext}'
        return os.path.join(path, name)
    
attachment_file_path = GenerateAttachmentFilePath()

class Task(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    # user_profile 1 - * task ; if user deleted, set created_by to null instead of deleting the task
    created_by = models.ForeignKey('users.Profile', null=True, blank=True, 
                                   on_delete=SET_NULL, related_name="created_tasks")
    completed_by = models.ForeignKey('users.Profile', null=True, blank=True, 
                                   on_delete=SET_NULL, related_name="completed_tasks")
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    task_status = models.CharField(
        max_length=2,
        choices=TASK_STATUS_CHOICES,
        default=NOT_COMPLETED
    )
    # task_list 1 - * task ; if task_list deleted, delete all tasks
    task_list = models.ForeignKey('task.TaskList', on_delete=models.CASCADE, related_name="tasks")
    
    def __str__(self):
        return f'{self.id} | {self.name}'
    
    def get_group(self):
        return self.task_list.group
    
class TaskList(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    # group 1 - * task ; if group deleted, delete all task lists
    group = models.ForeignKey('group.Group', on_delete=CASCADE, related_name= "task_lists")
    # user_profile 1 - * task ; if user_profile deleted, set created_by to null instead of deleting the task
    created_by = models.ForeignKey('users.Profile', null=True, blank=True, 
                                   on_delete=SET_NULL, related_name="task_lists")
    name = name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    task_status = models.CharField(
        max_length=2,
        choices=TASK_STATUS_CHOICES,
        default=NOT_COMPLETED
    )
    
    def __str__(self):
        return f'{self.id} | {self.name}'
    
class Attachment(models.Model):
    attachment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    data = models.FileField(upload_to=attachment_file_path)
    # task 1 - * attachments ; if task is deleted, delete all attachments
    task = models.ForeignKey("task.Task", on_delete=models.CASCADE, related_name="attachments")
    
    def __str__(self):
        return f'Attachemnt {self.attachment_id} | {self.task}'
    
    
    
    
