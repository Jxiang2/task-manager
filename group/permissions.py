from rest_framework import permissions

class IsGroupManagerOrNone(permissions.BasePermission):
    '''
    Custom permission for group managers to only allow specific 
    '''
    
    def has_permission(self, request, view):
        # if method == get, everyone can do it
        if request.method in permissions.SAFE_METHODS:
            return True
        # only non-anonymous users can register a new group
        if not request.user.is_anonymous:
            return True
        return False
        
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return request.user.profile == obj.manager
        return False
    