from rest_framework import permissions

class IsAllowedToEditTaskListElseNone(permissions.BasePermission):
    '''
    Custom permissions for task list viewset to allow the creator editing persmission.
    '''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            return request.user.profile == obj.created_by
        
class IsAllowedToEditTaskElseNone(permissions.BasePermission):
    '''
    Custom permissions for task viewset to only allow members of a group access to it's tasks
    '''
    
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.profile.group != None

    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            return request.user.profile.group == obj.task_list.group
        
        
class IsAllowedToEditAttachmentOrNone(permissions.BasePermission):
    '''
    Custom permissions for attachment viewset to only allow members of a group access to it's attachments
    '''
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.profile.group != None

    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            return request.user.profile.group == obj.task.task_list.group
        