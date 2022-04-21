from rest_framework import permissions


class IsAuthorOrHasAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or obj.access.filter(users=request.user))
