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