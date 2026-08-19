from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializer import (
    RegistrationSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
)
from .permissions import IsVerified
from ...models import Profile
from ..utils import EmailThread, get_tokens_for_user, get_activation_token

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from templated_email import get_templated_mail

User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # ساخت توکن فعال‌سازی و ارسال ایمیل
            token = get_activation_token(user)
            email_obj = get_templated_mail(
                template_name="activation_email",
                from_email="admin@admin.com",
                to=[user.email],
                context={"token": token},
            )
            EmailThread(email_obj).start()

            tokens = get_tokens_for_user(user)
            data = {
                "email": user.email,
                "tokens": tokens,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationConfirmApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token, *args, **kwargs):
        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
        except TokenError:
            return Response(
                {"detail": "توکن نامعتبر یا منقضی شده است."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, pk=user_id)

        if user.is_verified:
            return Response(
                {"detail": "حساب کاربری قبلاً فعال شده است."},
                status=status.HTTP_200_OK,
            )

        user.is_verified = True
        user.save()
        return Response(
            {"detail": "حساب کاربری با موفقیت فعال شد."},
            status=status.HTTP_200_OK,
        )


class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated, IsVerified]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated, IsVerified]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["wrong password"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"details": "password changed"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsVerified]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj


class TestEmailSend(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        email_obj = get_templated_mail(
            template_name="hello",
            from_email="admin@admin.com",
            to=["masih.masih1386@gmail.com"],
            context={"name": "masih"},
        )
        EmailThread(email_obj).start()
        return Response("email sent")
