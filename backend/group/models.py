from django.db import models
from django.utils.deconstruct import deconstructible
import uuid
import os

@deconstructible
class GenerateGroupImage(object):
    def __init__(self):
        pass
    
    # auto called when class is constructed
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/groups/{instance.id}/images/'
        name = f'main.{ext}'
        return os.path.join(path, name)
    
group_image_path = GenerateGroupImage()

class Group(models.Model):
    # necessary to store id first before storing image!
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    image = models.FileField(upload_to=group_image_path, blank=True, null=True)
    # auto populate current time, no more edition allowed
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    # delete the manager profile -> set the manager of group to null
    manager = models.OneToOneField('users.Profile', on_delete=models.SET_NULL, 
                                   blank=True, null=True, 
                                   # use profile.managed_group to access the group
                                   related_name="managed_group")
    points = models.IntegerField(default=1)
    completed_tasks_count = models.IntegerField(default=0)
    not_completed_tasks_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.group_id} | {self.name}'
    
    
