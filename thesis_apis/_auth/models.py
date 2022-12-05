from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
import uuid


class CustomUsersManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email address!")

        user = self.model(
            email=self.normalize_email(email),

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.activated = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=50, unique=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    activated = models.BooleanField(default=False)
    # it's better to use uuid instead of id here
    # uuid = models.UUIDField(
    #     primary_key=True, default=uuid.uuid4, editable=False)

    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name="last login", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUsersManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-date_joined']


class RadiologistProfile(models.Model):

    user = models.OneToOneField(CustomUser, related_name="radiologist_profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)

    # is already added in the customuser model,should be removed from here
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
