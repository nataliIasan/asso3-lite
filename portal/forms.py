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

    # ВАЛИДАЦИЯ ИМЕНИ: Находится строго НА УРОВНЕ класса Meta (4 пробела от края)
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        
        # Если имя состоит ТОЛЬКО из цифр, выкидываем ошибку
        if nome and nome.isdigit():
            raise forms.ValidationError("Il nome dell'ente non può essere composto solo da numeri.")
            
        return nome


class AziendaForm(forms.ModelForm):
    class Meta:
        model = Azienda
        # Выводим новые поля из макета.
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
            'nome': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Alfa.srl'}),
            'referente_contatti': forms.TextInput(attrs={'class': 'input', 'placeholder': 'nome, email, tel.'}),
            'settore': forms.TextInput(attrs={'class': 'input', 'placeholder': 'informatica'}),
            
            # Числовые поля с минимальным значением 0
            'fsl_attivati_anno_in_corso': forms.NumberInput(attrs={'class': 'input', 'min': 0, 'placeholder': 'num. modificabile manualmente (X)'}),
            'fsl_attivati_totale': forms.NumberInput(attrs={'class': 'input', 'min': 0}), # placeholder переопределим ниже динамически
            
            # Текстовое поле для заметок (4 строки в высоту)
            'note': forms.Textarea(attrs={'class': 'input', 'rows': 4, 'placeholder': 'es. num. scoperture, informazioni ecc.'}),
        }

    # ==========================================
    # 1. ДИНАМИЧЕСКИЙ ВНЕШНИЙ ВИД (ВЫРАВНИВАНИЕ ОТСТУПОВ)
    # ==========================================
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:
            # ЕСЛИ МОДИФИКАЦИЯ: намертво блокируем тотал, делаем его серым
            self.fields['fsl_attivati_totale'].widget.attrs['readonly'] = 'readonly'
            self.fields['fsl_attivati_totale'].widget.attrs['style'] = 'background-color: #f5f5f5; cursor: not-allowed;'
            self.fields['fsl_attivati_totale'].widget.attrs['placeholder'] = 'Calcolato automaticamente'
        else:
            # ЕСЛИ РЕГИСТРАЦИЯ: поле открыто для ввода суммы прошлых лет (Y)
            self.fields['fsl_attivati_totale'].widget.attrs['placeholder'] = 'Введи итог за прошлые года (если есть)'

    # ==========================================
    # 2. АВТОМАТИЧЕСКАЯ МАТЕМАТИКА ПРИ СОХРАНЕНИИ
    # ==========================================
    def save(self, commit=True):
        azienda = super().save(commit=False)
        
        if self.instance.pk:
            # ЛОГИКА ДЛЯ МОДИФИКАЦИИ: считаем разницу текущего года
            old_instance = Azienda.objects.get(pk=self.instance.pk)
            old_anno = old_instance.fsl_attivati_anno_in_corso or 0
            old_totale = old_instance.fsl_attivati_totale or 0
            new_anno = azienda.fsl_attivati_anno_in_corso or 0
            
            # Формула: Старый тотал + (Новый год - Старый год)
            azienda.fsl_attivati_totale = old_totale + (new_anno - old_anno)
        else:
            # ЛОГИКА ДЛЯ РЕГИСТРАЦИИ НОВОЙ КОМПАНИИ:
            # Если админ оставил тотал пустым, он равен текущему году
            if not azienda.fsl_attivati_totale:
                azienda.fsl_attivati_totale = azienda.fsl_attivati_anno_in_corso or 0
            # Если админ ввел общее число руками (прошлые года + текущий), сохраняем его
            elif azienda.fsl_attivati_totale < (azienda.fsl_attivati_anno_in_corso or 0):
                # Защита от дурака: тотал не может быть меньше текущего года
                azienda.fsl_attivati_totale = azienda.fsl_attivati_anno_in_corso or 0

        if commit:
            azienda.save()
        return azienda


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
class ScuolaForm(forms.ModelForm):
    class Meta:
        model = Scuola
        # Выносим только основные редактируемые данные школы.
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
            # ИСПРАВЛЕНО: убрали ошибочное сравнение "Scuola" ==, теперь поле закруглится!
            "codice_meccanografico": forms.TextInput(attrs={"class": "input"}),
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