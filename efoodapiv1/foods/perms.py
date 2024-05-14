from rest_framework import permissions

class CommnetOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, comment):
        return self.has_permission(request, view) and request.user == comment.user