from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Проверка принадлежности пользователя к владельцам объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.is_public
