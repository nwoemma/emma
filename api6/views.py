from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from .serializers import (
    CustomUserCreationSerializer,
    CustomUserChangeSerializer,
    PasswordResetSerializer,
    CustomSetPasswordSerializer,
    LoginSerializer,
)
from accounts.models import CustomUser
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = CustomUserCreationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Send email confirmation or welcome email if needed
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                django_login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserChangeSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = CustomUserChangeSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user:
                subject = "Password Reset Requested"
                email_template_name = "accounts/password_reset_email.html"
                context = {
                    "email": email,
                    "domain": request.META["HTTP_HOST"],
                    "site_name": "Ivory Hospital",
                    "protocol": "http",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                }
                email_body = render_to_string(email_template_name, context)
                plain_message = strip_tags(email_body)

                try:
                    send_mail(
                        subject,
                        plain_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    return Response({'detail': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({'detail': f'Error sending email: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'detail': 'No account found with this email address.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            serializer = CustomSetPasswordSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'The password reset link is invalid or has expired.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetCompleteAPIView(APIView):
    def get(self, request):
        return Response({'detail': 'Password reset complete.'}, status=status.HTTP_200_OK)
