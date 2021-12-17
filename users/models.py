from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
import os

@deconstructible
class GenrateProfileImagePath(object):
    def __init__(self):
        pass
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/accounts/{instance.user.id}/images/'
        name = f'profile_image.{ext}'
        return os.path.join(path, name)
        
user_profile_image_path = GenrateProfileImagePath()


class Profile(models.Model):
    ONLINE = 0
    OFFLINE = 1
    DONOTDISTURB = 2

    STATUS_CHOICES = [
        (ONLINE, 'ONLINE'),
        (OFFLINE, 'OFFLINE'),
        (DONOTDISTURB, 'DONOTDISTURB')
    ]
    
    # user can be customised in core app, when user model deleted -> delete the Profile model associated with the user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    image = models.FileField(upload_to=user_profile_image_path, blank=True, null=True)
    # house 1 - * profiles ; if the group is deleted, set the group attr to null
    group =  models.ForeignKey('group.Group', on_delete=models.SET_NULL, null=True, blank=True, related_name="member_set")
    
    
    def __str__(self):
        return f'{self.user.username}\'s Profile'
    
    def get_display_name(self):
        return f'{self.user.first_name}_{self.user.last_name}'