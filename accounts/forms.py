# accounts/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

from portal.models import Scuola
from portal.models import Ente

User = get_user_model()


class RoleLoginForm(AuthenticationForm):
    """Логин-форма с единым стилем input'ов."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
        self.fields["password"].label = "Password"
        for f in self.fields.values():
            f.widget.attrs.update({"class": "input"})


class ScuolaFullSignupForm(UserCreationForm):
    # Доп. поля анкеты SCUOLA
    nome_scuola = forms.CharField(label="Nome scuola:", max_length=200)
    codice_meccanografico = forms.CharField(label="Codice meccanografico (cf):", max_length=40)
    email = forms.EmailField(label="Email:")

    password2 = forms.CharField(
        label="Conferma password:",
        widget=forms.PasswordInput,
        help_text=None
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
        help_texts = {
            "username": None,
            "password1": None,
            "password2": None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({"class": "input"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "SCUOLA"
        user.email = self.cleaned_data["email"]
        user.is_active = False
        if commit:
            user.save()

        # Профиль школы с привязкой к юзеру
        Scuola.objects.create(
            nome=self.cleaned_data["nome_scuola"],
            codice_meccanografico=self.cleaned_data["codice_meccanografico"],
            user=user  
        )
        return user


class EnteFullSignupForm(UserCreationForm):
    # Доп. поля анкеты ENTE
    nome_ente = forms.CharField(label="Nome ente:", max_length=200)
    codice_fiscale = forms.CharField(label="Codice Fiscale:", max_length=16)
    email = forms.EmailField(label="Email:")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({"class": "input"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "ENTE"
        user.email = self.cleaned_data["email"]
        user.is_active = False
        if commit:
            user.save()

        ente = Ente.objects.create(
            nome=self.cleaned_data["nome_ente"],
            codice_fiscale=self.cleaned_data["codice_fiscale"],
            user=user
        )
        return user