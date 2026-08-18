from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):
    message = "حساب کاربری شما هنوز تایید (verify) نشده است."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_verified
        )
