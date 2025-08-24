from django.urls import path,include
from .views import RegistrationView, VerifyEmailView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path('verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
] 
