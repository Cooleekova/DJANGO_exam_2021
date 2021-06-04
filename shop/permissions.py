from rest_framework import permissions


class ReadOnly(permissions.DjangoModelPermissionsOrAnonReadOnly):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


# Создавать товары могут только админы. Смотреть могут все пользователи.
class IsAdminUser(permissions.BasePermission):
    message = 'Требуются права администратора'

    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        # Create permissions for admins only
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


# Пользователь может обновлять и удалять только свой собственный отзыв.
class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'Нет прав на изменение отзыва'

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user



