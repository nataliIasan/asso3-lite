from django.urls import path
from . import views 

urlpatterns = [
    path('', views.landing, name='landing'),
    path('purpose/', views.purpose, name='purpose'),
    path('scuole/', views.scuole, name='scuole'),
    path('scuole_public/', views.scuole_public, name='scuole_public'),
    path('aziende_public/', views.aziende_public, name='aziende_public'),
    path('chisiamo/', views.chisiamo, name='chisiamo'),
    path('faq/', views.faq, name='faq'),
    
    # Страницы для Школы (Макапы 15, 16, 19)
    path('scuola/scheda/', views.scuola_scheda_scuola, name='scuola_scheda_scuola'),
    path('scuola/situazione/', views.scuola_situazione_studenti, name='scuola_situazione_studenti'),
    path('scuola/istruzioni/', views.scuola_istruzioni, name='scuola_istruzioni'),
    path('scuole/<int:pk>/', views.scuola_detail, name='scuola_detail'),

    # Страницы для Ente и Aziende
    path('ente/dati/', views.ente_dati, name='ente_dati'),
    path('ente/aziende/', views.ente_aziende_list, name='ente_aziende_list'),
    path('ente/aziende/nuova/', views.ente_azienda_create, name='ente_azienda_create'),
    path('ente/aziende/<int:pk>/mod/', views.ente_azienda_update, name='ente_azienda_update'),
    path('ente/aziende/<int:pk>/del/', views.ente_azienda_delete, name='ente_azienda_delete'),
    path('aziende/<int:pk>/', views.azienda_detail, name='azienda_detail'),
    path('ente/scheda/', views.ente_scheda_azienda, name='ente_scheda_azienda'),
    path('ente/istruzioni/', views.ente_istruzioni, name='ente_istruzioni'),
    path('enti/<int:pk>/', views.ente_detail, name='ente_detail'),
    
    # Хабы и списки видимости
    path('scuola/', views.scuola_hub, name='scuola_hub'),
    path('ente/', views.ente_hub, name='ente_hub'),
    path('scuola/visibili/', views.scuola_visibili, name='scuola_visibili'),
    path('ente/visibili/', views.ente_visibili, name='ente_visibili'),
]