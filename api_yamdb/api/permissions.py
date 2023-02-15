from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для Admin-пользователя или только на чтение."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsSuperUserOrAdmin(permissions.BasePermission):
    """Разрешение для Admin-пользователя или SuperUser."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_admin)
        )


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для Admin-пользователя, Moderator-пользователя или
    автора. В остальных случаях только чтение. """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
