import logging
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from .serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    UserSerializer,
    PasswordChangeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    EmailVerificationSerializer
)
from .models import EmailVerificationToken, PasswordResetToken

logger = logging.getLogger()

class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if not serializer.is_valid():
                logger.warning(f"Registration validation failed: {serializer.errors}")
                return Response(
                    {'error': True, 'message': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = serializer.save()
            
            # Create email verification token
            expires_at = timezone.now() + timedelta(hours=24)
            EmailVerificationToken.objects.create(user=user, expires_at=expires_at)
            
            logger.info(f"User registered: {user.email}")
            
            return Response({
                'error': False, 
                'message': 'User registered successfully. Please verify your email.',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Registration error: {str(e)}", exc_info=True)
            return Response(
                {'error': True, 'message': 'Registration failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                logger.warning(f"Login validation failed: {serializer.errors}")
                return Response(
                    {'error': True, 'message': 'Invalid email or password.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, username=email, password=password)
            if not user:
                logger.warning(f"Login failed for: {email}")
                return Response(
                    {'error': True, 'message': 'Invalid email or password.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not user.is_active:
                return Response(
                    {'error': True, 'message': 'Account is deactivated.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            
            logger.info(f"User logged in: {user.email}")
            
            return Response({
                'error': False,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                'user': user_serializer.data,
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return Response(
                {'error': True, 'message': 'Login failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MeView(APIView):
    def get(self, request):
        try:
            serializer = UserSerializer(request.user)
            return Response({
                'error': False,
                'user': serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"MeView error: {str(e)}", exc_info=True)
            return Response(
                {'error': True, 'message': 'Failed to fetch user'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PasswordChangeView(APIView):
    def post(self, request):
        try:
            serializer = PasswordChangeSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'error': True, 'message': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = request.user
            
            # Verify old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'error': True, 'message': 'Current password is incorrect.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            logger.info(f"Password changed for: {user.email}")
            
            return Response({
                'error': False,
                'message': 'Password changed successfully.'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Password change error: {str(e)}", exc_info=True)
            return Response(
                {'error': True, 'message': 'Password change failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PasswordResetRequestView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            serializer = PasswordResetRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'error': True, 'message': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            email = serializer.validated_data['email']
            
            try:
                user = type('User', (), {})  # Mock user object
                from users.models import User
                user = User.objects.get(email=email)
                
                # Create reset token
                expires_at = timezone.now() + timedelta(hours=1)
                reset_token = PasswordResetToken.objects.create(user=user, expires_at=expires_at)
                
                # TODO: Send email with reset link
                # reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token.token}"
                # send_mail(...)
                
                logger.info(f"Password reset requested for: {email}")
                
                return Response({
                    'error': False,
                    'message': 'Password reset link sent to your email.'
                }, status=status.HTTP_200_OK)
            
            except User.DoesNotExist:
                # Don't reveal if email exists
                return Response({
                    'error': False,
                    'message': 'If the email exists, a reset link has been sent.'
                }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Password reset request error: {str(e)}", exc_info=True)
            return Response(
                {'error': True, 'message': 'Password reset request failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PasswordResetConfirmView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            serializer = PasswordResetConfirmSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'error': True, 'message': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            from users.models import User
            token_obj = PasswordResetToken.objects.get(token=serializer.validated_data['token'])
            user = token_obj.user
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Mark token as used
            token_obj.is_used = True
            token_obj.save()
            
            logger.info(f"Password reset completed for: {user.email}")
            
            return Response({
                'error': False,
                'message': 'Password reset successful.'
            }, status=status.HTTP_200_OK)
        
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'error': True, 'message': 'Invalid token.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Password reset confirm error: {str(e)}", exc_info=True)
            return Response(
                {'error': True, 'message': 'Password reset failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class EmailVerificationView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            serializer = EmailVerificationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'error': True, 'message': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            from users.models import User
            token_obj = EmailVerificationToken.objects.get(token=serializer.validated_data['token'])
            user = token_obj.user
            
            # Mark email as verified
            user.is_email_verified = True
            user.save()
            
            # Mark token as used
            token_obj.is_used = True
            token_obj.save()
            
            logger.info(f"Email verified for: {user.email}")
            
            return Response({
                'error': False,
                'message': 'Email verified successfully.'
            }, status=status.HTTP_200_OK)
        
        except EmailVerificationToken.DoesNotExist:
            return Response(
                {'error': True, 'message': 'Invalid token.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Email verification error: {str(e)}", exc_info=True)
            return Response(
                {'error': True, 'message': 'Email verification failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class HealthCheckView(APIView):
    permission_classes = []

    def get(self, request):
        return Response({
            'status': 'healthy',
            'message': 'Polymath API is running',
            'timestamp': timezone.now().isoformat()
        }, status=status.HTTP_200_OK)