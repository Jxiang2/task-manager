from background_task import background
from background_task.tasks import Task as Bt
from group.models import Group
from task.models import COMPLETED

@background(schedule=10)
def calculate_group_stats():
    for group in Group.objects.all():
        total_tasks = 0
        completed_task_count = 0
        group_task_lists = group.task_lists.all()
        for task_list in group_task_lists:
            total_tasks += task_list.tasks.count()
            completed_task_count += task_list.tasks.filter(task_status=COMPLETED).count()
            
        group.completed_tasks_count = completed_task_count
        group.not_completed_tasks_count = total_tasks - completed_task_count
        group.save()

if not Bt.objects.filter(verbose_name = "calculate_group_stats").exists():
    calculate_group_stats(repeat=Bt.DAILY, verbose_name = 'calculate_group_stats', priority=0)