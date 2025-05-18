from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=240, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


"""
Pourquoi ne pas utiliser le modèle de base de Django pour les rôles et permissions ?
Sinon c'est valide quand même
"""
class Role(models.Model):
    name = models.CharField("Role utilisateur", max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
