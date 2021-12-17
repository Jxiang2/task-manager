from django.contrib import admin
from .models import Group

# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ('group_id', 'created_on')
admin.site.register(Group,GroupAdmin)
