from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
# created arg only exists in post_save signals
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # instance is already user
        Profile.objects.create(user=instance)

@receiver(pre_save, sender=User)   
def set_username(sender, instance, **kwargs):
    if not instance.username:
        username = f'{instance.first_name}_{instance.last_name}'.lower()
        counter = 1
        while User.objects.filter(username=username):
            username = f'{instance.first_name}_{instance.last_name}_{counter}'.lower()
            counter+=1
        instance.username = username
