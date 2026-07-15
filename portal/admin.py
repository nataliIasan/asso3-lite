from django.contrib import admin
from .models import Scuola, Ente, Azienda


@admin.register(Scuola)
class ScuolaAdmin(admin.ModelAdmin):
    """
    Personalizzazione dell'interfaccia di amministrazione per il modello Scuola.
    Consente di visualizzare i dettagli anagrafici, cercare per nome/codice 
    e monitorare i dati quantitativi degli istituti.
    """
    # Colonne visualizzate nell'elenco delle scuole
    list_display = ('nome', 'codice_meccanografico', 'email', 'telefono', 'indirizzo')
    
    # Campi abilitati per la ricerca rapida nella barra in alto
    search_fields = ('nome', 'codice_meccanografico', 'email')
    
    # Filtri laterali per una navigazione più rapida
    list_filter = ('numero_studenti_quinto', 'numero_studenti_quarto')


@admin.register(Ente)
class EnteAdmin(admin.ModelAdmin):
    """
    Personalizzazione dell'interfaccia di amministrazione per il modello Ente.
    Ottimizza la visualizzazione delle doti finanziarie e dei contatti dell'ente.
    """
    # Colonne principali con informazioni di contatto e budget doti
    list_display = ('nome', 'codice_fiscale', 'email', 'telefono', 'doti_disponibili')
    
    # Campi abilitati per la ricerca
    search_fields = ('nome', 'codice_fiscale', 'email')


@admin.register(Azienda)
class AziendaAdmin(admin.ModelAdmin):
    """
    Personalizzazione dell'interfaccia di amministrazione per il modello Azienda.
    Mostra l'associazione con l'Ente gestore e permette di monitorare i tirocini FSL.
    """
    # Colonne principali per tracciare settore, referente e l'Ente proprietario della scheda
    list_display = ('nome', 'settore', 'ente', 'referente_contatti', 'fsl_attivati_anno_in_corso')
    
    # Campi abilitati per la ricerca
    search_fields = ('nome', 'settore', 'referente_contatti')
    
    # Filtro laterale per raggruppare le aziende in base all'Ente di appartenenza o al settore
    list_filter = ('ente', 'settore')
