from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class VotePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return True  # Allow editing or deleting only if the user owns the vote
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            # Allow editing or deleting only if the user owns the vote or is admin
            return obj.user == request.user or request.user.is_staff
        return True  # Allow GET request for any user


class DogPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            # Allow editing or deleting only if the user owns the dog or is admin
            return obj.owner.user == request.user or request.user.is_staff
        elif request.method == 'GET':
            # Allow GET request only if the user owns the dog or is admin
            try:
                if obj.owner.user == request.user or request.user.is_staff:
                    return True
                else:
                    raise PermissionDenied(
                        'You can only access your dog\'s detail. '
                        'To see other dogs\' detail, please visit the list page.'
                    )
            except ObjectDoesNotExist:
                # If the object (user) doesn't exist, return a proper message
                raise PermissionDenied(
                    'The dog with the given id does not exist.')
        return True  # Allow other requests
