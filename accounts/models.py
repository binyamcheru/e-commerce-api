import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.
class CustomUserManger(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email: 
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('role','superadmin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email,password,**extra_fields)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,unique=True)
    ROLE_CHOICES = (
        ("superadmin","SuperAdmin"),
        ("admin","Admin"),
        ("customer","Customer"),
        ("guest","Guest"),
    )
    username = None
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    oauth_provider = models.CharField(max_length=50, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # no username is required

    objects = CustomUserManger()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return self.email