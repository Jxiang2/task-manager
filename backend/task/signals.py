from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Task, COMPLETED, NOT_COMPLETED

# group add 1 mark if a task is done
@receiver(post_save, sender=Task)
def update_group_point(sender, instance, created, **kwargs):
    group = instance.task_list.group
    if instance.task_status == COMPLETED:
        group.points += 1
    group.save()

# mark task list as COMPLETED if all of it's tasks are done
@receiver(post_save, sender=Task)
def update_task_list_status(sender, instance, created, **kwargs):
    task_list = instance.task_list
    is_complete = True
    
    for task in task_list.tasks.all():
        if task.task_status != COMPLETED:
            is_complete = False
            break
    task_list.status = COMPLETED if is_complete else NOT_COMPLETED
    task_list.save()
    
    


