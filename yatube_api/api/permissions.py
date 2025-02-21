from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение всем пользователям, но изменять
    и удалять объект может только его автор.
    """

    def has_permission(self, request, view):
        """Разрешает доступ аутентифицированным пользователям."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Разрешает:
        Чтение (GET, HEAD, OPTIONS) всем пользователям.
        Изменение и удаление только автору объекта.
        """
        return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
        )
