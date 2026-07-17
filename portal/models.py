from django.conf import settings
from django.db import models


class Scuola(models.Model):
    """
    Modello che rappresenta il profilo di un Istituto Scolastico.
    È associato in relazione One-to-One con l'utente di tipo 'SCUOLA'.
    Contiene i dati anagrafici e i dati quantitativi degli studenti certificati.
    """
    # Associazione del profilo scuola all'account utente
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scuola_profile',
        null=True,
        blank=True
    )
    nome = models.CharField(max_length=200)
    # OPZIONI PER LA TIPOLOGIA DI SCUOLA
    TIPOLOGIA_CHOICES = [
        ('LICEO', 'Liceo'),
        ('TECNICO', 'Istituto Tecnico'),
        ('PROFESSIONALE', 'Istituto Professionale'),
    ]
    tipologia = models.CharField(
        max_length=50,  
        blank=True,
        verbose_name="Tipologia"
    )
    codice_meccanografico = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    indirizzo = models.CharField(max_length=255, blank=True)
    
    # Campi quantitativi derivanti dal mockup "Situazione studenti con certificazione"
    numero_studenti_quinto = models.PositiveIntegerField(default=0)    # Quinto anno
    numero_studenti_quarto = models.PositiveIntegerField(default=0)    # Quarto anno
    numero_studenti_triennio = models.PositiveIntegerField(default=0)  # Primo triennio
    
    # Campi per la gestione dei tirocini (FSL - Formazione in Situazione di Lavoro)
    numero_fsl_da_attivare = models.PositiveIntegerField(default=0)
    numero_fsl_attivati = models.PositiveIntegerField(default=0)

    # --- CALCOLI AUTOMATICI E PROPRIETÀ (PROPERTY) ---

    @property
    def numero_studenti_certificati(self):
        """
        Calcola il totale complessivo degli studenti con certificazione.
        Somma i valori del quinto anno, del quarto anno e del primo triennio.
        """
        return self.numero_studenti_quinto + self.numero_studenti_quarto + self.numero_studenti_triennio

    @property
    def numero_fsl_ancora_da_attivare(self):
        """
        Calcola la differenza tra i tirocini pianificati (da attivare) e quelli già attivi.
        Restituisce 0 se il numero di attivati supera quello pianificato.
        """
        return max(0, self.numero_fsl_da_attivare - self.numero_fsl_attivati)

    def __str__(self): 
        return self.nome


class Ente(models.Model):
    """
    Modello che rappresenta il profilo dell'Ente partner del progetto ASSO.
    È associato in relazione One-to-One con l'utente di tipo 'ENTE'.
    Gestisce le doti di finanziamento disponibili e i servizi offerti.
    """
    # Associazione del profilo Ente all'account utente (campo obbligatorio)
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
        # Ritorna il nome dell'Ente, se vuoto usa un fallback sicuro con l'ID
        return self.nome if self.nome else f"Ente senza nome (ID: {self.pk})"


class Azienda(models.Model):
    """
    Modello che rappresenta un'Azienda partner registrata all'interno della piattaforma.
    Ogni azienda appartiene ad un Ente gestore principale (relazione ForeignKey).
    """
    ente = models.ForeignKey(Ente, on_delete=models.CASCADE, related_name='aziende')
    nome = models.CharField(max_length=200)
    settore = models.CharField(max_length=120, blank=True)
    referente_contatti = models.CharField(max_length=255, blank=True)
    
    # === NUOVI CAMPI PER LA GESTIONE DEI CONTATORI DEL LAYOUT (CANVA) ===
    fsl_attivati_anno_in_corso = models.PositiveIntegerField(default=0)  # Contatore 'X' dei tirocini correnti
    fsl_attivati_totale = models.PositiveIntegerField(default=0)         # Totale storico d'archivio 'Y'
    note = models.TextField(blank=True, max_length=2000)                 # Note interne per scoperture o contatti
    
    # === CAMPI PRECEDENTI (Mantenuti intatti per preservare l'integrità del database esistente) ===
    numero_scoperture = models.PositiveIntegerField(default=0)
    fsl_attivati_anni = models.CharField(max_length=120, blank=True) 
    foto = models.FileField(upload_to='aziende_foto/', blank=True, null=True)
    video = models.URLField(blank=True, null=True)

    def __str__(self): 
        return self.nome


# =====================================================================
# --- NUOVI MODELLI PER LA GESTIONE DEL BLOCCO NOTE CONDIVISO ---
# =====================================================================

class NotaScuola(models.Model):
    """
    Modello per gestire il Blocco Note condiviso (commenti interni) 
    tra gli operatori associati allo stesso Istituto Scolastico.
    """
    scuola = models.ForeignKey(Scuola, on_delete=models.CASCADE, related_name='note_scuola')
    # Utilizza la configurazione globale dell'utente per preservare l'integrità del database
    autore = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    testo = models.TextField()
    operatore = models.CharField(max_length=100, blank=True, null=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_creazione']  # Ordina i messaggi mostrando prima i più recenti


class NotaEnte(models.Model):
    """
    Modello per gestire il Blocco Note condiviso (commenti interni) 
    tra gli operatori associati allo stesso Ente partner.
    """
    ente = models.ForeignKey(Ente, on_delete=models.CASCADE, related_name='note_ente')
    # Utilizza la configurazione globale dell'utente per preservare l'integrità del database
    autore = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    testo = models.TextField()
    operatore = models.CharField(max_length=100, blank=True, null=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_creazione']  # Ordina i messaggi mostrando prima i più recenti