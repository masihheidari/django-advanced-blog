# utils.py
import threading

from rest_framework_simplejwt.tokens import RefreshToken


class EmailThread(threading.Thread):

    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()


def get_tokens_for_user(user):
    """توکن‌های لاگین (برای بعد از ثبت‌نام/لاگین)"""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def get_activation_token(user):
    """یک access token جدا، فقط برای لینک فعال‌سازی ایمیل"""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
