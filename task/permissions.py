from rest_framework import permissions

class IsAllowedToEditTaskListElseNone(permissions.BasePermission):
    '''
    Custom permissions for task list viewset to allow group members to view the task list 
    and the creator editing persmission.
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
            if request.method in permissions.SAFE_METHODS: # only group members can see the task list
                return request.user.profile.group == obj.group
            else: # only task list creator can edit the task list
                if request.user.profile.group == obj.group:
                    return request.user.profile == obj.created_by
        return False
        
class IsAllowedToEditTaskElseNone(permissions.BasePermission):
    '''
    Custom permissions for task viewset to only allow members of a group to view it's tasks
    and task creator or tasklist creator to edit the tasks
    '''
    
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.profile.group != None

    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            if request.method in permissions.SAFE_METHODS: # only group members can see the task details
                return request.user.profile.group == obj.task_list.group
            else: # only task creator and tasklist owner can edit the task
                if request.user.profile.group == obj.task_list.group:
                    return (request.user.profile == obj.created_by) or (request.user.profile == obj.task_list.created_by)
        return False
        
        
class IsAllowedToEditAttachmentOrNone(permissions.BasePermission):
    '''
    Custom permissions for attachment viewset to only allow members of a group access to it's tasks' attachments
    '''
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.profile.group != None

    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            # only group members can access their task attachment
            return request.user.profile.group == obj.task.task_list.group
        