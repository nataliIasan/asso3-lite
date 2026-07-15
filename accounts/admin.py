from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Personalizzazione dell'interfaccia di amministrazione di Django per il modello User.
    Estende l'amministrazione standard per visualizzare e gestire il campo personalizzato 'role'.
    """
    # Aggiunge la sezione 'Ruolo' nei dettagli dell'utente all'interno dell'Admin Django
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Ruolo', {'fields': ('role',)}),
    )
    
    # Colonne visualizzate nella lista degli utenti
    list_display = ('username', 'email', 'role', 'is_staff')
