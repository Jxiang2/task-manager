from rest_framework import permissions

class IsUserOwnerOrGetPostOnly(permissions.BasePermission):
    '''
    custom permission for userViewSet to only allow users to edit their 
    own profiles, otherwise they can only GET and POST
    '''
    
    # has permission() only called when perform list and create, we want to to be true by Default
    def has_permission(self, request, view):
        return True
    
    # has_object_permission() called when perform retrieve, update, partial_update and delete on a specific resource
    # obj: the actual object to be permitted or not, in this case, auth user
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # GET(retrieve) & POST(none in this case)
            return True
        
        if not request.user.is_anonymous:
            # ture -> has permission
            # false -> permission denied
            return request.user == obj
        
        return False
            
            
    
    
