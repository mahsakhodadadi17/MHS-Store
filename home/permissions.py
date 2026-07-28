from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    فقط صاحب آبجکت اجازه دسترسی دارد.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsSuperAdmin(BasePermission):
    """
    فقط سوپرادمین اجازه دسترسی دارد.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )