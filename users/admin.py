from django.contrib import admin
from .models import Profile

# register the user
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id','user_status')
admin.site.register(Profile, ProfileAdmin)