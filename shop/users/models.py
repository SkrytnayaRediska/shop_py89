from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email field is required")
        if not password:
            raise ValueError("Password field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50, blank=True, null=True, default=None)
    last_name = models.CharField(max_length=50, blank=True, null=True, default=None)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, default=None)
    cashback_points = models.IntegerField(default=0)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_mailing_required = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, _):
        return self.is_superuser

    def has_perm(self, _, __=None):
        return self.is_superuser
