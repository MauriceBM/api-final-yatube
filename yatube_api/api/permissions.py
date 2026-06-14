# yatube_api/api/permissions.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Разрешает чтение всем пользователям (аутентифицированным и нет).
    Запись/изменение/удаление доступно только автору объекта.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        if not request.user.is_authenticated:
            return False

        return obj.author == request.user
