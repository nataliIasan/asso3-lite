from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import EnteFullSignupForm, RoleLoginForm, ScuolaFullSignupForm
from .models import ActivationToken, User

# Inizializzazione del firmatario con timestamp per la gestione dei token temporali
signer = TimestampSigner()


class RoleLoginView(LoginView):
    """
    Vista di login personalizzata.
    Utilizza il modulo RoleLoginForm per applicare gli stili del brand.
    """
    authentication_form = RoleLoginForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        # Reindirizza alla vista post-login per lo smistamento in base al ruolo
        return reverse('post_login')


class RoleLogoutView(LogoutView):
    """
    Vista di logout.
    Reindirizza l'utente alla landing page principale dopo la disconnessione.
    """
    next_page = '/'


def post_login(request):
    """
    Gestisce lo smistamento dell'utente subito dopo l'accesso 
    reindirizzandolo all'Hub corrispondente in base al suo ruolo.
    """
    # Se l'utente non è autenticato, lo rimanda al login
    if not request.user.is_authenticated:
        return redirect('login')

    # Se è presente un parametro di reindirizzamento "next" (es. accesso a pagina protetta)
    next_page = request.GET.get('next')
    if next_page:
        return redirect(next_page)

    # Reindirizzamento in base al ruolo dell'utente
    if request.user.role == 'SCUOLA':
        return redirect('scuola_hub')
    elif request.user.role == 'ENTE':
        return redirect('ente_hub')

    # Fallback di sicurezza se si accede direttamente a /post-login
    if request.path.endswith('/post-login') or request.path.endswith('/post-login/'):
        return redirect('landing')

    return redirect('landing')


def login_options(request):
    """
    Mostra la pagina di selezione per l'accesso (Scuola o Ente).
    Se l'utente è già autenticato, lo reindirizza direttamente al suo Hub.
    """
    if request.user.is_authenticated:
        if request.user.role == 'SCUOLA':
            return redirect('scuola_hub')
        elif request.user.role == 'ENTE':
            return redirect('ente_hub')
        else:
            return redirect('landing')
            
    return render(request, 'portal/login_options.html')


def signup_scuola_full(request):
    """
    Gestisce il processo di registrazione per il profilo 'SCUOLA'.
    In modalità Demo, genera e mostra direttamente a schermo il link di attivazione.
    """
    if request.method == 'POST':
        form = ScuolaFullSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Generazione del token di sicurezza firmato con l'ID utente
            raw_token = signer.sign(user.pk)
            token = ActivationToken.objects.create(user=user, token=raw_token)

            # MODALITÀ DEMO: Generazione del link visibile direttamente a schermo
            activation_url = f"/accounts/activate/{token.token}/"
            messages.info(request, "Demo: copia il link di attivazione qui sotto.")

            return render(request, 'accounts/signup_done_demo.html', {
                'activation_url': activation_url
            })
    else:
        form = ScuolaFullSignupForm()

    return render(request, 'accounts/signup_scuola_full.html', {'form': form})


def signup_ente_full(request):
    """
    Gestisce il processo di registrazione per il profilo 'ENTE'.
    In modalità Demo, genera e mostra direttamente a schermo il link di attivazione.
    """
    if request.method == "POST":
        form = EnteFullSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Generazione del token di sicurezza firmato con l'ID utente
            raw_token = signer.sign(user.pk)
            token = ActivationToken.objects.create(user=user, token=raw_token)

            # MODALITÀ DEMO: Generazione del link visibile direttamente a schermo
            activation_url = f"/accounts/activate/{token.token}/"

            return render(request, "accounts/signup_done_demo.html", {
                "activation_url": activation_url
            })
    else:
        form = EnteFullSignupForm()

    return render(request, "accounts/signup_ente_full.html", {"form": form})


def activate(request, token):
    """
    Verifica il token di attivazione ricevuto tramite URL.
    Se valido ed entro i limiti di tempo (7 giorni), attiva l'utente e lo autentica.
    """
    rec = get_object_or_404(ActivationToken, token=token, used=False)
    
    try:
        # Verifica la firma del token e la scadenza impostata a 7 giorni (604800 secondi)
        user_pk = signer.unsign(token, max_age=604800)
    except SignatureExpired:
        messages.error(request, "Link di attivazione scaduto.")
        return redirect('login')
    except BadSignature:
        messages.error(request, "Link di attivazione non valido.")
        return redirect('login')

    # Controllo di integrità del token associato all'utente
    if int(user_pk) != rec.user_id:
        messages.error(request, "Link non valido.")
        return redirect('login')

    # Attivazione dell'utente e aggiornamento dello stato del token
    user = rec.user
    user.is_active = True
    user.save()
    
    rec.used = True
    rec.save()

    # Autenticazione automatica dell'utente dopo l'attivazione
    login(request, user)
    messages.success(request, "Account attivato con successo.")

    # Indirizzamento specifico in base al ruolo per i passaggi successivi
    if getattr(user, 'role', '') == 'SCUOLA':
        target = 'scuola_hub'
    elif getattr(user, 'role', '') == 'ENTE':
        target = 'ente_dati'
    else:
        target = 'landing'  # Fallback sicuro sulla landing page

    return redirect(target)