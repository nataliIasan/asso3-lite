from django.contrib import messages
from django.contrib.auth.decorators import login_required as _login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from accounts.decorators import login_required, role_required
# AGGIORNATO: Importazione dei nuovi moduli per la gestione del blocco note
from .forms import AziendaForm, EnteForm, ScuolaForm, SituazioneStudentiForm, NotaScuolaForm, NotaEnteForm
from .models import Azienda, Ente, Scuola, NotaScuola, NotaEnte


# --- VISTE PUBBLICHE ---

def landing(request):
    """
    Rende la Landing Page principale del progetto ASSO.
    Fornisce al template l'elenco delle scuole e delle aziende partner.
    """
    scuole = Scuola.objects.all()
    aziende = Azienda.objects.all()
    context = {
        'scuole': scuole,
        'aziende': aziende,
        'user': request.user,
    }
    return render(request, 'portal/landing.html', context)


def purpose(request): 
    """Rende la pagina degli obiettivi del progetto (Scopo)."""
    return render(request, 'portal/purpose.html')


def chisiamo(request): 
    """Rende la pagina descrittiva "Chi Siamo"."""
    return render(request, 'portal/chisiamo.html')
    

def faq(request): 
    """Rende la pagina delle domande frequenti (FAQ)."""
    return render(request, 'portal/faq.html')


def scuole(request):  
    """Rende la pagina interna con l'elenco completo delle scuole registrate."""
    return render(request, 'portal/scuole.html', {'items': Scuola.objects.all()})
    

def aziende(request): 
    """Rende la pagina interna con l'elenco completo delle aziende registrate."""
    return render(request, 'portal/aziende.html', {'items': Azienda.objects.all()})


def scuole_public(request):
    """Rende l'elenco delle scuole accessibile pubblicamente (senza login)."""
    scuole_list = Scuola.objects.all()
    return render(request, 'portal/scuole_public.html', {'items': scuole_list})


def aziende_public(request):
    """Rende l'elenco delle aziende accessibile pubblicamente (senza login)."""
    aziende_list = Azienda.objects.all()
    return render(request, 'portal/aziende_public.html', {'items': aziende_list})


def enti_public(request):
    """Rende l'elenco degli enti accessibile pubblicamente (senza login)."""
    enti_list = Ente.objects.all()
    return render(request, 'portal/enti_public.html', {'items': enti_list})


# --- DASHBOARD / HUB UTENTI (ACCESSO LIMITATO) ---

@login_required 
@role_required('SCUOLA')
def scuola_hub(request): 
    """Rende la dashboard principale (Hub) per gli utenti di tipo Scuola."""
    return render(request, 'portal/scuola_hub.html')


@login_required 
@role_required('ENTE')
def ente_hub(request): 
    """Rende la dashboard principale (Hub) per gli utenti di tipo Ente."""
    return render(request, 'portal/ente_hub.html')


@login_required 
@role_required('SCUOLA')
def scuola_visibili(request):
    """
    Mostra all'utente Scuola l'elenco di tutti gli Enti partner disponibili
    (corrispondente alle pagine 12/13 del mockup).
    """
    enti = Ente.objects.all().order_by('nome')
    return render(request, 'portal/scuola_visibili.html', {'enti': enti})


@login_required 
@role_required('ENTE')
def ente_visibili(request):
    """
    Mostra all'Ente l'elenco completo delle Scuole e solo le proprie Aziende associate
    (corrispondente alle pagine 21/22 del mockup).
    """
    scuole_list = Scuola.objects.all().order_by('nome')
    aziende_list = Azienda.objects.filter(ente__user=request.user)
    return render(request, 'portal/ente_visibili.html', {
        'scuole': scuole_list, 
        'aziende': aziende_list
    })


# =====================================================================
# --- VISTE PER UTENTI: SCUOLA ---
# =====================================================================

@login_required
@role_required('SCUOLA')
def scuola_scheda_scuola_detail(request):
    """
    Pagina 15 (Visualizzazione): Consente alla Scuola di visualizzare i propri dati.
    Tutti i campi del modulo sono forzati in modalità sola lettura (Read-only).
    """
    scuola, _ = Scuola.objects.get_or_create(user=request.user)
    form = ScuolaForm(instance=scuola)
    
    # Blocca tutti i campi per impedire modifiche accidentali nella vista di dettaglio
    for field in form.fields.values():
        field.widget.attrs['readonly'] = True
        field.widget.attrs['disabled'] = True

    return render(request, 'portal/scuola_scheda_scuola_detail.html', {
        'form': form, 
        'scuola': scuola
    })


@login_required
@role_required('SCUOLA')
def scuola_scheda_scuola_edit(request):
    """
    Pagina 15 (Modifica): Consente alla Scuola di aggiornare i propri dati anagrafici.
    Al termine del salvataggio, reindirizza alla vista di dettaglio (Read-only).
    """
    scuola, _ = Scuola.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ScuolaForm(request.POST, instance=scuola)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Scheda SCUOLA salvata con successo.')
            return redirect('scuola_scheda_scuola_detail')
    else:
        form = ScuolaForm(instance=scuola)
        
    return render(request, 'portal/scuola_scheda_scuola_edit.html', {
        'form': form, 
        'scuola': scuola
    })


@login_required
@role_required('SCUOLA')
def scuola_situazione_studenti(request):
    """
    Pagina 16 (Gestione studenti): Consente alla Scuola di aggiornare la distribuzione 
    degstudi certificati e la pianificazione dei tirocini (FSL).
    """
    scuola, _ = Scuola.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = SituazioneStudentiForm(request.POST, instance=scuola)
        if form.is_valid():
            form.save()
            messages.success(request, 'Situazione studenti aggiornata con successo.')
            return redirect('scuola_hub')
    else:
        form = SituazioneStudentiForm(instance=scuola)

    return render(request, 'portal/scuola_situazione_studenti.html', {
        'form': form, 
        'scuola': scuola
    })


@login_required
@role_required('SCUOLA')
def scuola_istruzioni(request):
    """
    Pagina 19: Gestisce la visualizzazione delle istruzioni operative (FAQ)
    e l'inserimento di nuove note/commenti nel Blocco Note condiviso della Scuola.
    """
    scuola, _ = Scuola.objects.get_or_create(user=request.user)
    note = scuola.note_scuola.all()
    
    if request.method == 'POST':
        form = NotaScuolaForm(request.POST)
        if form.is_valid():
            nuova_nota = form.save(commit=False)
            nuova_nota.scuola = scuola
            nuova_nota.autore = request.user
            nuova_nota.save()
            messages.success(request, 'Nota aggiunta con successo al blocco note.')
            return redirect('scuola_istruzioni')
    else:
        form = NotaScuolaForm()

    return render(request, 'portal/scuola_istruzioni.html', {
        'scuola': scuola,
        'note': note,
        'form': form
    })


# =====================================================================
# --- VISTE PER UTENTI: ENTE ---
# =====================================================================

@login_required
@role_required('ENTE')
def ente_dati_detail(request):
    """
    Pagina 23 (Visualizzazione): Consente all'Ente di visualizzare il proprio profilo.
    I campi del modulo sono bloccati in modalità sola lettura.
    """
    ente, _ = Ente.objects.get_or_create(user=request.user)
    form = EnteForm(instance=ente)
    
    for field in form.fields.values():
        field.widget.attrs['readonly'] = True
        field.widget.attrs['disabled'] = True

    return render(request, 'portal/ente_dati_detail.html', {'form': form, 'ente': ente})


@login_required
@role_required('ENTE')
def ente_dati_edit(request):
    """
    Pagina 23 (Modifica): Consente all'Ente di modificare i propri dati e le doti disponibili.
    """
    ente, _ = Ente.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EnteForm(request.POST, instance=ente)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Dati ente aggiornati con successo.')
            return redirect('ente_dati_detail')
    else:
        form = EnteForm(instance=ente)

    return render(request, 'portal/ente_dati_edit.html', {'form': form, 'ente': ente})


@login_required
@role_required('ENTE')
def ente_aziende_list(request):
    """Pagina 24: Elenca tutte le aziende partner gestite dall'Ente corrente."""
    ente = get_object_or_404(Ente, user=request.user)
    aziende_list = Azienda.objects.filter(ente=ente).order_by('nome')
    return render(request, 'portal/ente_aziende_list.html', {'aziende': aziende_list})


@login_required
@role_required('ENTE')
def ente_azienda_create(request):
    """Pagina 25: Consente ad un Ente di registrare una nuova azienda partner."""
    ente = get_object_or_404(Ente, user=request.user)
    if request.method == 'POST':
        form = AziendaForm(request.POST)
        if form.is_valid():
            az = form.save(commit=False)
            az.ente = ente
            az.save()
            messages.success(request, 'Azienda partner creata con successo.')
            return redirect('ente_aziende_list')
    else:
        form = AziendaForm()
    return render(request, 'portal/ente_azienda_form.html', {'form': form, 'mode': 'create'})


@login_required
@role_required('ENTE')
def ente_azienda_update(request, pk):
    """Pagina 31: Consente ad un Ente di modificare i dettagli di una propria azienda partner."""
    ente = get_object_or_404(Ente, user=request.user)
    azienda = get_object_or_404(Azienda, pk=pk, ente=ente)
    if request.method == 'POST':
        form = AziendaForm(request.POST, instance=azienda)
        if form.is_valid():
            form.save()
            messages.success(request, "Scheda AZIENDA aggiornata con successo.")
            return redirect('ente_aziende_list')
    else:
        form = AziendaForm(instance=azienda)
    return render(request, 'portal/ente_azienda_form.html', {'form': form, 'mode': 'update'})


@login_required
@role_required('ENTE')
def ente_azienda_delete(request, pk):
    """Pagina 32: Gestisce la rimozione definitiva di un'azienda partner di competenza dell'Ente."""
    ente = get_object_or_404(Ente, user=request.user)
    azienda = get_object_or_404(Azienda, pk=pk, ente=ente)
    if request.method == 'POST':
        azienda.delete()
        messages.success(request, "Scheda AZIENDA eliminata con successo.")
        return redirect('ente_aziende_list')
    return render(request, 'portal/ente_azienda_confirm_delete.html', {'azienda': azienda})


@login_required
@role_required('ENTE')
def ente_istruzioni(request):
    """
    Pagina 26: Gestisce la visualizzazione delle istruzioni operative (FAQ)
    e l'inserimento di nuove note/commenti nel Blocco Note condiviso dell'Ente.
    """
    ente, _ = Ente.objects.get_or_create(user=request.user)
    note = ente.note_ente.all()
    
    if request.method == 'POST':
        form = NotaEnteForm(request.POST)
        if form.is_valid():
            nuova_nota = form.save(commit=False)
            nuova_nota.ente = ente
            nuova_nota.autore = request.user
            nuova_nota.save()
            messages.success(request, 'Nota aggiunta con successo al blocco note.')
            return redirect('ente_istruzioni')
    else:
        form = NotaEnteForm()

    return render(request, 'portal/ente_istruzioni.html', {
        'ente': ente,
        'note': note,
        'form': form
    })


@login_required
@role_required('ENTE')
def ente_scheda_azienda(request):
    """Vista ausiliaria per il salvataggio rapido di un'azienda."""
    if request.method == 'POST':
        form = AziendaForm(request.POST)
        if form.is_valid():
            azienda = form.save(commit=False)
            azienda.ente = request.user.ente_profile  
            azienda.save()
            messages.success(request, 'Scheda AZIENDA salvata con successo.')
            return redirect('ente_hub')
    else:
        form = AziendaForm()
    return render(request, 'portal/ente_scheda_azienda.html', {'form': form})


@login_required
@role_required('ENTE')
def azienda_chiudi_anno(request, pk):
    """
    Azione di chiusura dell'anno scolastico per un'azienda partner:
    Accumula i tirocini correnti nello storico e resetta il contatore dell'anno corrente.
    Formula di calcolo: Y (totale storico) = X (anno corrente) + Y, dopodiché X = 0.
    """
    ente = get_object_or_404(Ente, user=request.user)
    azienda = get_object_or_404(Azienda, pk=pk, ente=ente)
    
    azienda.fsl_attivati_totale += azienda.fsl_attivati_anno_in_corso
    azienda.fsl_attivati_anno_in_corso = 0
    azienda.save()
    
    messages.success(request, f"Anno scolastico chiuso con successo per {azienda.nome}.")
    return redirect('ente_azienda_update', pk=azienda.pk)


# --- VISTE DI DETTAGLIO CONDIVISE / INTER-RUOLO ---

@login_required
def ente_detail(request, pk):
    """Pagina 18: Consente la visualizzazione della scheda informativa di un Ente."""
    ente = get_object_or_404(Ente, pk=pk)
    return render(request, 'portal/ente_detail.html', {'ente': ente})


@login_required
def azienda_detail(request, pk):
    """Pagina 30: Consente la visualizzazione dettagliata di un'azienda partner."""
    azienda = get_object_or_404(Azienda, pk=pk)
    return render(request, 'portal/azienda_detail.html', {'azienda': azienda})


@login_required
def school_detail(request, pk):
    """Alias di compatibilità per il caricamento dei dettagli scuola."""
    return scuola_detail(request, pk)


@login_required
def scuola_detail(request, pk):
    """Pagina 28 e 29: Consente all'Ente di esaminare la situazione studenti di una Scuola."""
    scuola = get_object_or_404(Scuola, pk=pk)
    return render(request, 'portal/scuola_detail.html', {'scuola': scuola})


# =====================================================================
# --- SERVIZI DI SISTEMA ---
# =====================================================================

@login_required
def richiedi_cancellazione(request):
    """
    Gestisce l'invio di una notifica email all'amministratore di sistema
    in seguito alla richiesta di eliminazione dell'account da parte di un utente.
    """
    if request.method == 'POST':
        user = request.user
        
        subject = f"ASSO: Richiesta cancellazione account - {user.username}"
        message = (
            f"L'utente '{user.username}' ha richiesto la cancellazione del proprio account "
            f"dalla piattaforma ASSO.\n\n"
            f"Dettagli profilo:\n"
            f"- ID Utente: {user.pk}\n"
            f"- Username: {user.username}\n"
            f"- Email profilo: {user.email}\n"
        )
        from_email = 'noreply@asso.it'
        recipient_list = ['admin@asso.it']
        
        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(
                request, 
                "La tua richiesta è stata inviata all'amministratore. Riceverai una conferma via email."
            )
        except Exception:
            messages.error(
                request, 
                "Si è verificato un errore durante l'invio della richiesta. Riprova più tardi."
            )
        
        return redirect(request.META.get('HTTP_REFERER', 'landing'))
        
    return redirect('landing')