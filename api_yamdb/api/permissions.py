from rest_framework import permissions


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    """Изменение и удаление отзывов (Review) и комментариев (Comment)
    доступно только авторам, модераторам и администраторам."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_moderator
            or request.user == obj.author
        )


class AdminOnlyOrRead(permissions.BasePermission):
    """Создание, изменение и удаление произведений (Title),
    категорий (Category) и жанров (Genre) доступно только администраторам."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )
