from django.urls import path
from . import views 

urlpatterns = [
    # --- PAGINE PUBBLICHE ---
    path('', views.landing, name='landing'),
    path('purpose/', views.purpose, name='purpose'),
    path('scuole/', views.scuole, name='scuole'),
    path('scuole_public/', views.scuole_public, name='scuole_public'),
    path('aziende_public/', views.aziende_public, name='aziende_public'),
    path('chisiamo/', views.chisiamo, name='chisiamo'),
    path('faq/', views.faq, name='faq'),
    
    # --- SEZIONE SCUOLA (Visualizzazione, Modifica e Istruzioni) ---
    path('scuola/scheda/', views.scuola_scheda_scuola_detail, name='scuola_scheda_scuola_detail'),
    path('scuola/scheda/modifica/', views.scuola_scheda_scuola_edit, name='scuola_scheda_scuola_edit'),
    path('scuola/situazione/', views.scuola_situazione_studenti, name='scuola_situazione_studenti'),
    path('scuola/istruzioni/', views.scuola_istruzioni, name='scuola_istruzioni'),
    path('scuole/<int:pk>/', views.scuola_detail, name='scuola_detail'),

    # --- SEZIONE ENTE E AZIENDE (Gestione Partner) ---
    path('ente/dati/', views.ente_dati_detail, name='ente_dati_detail'),
    path('ente/dati/modifica/', views.ente_dati_edit, name='ente_dati_edit'),
    path('ente/aziende/', views.ente_aziende_list, name='ente_aziende_list'),
    path('ente/aziende/nuova/', views.ente_azienda_create, name='ente_azienda_create'),
    path('ente/aziende/<int:pk>/mod/', views.ente_azienda_update, name='ente_azienda_update'),
    path('ente/aziende/<int:pk>/chiudi-anno/', views.azienda_chiudi_anno, name='ente_azienda_chiudi_anno'),
    path('ente/aziende/<int:pk>/del/', views.ente_azienda_delete, name='ente_azienda_delete'),
    path('aziende/<int:pk>/', views.azienda_detail, name='azienda_detail'),
    path('ente/scheda/', views.ente_scheda_azienda, name='ente_scheda_azienda'),
    path('ente/istruzioni/', views.ente_istruzioni, name='ente_istruzioni'),
    path('enti/<int:pk>/', views.ente_detail, name='ente_detail'),
    
    # --- DASHBOARD & VISTE DI COLLEGAMENTO (Hub e Visibilità) ---
    path('scuola/', views.scuola_hub, name='scuola_hub'),
    path('ente/', views.ente_hub, name='ente_hub'),
    path('scuola/visibili/', views.scuola_visibili, name='scuola_visibili'),
    path('ente/visibili/', views.ente_visibili, name='ente_visibili'),

    # --- FUNZIONALITÀ DI SISTEMA (Gestione Account) ---
    path('account/richiedi-cancellazione/', views.richiedi_cancellazione, name='richiedi_cancellazione'),
]