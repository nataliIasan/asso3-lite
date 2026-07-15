
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from portal.models import Scuola, Ente

User = get_user_model()


class RoleLoginForm(AuthenticationForm):
    """
    Modulo di login personalizzato.
    Gestisce l'autenticazione degli utenti applicando uno stile unificato 
    e classi CSS coerenti per tutti i campi di input.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
        self.fields["password"].label = "Password"
        
        # Applica la classe CSS 'input' definita nel brand guideline
        for f in self.fields.values():
            f.widget.attrs.update({"class": "input"})


class ScuolaFullSignupForm(UserCreationForm):
    """
    Modulo di registrazione completo per gli utenti di tipo 'SCUOLA'.
    Crea l'utente disattivato di default (in attesa di approvazione) 
    e genera automaticamente il relativo profilo Scuola associato.
    """
    nome_scuola = forms.CharField(label="Nome scuola:", max_length=200)
    codice_meccanografico = forms.CharField(label="Codice meccanografico (cf):", max_length=40)
    email = forms.EmailField(label="Email:")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Traduzione dei campi standard di Django ed eliminazione degli help_text nativi in inglese
        if "username" in self.fields:
            self.fields["username"].help_text = None
        if "password1" in self.fields:
            self.fields["password1"].label = "Password:"
            self.fields["password1"].help_text = None
        if "password2" in self.fields:
            self.fields["password2"].label = "Conferma password:"
            self.fields["password2"].help_text = None

        # Applica lo stile unificato del brand a tutti i widget
        for f in self.fields.values():
            f.widget.attrs.update({"class": "input"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "SCUOLA"
        user.email = self.cleaned_data["email"]
        user.is_active = False  # L'utente richiede l'attivazione manuale/amministrativa
        
        if commit:
            user.save()

        # Creazione del profilo della Scuola associato all'utente appena registrato
        Scuola.objects.create(
            nome=self.cleaned_data["nome_scuola"],
            codice_meccanografico=self.cleaned_data["codice_meccanografico"],
            user=user  
        )
        return user


class EnteFullSignupForm(UserCreationForm):
    """
    Modulo di registrazione completo per gli utenti di tipo 'ENTE'.
    Crea l'utente disattivato di default e genera il relativo profilo Ente associato.
    """
    nome_ente = forms.CharField(label="Nome ente:", max_length=200)
    codice_fiscale = forms.CharField(label="Codice Fiscale:", max_length=16)
    email = forms.EmailField(label="Email:")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Traduzione dei campi standard di Django ed eliminazione degli help_text nativi in inglese
        if "username" in self.fields:
            self.fields["username"].help_text = None
        if "password1" in self.fields:
            self.fields["password1"].label = "Password:"
            self.fields["password1"].help_text = None
        if "password2" in self.fields:
            self.fields["password2"].label = "Conferma password:"
            self.fields["password2"].help_text = None

        # Applica lo stile unificato del brand a tutti i widget
        for f in self.fields.values():
            f.widget.attrs.update({"class": "input"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "ENTE"
        user.email = self.cleaned_data["email"]
        user.is_active = False  # L'utente richiede l'attivazione manuale/amministrativa
        
        if commit:
            user.save()

        # Creazione del profilo dell'Ente associato all'utente appena registrato
        Ente.objects.create(
            nome=self.cleaned_data["nome_ente"],
            codice_fiscale=self.cleaned_data["codice_fiscale"],
            user=user
        )
        return user