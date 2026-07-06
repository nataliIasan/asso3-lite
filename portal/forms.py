from django import forms
from .models import Ente, Azienda, Scuola

# --- ENTE (СТРАНИЦА 23) ---
class EnteForm(forms.ModelForm):
    class Meta:
        model = Ente
        fields = ['nome', 'telefono', 'email', 'doti_disponibili', 'servizi_extra']
        labels = {
            'nome': 'Nome ente',
            'telefono': 'Telefono',
            'email': 'Email',
            'doti_disponibili': 'Doti disponibili',
            'servizi_extra': 'Servizi offerti oltre a FSL',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Es. Associazione Asso'}),
            'telefono': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Telefono'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}),
            'doti_disponibili': forms.NumberInput(attrs={'class': 'input', 'min': 0}),
            'servizi_extra': forms.Textarea(attrs={'class': 'input', 'rows': 6, 'maxlength': '2000',
                                                   'placeholder': 'Descrizione (max 2000)'}),
        }


# --- AZIENDA (СТРАНИЦЫ 25, 31) ---
class AziendaForm(forms.ModelForm):
    class Meta:
        model = Azienda
        # Поменяли поле pcto_attivati_anni на fsl_attivati_anni
        fields = ['nome', 'settore', 'referente_contatti', 'fsl_attivati_anni', 'foto', 'video']
        labels = {   
            'nome': 'Nome azienda',
            'settore': 'Settore',
            'referente_contatti': 'Contatto referente',
            'fsl_attivati_anni': 'FSL attivi',
            'foto': 'Foto (URL o File)',
            'video': 'Video (URL)',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Es. Alfa S.r.l.'}),
            'settore': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Es. Informatica'}),
            'referente_contatti': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Nome, email, telefono'}),
            'fsl_attivati_anni': forms.TextInput(attrs={'class': 'input'}),
            'foto': forms.FileInput(attrs={'class': 'input'}),
            'video': forms.URLInput(attrs={'class': 'input', 'placeholder': 'https://...'}),
        }


# --- SCUOLA: SCHEDA SCUOLA (СТРАНИЦА 15) ---
class ScuolaForm(forms.ModelForm):
    class Meta:
        model = Scuola
        # Выносим только основные редактируемые данные школы.
        # Остальные поля на стр. 15 вычисляются автоматически, вводить их руками не нужно.
        fields = [
            "nome",
            "codice_meccanografico",
            "email",
            "telefono",
            "indirizzo",
        ]
        labels = {
            "nome": "Nome scuola:",
            "codice_meccanografico": "Codice meccanografico:",
            "email": "Email:",
            "telefono": "Telefono:",
            "indirizzo": "Indirizzo:",
        }
        widgets = {
            "nome": forms.TextInput(attrs={"class": "input"}),
            "codice_meccanografico": "Scuola" == forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
            "telefono": forms.TextInput(attrs={"class": "input"}),
            "indirizzo": forms.TextInput(attrs={"class": "input"}),
        }


# --- SCUOLA: SITUAZIONE STUDENTI (СТРАНИЦА 16) ---
class SituazioneStudentiForm(forms.ModelForm):
    class Meta:
        model = Scuola
        # Поля ввода для распределения студентов и планов FSL
        fields = [
            "numero_studenti_quinto",
            "numero_studenti_quarto",
            "numero_studenti_triennio",
            "numero_fsl_da_attivare",
            "numero_fsl_attivati",
        ]
        labels = {
            "numero_studenti_quinto": "Numero studenti al quinto anno:",
            "numero_studenti_quarto": "Numero studenti al quarto anno:",
            "numero_studenti_triennio": "Numero studenti dei primi tre anni:",
            "numero_fsl_da_attivare": "Numero FSL da attivare nell'AS:",
            "numero_fsl_attivati": "Numero FSL attivati nell'AS:",
        }
        widgets = {
            "numero_studenti_quinto": forms.NumberInput(attrs={"class": "input", "min": 0}),
            "numero_studenti_quarto": forms.NumberInput(attrs={"class": "input", "min": 0}),
            "numero_studenti_triennio": forms.NumberInput(attrs={"class": "input", "min": 0}),
            "numero_fsl_da_attivare": forms.NumberInput(attrs={"class": "input", "min": 0}),
            "numero_fsl_attivati": forms.NumberInput(attrs={"class": "input", "min": 0}),
        }