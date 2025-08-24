from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import RegisterSerializer
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings  # This now gets values from .env via settings
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
User = get_user_model()

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        self.send_verification_email(user)  # This calls the instance method

    def send_verification_email(self, user): 
        # Generate verification token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Build verification URL using self.request
        # verification_url = self.request.build_absolute_uri(
        #     f'/api/auth/verify-email/{uid}/{token}/'
        # )

        # Temporary link for frontend verification link
        verification_url = f"http://localhost:5173/verify-email/{uid}/{token}/"

        # Prepare email context
        context = {
            'user': user,
            'verification_url': verification_url,
            'site_name': getattr(settings, 'SITE_NAME', 'Our Site'),  # Safe access
        }
        
        # Render HTML template
        html_message = render_to_string('accounts/email_verification.html', context)
        subject = 'Verify your email address'
        
        # Create and send email
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.content_subtype = 'html'
        
        try:
            email.send()
            return True
        except Exception as e:
            print(f"Error sending verification email: {e}")
            return False

User = get_user_model()

class VerifyEmailView(APIView):
    permission_classes = []  # Allow unauthenticated access
    authentication_classes = []  # No authentication required
    
    def get(self, request, uidb64, token):
        try:
            # Decode the user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            # Check if token is valid
            if not default_token_generator.check_token(user, token):
                return Response(
                    {"error": "Invalid or expired verification link"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Check if email is already verified
            if user.is_email_verified:
                return Response(
                    {"message": "Email already verified"}, 
                    status=status.HTTP_200_OK
                )
                
            # Update user status
            user.is_email_verified = True
            user.is_active = True  # Activate the user account
            user.save()

            return Response(
                {"message": "Email verified successfully! Your account is now active."}, 
                status=status.HTTP_200_OK
            )
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"error": "Invalid verification link"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver

@receiver(reset_password_token_created)
def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
    """
    Handle password reset token creation and send email
    """
    # Build the reset URL (frontend URL)
    reset_url = f"http://localhost:5173/password-reset/{reset_password_token.key}/"
    
    # Prepare email context
    context = {
        'user': reset_password_token.user,
        'reset_url': reset_url,
        'site_name': getattr(settings, 'SITE_NAME', 'Our Site'),
        'email_address': reset_password_token.user.email,
    }
    
    # Render HTML template
    html_message = render_to_string("accounts/email_reset.html", context)
    
    # Create plain text version (optional but recommended)
    plain_message = strip_tags(html_message)
    
    # Create and send email
    email = EmailMultiAlternatives(
        subject=f"Password Reset Request for {reset_password_token.user.email}",
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,  # Use from .env
        to=[reset_password_token.user.email],
    )
    email.attach_alternative(html_message, "text/html")
    
    try:
        email.send()
        print(f"Password reset email sent to {reset_password_token.user.email}")
    except Exception as e:
        print(f"Error sending password reset email: {e}")