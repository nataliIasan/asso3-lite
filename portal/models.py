from django.conf import settings
from django.db import models

class Scuola(models.Model):
    # Привязка школы к аккаунту пользователя-SCUOLA
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scuola_profile',
        null=True,
        blank=True
    )
    nome = models.CharField(max_length=200)
    codice_meccanografico = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    indirizzo = models.CharField(max_length=255, blank=True)
    
    # Поля из макапа "Situazione studenti con certificazione"
    numero_studenti_quinto = models.PositiveIntegerField(default=0)   # пятый год
    numero_studenti_quarto = models.PositiveIntegerField(default=0)   # четвертый год
    numero_studenti_triennio = models.PositiveIntegerField(default=0) # первые три года
    
    # Поля для FSL из макапа "Situazione studenti con certificazione"
    numero_fsl_da_attivare = models.PositiveIntegerField(default=0)
    numero_fsl_attivati = models.PositiveIntegerField(default=0)

    # --- АВТОМАТИЧЕСКИЕ РАСЧЕТЫ И ДУБЛИРОВАНИЕ ДЛЯ МАКУПОВ ---

    @property
    def numero_studenti_certificati(self):
        """
        = campo 1 + campo 2 + campo 3 (Макап Scheda scuola)
        Суммирует студентов 5-го, 4-го и первых 3-х классов.
        """
        return self.numero_studenti_quinto + self.numero_studenti_quarto + self.numero_studenti_triennio

    @property
    def numero_fsl_ancora_da_attivare(self):
        """
        = n FSL da attivare - numero FSL attivate nell'AS (Макап Situazione studenti)
        """
        return max(0, self.numero_fsl_da_attivare - self.numero_fsl_attivati)

    def __str__(self): 
        return self.nome


class Ente(models.Model):
    # Привязка к аккаунту пользователя-ENTE
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ente_profile',
        null=False, 
        blank=False,
    )
    nome = models.CharField(max_length=200)
    codice_fiscale = models.CharField(max_length=16, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    doti_disponibili = models.PositiveIntegerField(default=0)
    servizi_extra = models.TextField(blank=True, max_length=2000)

    def __str__(self): 
        # Если имя есть — выводим его, если пусто — выводим красивую заглушку с ID
        return self.nome if self.nome else f"Ente senza nome (ID: {self.pk})"


class Azienda(models.Model):
    ente = models.ForeignKey(Ente, on_delete=models.CASCADE, related_name='aziende')
    nome = models.CharField(max_length=200)
    settore = models.CharField(max_length=120, blank=True)
    referente_contatti = models.CharField(max_length=255, blank=True)
    
    # === НОВЫЕ ПОЛЯ ДЛЯ СЧЁТЧИКОВ ИЗ МАКЕТА ===
    fsl_attivati_anno_in_corso = models.PositiveIntegerField(default=0)  # Наш счётчик "X"
    fsl_attivati_totale = models.PositiveIntegerField(default=0)         # Наш архивный итог "Y"
    note = models.TextField(blank=True, max_length=2000)                 # Большое поле для заметок (scoperture и др.)

    # === СТАРЫЕ ПОЛЯ (Оставляем для сохранности текущей базы данных) ===
    numero_scoperture = models.PositiveIntegerField(default=0)
    fsl_attivati_anni = models.CharField(max_length=120, blank=True) 
    foto = models.FileField(upload_to='aziende_foto/', blank=True, null=True)
    video = models.URLField(blank=True, null=True)

    def __str__(self): 
        return self.nome