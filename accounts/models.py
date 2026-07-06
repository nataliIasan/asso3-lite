from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('SCUOLA', 'Scuola'),
        ('ENTE', 'Ente'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='SCUOLA')

    def __str__(self): 
        return f"{self.username} ({self.role})"


class ActivationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Activation token for {self.user.username}"