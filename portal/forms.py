from django import forms
from .models import Ente, Azienda, Scuola


# --- SEZIONE ENTE ---

class EnteForm(forms.ModelForm):
    """
    Modulo per la gestione e la modifica dei dati anagrafici dell'Ente.
    Include la validazione del nome per evitare inserimenti puramente numerici.
    """
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
            'servizi_extra': forms.Textarea(attrs={
                'class': 'input', 
                'rows': 6, 
                'maxlength': '2000',
                'placeholder': 'Descrizione dei servizi (max 2000 caratteri)'
            }),
        }

    def clean_nome(self):
        """
        Validazione personalizzata: impedisce l'inserimento di un nome 
        composto interamente da numeri.
        """
        nome = self.cleaned_data.get('nome')
        if nome and nome.isdigit():
            raise forms.ValidationError("Il nome dell'ente non può essere composto solo da numeri.")
        return nome


# --- SEZIONE AZIENDA (Gestione Partner) ---

class AziendaForm(forms.ModelForm):
    """
    Modulo per l'inserimento e la modifica delle aziende partner dell'Ente.
    Mantiene bloccato il contatore totale delle FSL, gestito via backend.
    """
    class Meta:
        model = Azienda
        fields = ['nome', 'referente_contatti', 'settore', 'fsl_attivati_anno_in_corso', 'fsl_attivati_totale', 'note']
        labels = {   
            'nome': 'Nome azienda:',
            'referente_contatti': 'Contatto referente:',
            'settore': 'Settore:',
            'fsl_attivati_anno_in_corso': 'FSL attivati nell\'anno in corso:',
            'fsl_attivati_totale': 'FSL attivati in totale:',
            'note': 'Note:',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Alfa s.r.l.'}),
            'referente_contatti': forms.TextInput(attrs={'class': 'input', 'placeholder': 'nome, email, tel.'}),
            'settore': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Informatica'}),
            
            # Campi numerici con limite minimo impostato a 0
            'fsl_attivati_anno_in_corso': forms.NumberInput(attrs={
                'class': 'input', 
                'min': 0, 
                'placeholder': 'Valore modificabile manualmente (X)'
            }),
            'fsl_attivati_totale': forms.NumberInput(attrs={'class': 'input', 'min': 0}),
            
            # Area di testo per note e informazioni sulle scoperture
            'note': forms.Textarea(attrs={
                'class': 'input', 
                'rows': 4, 
                'placeholder': 'Es. numero scoperture, altri contatti utili, informazioni particolari ecc.'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Rende il campo del totale in sola lettura (Readonly) sia in creazione che in modifica.
        # Il calcolo del totale storico viene gestito centralmente tramite l'azione "Chiudi anno".
        self.fields['fsl_attivati_totale'].widget.attrs['readonly'] = True
        self.fields['fsl_attivati_totale'].widget.attrs['placeholder'] = 'Calcolato automaticamente'
        self.fields['fsl_attivati_totale'].required = False


# --- SEZIONE SCUOLA: SCHEDA ANAGRAFICA  ---

class ScuolaForm(forms.ModelForm):
    """
    Modulo per l'aggiornamento dei dati anagrafici e di contatto della Scuola.
    """
    class Meta:
        model = Scuola
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
            "codice_meccanografico": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
            "telefono": forms.TextInput(attrs={"class": "input"}),
            "indirizzo": forms.TextInput(attrs={"class": "input"}),
        }


# --- SEZIONE SCUOLA: SITUAZIONE STUDENTI  ---

class SituazioneStudentiForm(forms.ModelForm):
    """
    Modulo per l'aggiornamento dei dati quantitativi degli studenti con certificazione 
    e pianificazione dei percorsi di tirocinio (FSL) attivi e da attivare.
    """
    class Meta:
        model = Scuola
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