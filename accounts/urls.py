from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- AUTENTICAZIONE (Login & Logout) ---
    path('login/', views.RoleLoginView.as_view(), name='login'),
    path('logout/', views.RoleLogoutView.as_view(), name='logout'),

    # --- REINDIRIZZAMENTO & OPZIONI DI ACCESSO ---
    # Gestisce lo smistamento iniziale all'Hub corretto dopo il login
    path('post-login/', views.post_login, name='post_login'),
    # Pagina di scelta per l'accesso (Scuola o Ente)
    path('auth/choose/', views.login_options, name='login_options'),

    # --- REGISTRAZIONE DEI PROFILI ---
    path('signup/scuola-full/', views.signup_scuola_full, name='signup_scuola_full'),
    path('signup/ente-full/', views.signup_ente_full, name='signup_ente_full'), 
    
    # --- ATTIVAZIONE ACCOUNT ---
    # Gestisce la verifica del token inviato via email per attivare l'utente
    path('activate/<str:token>/', views.activate, name='activate'),

    # --- GESTIONE COOPERA/RIPRISTINO PASSWORD (Django Auth + Template personalizzati) ---
    path(
        'password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), 
        name='password_reset'
    ),
    path(
        'password_reset_done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), 
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), 
        name='password_reset_confirm'
    ),
    path(
        'reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
        name='password_reset_complete'
    ),
]
