from rest_framework import permissions

class IsOrganizerOrReadOnly(permissions.BasePermission):
    """Allow organizer to edit/delete event, others read-only."""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for organizer
        return obj.organizer == request.user
