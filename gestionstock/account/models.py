from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .managers import CustomUserManager


# Create your models here.
class EnterpriseUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=240, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(
        Group,
        related_name="enterpriseuser_set",  # <-- avoid conflict
        blank=True,
        verbose_name=("groups"),
        help_text=("The groups this user belongs to."),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="enterpriseuser_set",  # <-- avoid conflict
        blank=True,
        verbose_name=("user permissions"),
        help_text=("Specific permissions for this user."),
    )
    objects = CustomUserManager()


class Role(models.Model):
    name = models.CharField("Role utilisateur", max_length=100)
    user = models.ForeignKey(EnterpriseUser, on_delete=models.CASCADE)
