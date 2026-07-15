from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Modello utente personalizzato che estende l'AbstractUser di Django.
    Aggiunge la gestione dei ruoli per distinguere tra Scuole ed Enti partner.
    """
    ROLE_CHOICES = (
        ('SCUOLA', 'Scuola'),
        ('ENTE', 'Ente'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='SCUOLA')

    def __str__(self): 
        return f"{self.username} ({self.role})"


class ActivationToken(models.Model):
    """
    Modello per la gestione dei token di attivazione degli account.
    Utilizzato per verificare le registrazioni o i processi di attivazione dei profili.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Token di attivazione per {self.user.username}"