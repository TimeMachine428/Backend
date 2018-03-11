from rest_framework import permissions
from restapi.models import Problem


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission which grants write access to a route if and only if the authenticated
    user is the owner of that resource. Otherwise it grants read-only access
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsOwnerOfProblemOrReadOnly(permissions.BasePermission):
    """
    Permission which grants write access to a sub-route of problem/[problem_id]/ based on whether the user
    is the owner of the underlying problem
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        problem_id = view.kwargs.get('problem_id')
        return Problem.objects.get(pk=problem_id).owner == request.user
