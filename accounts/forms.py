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
    nome_scuola = forms.CharField(label="Nome scuola", max_length=200)
    codice_meccanografico = forms.CharField(label="Codice meccanografico (cf)", max_length=40)
    email = forms.EmailField(label="Email")


    password2 = forms.CharField(
        label="Conferma password",
        widget=forms.PasswordInput,
        help_text=None
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # пароли унаследованы (password1/password2)
        fields = ("username", "email")
        help_texts = {
            "username": None,
            "password1": None,
            "password2": None,
}

    def save(self, commit=True):
        # создаём НЕактивного пользователя с ролью SCUOLA
        user = super().save(commit=False)
        user.role = "SCUOLA"
        user.email = self.cleaned_data["email"]
        user.is_active = False
        if commit:
            user.save()

        # профиль школы (привязываем к пользователю)
        Scuola.objects.create(
            nome=self.cleaned_data["nome_scuola"],
            codice_meccanografico=self.cleaned_data["codice_meccanografico"],
            # остальные поля опустим — у них есть blank/default
            # indirizzo, numero_studenti, numero_pcto_da_attivare
        )
        return user


class EnteFullSignupForm(UserCreationForm):
    # Доп. поля анкеты ENTE
    nome_ente = forms.CharField(label="Nome ente", max_length=200)
    codice_fiscale = forms.CharField(label="Codice Fiscale", max_length=16)
    email = forms.EmailField(label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")  # password1/2 унаследованы

    def save(self, commit=True):
        # создаём НЕактивного пользователя с ролью ENTE
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
        # профиль ENTE пока не создаём (данные введут на "Inserisci i dati del tuo ente")
        return user
