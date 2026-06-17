from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, SAFE_METHODS
)


class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """Разрешает чтение всем, запись только автору."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return obj.author == request.user
