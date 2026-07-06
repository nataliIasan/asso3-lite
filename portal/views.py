from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from accounts.decorators import login_required, role_required
from .models import Scuola, Ente, Azienda
# Имортируем новые чистые формы (убрали StudenteForm, добавили SituazioneStudentiForm)
from .forms import ScuolaForm, EnteForm, AziendaForm, SituazioneStudentiForm

def landing(request):
    scuole = Scuola.objects.all()
    aziende = Azienda.objects.all()
    context = {
        'scuole': scuole,
        'aziende': aziende,
        'user': request.user,
    }
    return render(request, 'portal/landing.html', context)


def purpose(request): 
    return render(request, 'portal/purpose.html')

def chisiamo(request): 
    return render(request, 'portal/chisiamo.html')
    
def faq(request): 
    return render(request, 'portal/faq.html')

def scuole(request):  
    return render(request, 'portal/scuole.html', {'items': Scuola.objects.all()})
    
def aziende(request): 
    return render(request, 'portal/aziende.html', {'items': Azienda.objects.all()})

def scuole_public(request):
    scuole = Scuola.objects.all()
    return render(request, 'portal/scuole_public.html', {'items': scuole})

def aziende_public(request):
    aziende = Azienda.objects.all()
    return render(request, 'portal/aziende_public.html', {'items': aziende})


@login_required 
@role_required('SCUOLA')
def scuola_hub(request): 
    return render(request, 'portal/scuola_hub.html')


@login_required 
@role_required('ENTE')
def ente_hub(request): 
    return render(request, 'portal/ente_hub.html')


@login_required 
@role_required('SCUOLA')
def scuola_visibili(request):
    # Показываем школе список всех организаций (как на стр. 12/13 макапа)
    enti = Ente.objects.all().order_by('nome')
    return render(request, 'portal/scuola_visibili.html', {'enti': enti})


@login_required 
@role_required('ENTE')
def ente_visibili(request):
    # Показываем организации список всех школ и только свои компании (стр. 21/22 макапа)
    scuole = Scuola.objects.all().order_by('nome')
    aziende = Azienda.objects.filter(ente__user=request.user)
    return render(request, 'portal/ente_visibili.html', {'scuole': scuole, 'aziende': aziende})


# ==========================================
# --- ВЬЮХИ ДЛЯ РОЛИ: SCUOLA (ШКОЛА) ---
# ==========================================

@login_required
@role_required('SCUOLA')
def scuola_scheda_scuola(request):
    """Страница 15: Ввод и модификация основных данных школы"""
    scuola, _ = Scuola.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ScuolaForm(request.POST, instance=scuola)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Scheda SCUOLA salvata.')
            return redirect('scuola_hub')
    else:
        form = ScuolaForm(instance=scuola)
        
    return render(request, 'portal/scuola_scheda_scuola.html', {'form': form, 'scuola': scuola})


@login_required
@role_required('SCUOLA')
def scuola_situazione_studenti(request):
    """Страница 16: Новая страница распределения студентов по годам и FSL"""
    scuola, _ = Scuola.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = SituazioneStudentiForm(request.POST, instance=scuola)
        if form.is_valid():
            form.save()
            messages.success(request, 'Situazione studenti aggiornata con successo.')
            return redirect('scuola_hub')
    else:
        form = SituazioneStudentiForm(instance=scuola)

    return render(request, 'portal/scuola_situazione_studenti.html', {'form': form, 'scuola': scuola})


@login_required
@role_required('SCUOLA')
def scuola_istruzioni(request):
    """Страница 19: Инструкции для школы"""
    return render(request, 'portal/scuola_istruzioni.html')


# ==========================================
# --- ВЬЮХИ ДЛЯ РОЛИ: ENTE (ОРГАНИЗАЦИЯ) ---
# ==========================================

@login_required
@role_required('ENTE')
def ente_dati(request):
    """Страница 23: Редактирование профиля организации"""
    ente, _ = Ente.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EnteForm(request.POST, instance=ente)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Dati ente aggiornati.')
            return redirect('ente_hub')
    else:
        form = EnteForm(instance=ente)

    return render(request, 'portal/ente_dati.html', {'form': form})


@login_required
@role_required('ENTE')
def ente_aziende_list(request):
    """Страница 24: Список компаний, привязанных к текущему Ente"""
    ente = get_object_or_404(Ente, user=request.user)
    aziende = Azienda.objects.filter(ente=ente).order_by('nome')
    return render(request, 'portal/ente_aziende_list.html', {'aziende': aziende})


@login_required
@role_required('ENTE')
def ente_azienda_create(request):
    """Страница 25: Создание новой карточки компании"""
    ente = get_object_or_404(Ente, user=request.user)
    if request.method == 'POST':
        form = AziendaForm(request.POST)
        if form.is_valid():
            az = form.save(commit=False)
            az.ente = ente
            az.save()
            messages.success(request, 'Azienda creata.')
            return redirect('ente_aziende_list')
    else:
        form = AziendaForm()
    return render(request, 'portal/ente_azienda_form.html', {'form': form, 'mode': 'create'})


@login_required
@role_required('ENTE')
def ente_azienda_update(request, pk):
    """Страница 31: Редактирование карточки компании"""
    ente = get_object_or_404(Ente, user=request.user)
    azienda = get_object_or_404(Azienda, pk=pk, ente=ente)
    if request.method == 'POST':
        form = AziendaForm(request.POST, instance=azienda)
        if form.is_valid():
            form.save()
            messages.success(request, "Scheda AZIENDA aggiornata.")
            return redirect('ente_aziende_list')
    else:
        form = AziendaForm(instance=azienda)
    return render(request, 'portal/ente_azienda_form.html', {'form': form, 'mode': 'update'})


@login_required
@role_required('ENTE')
def ente_azienda_delete(request, pk):
    """Страница 32: Подтверждение и удаление компании"""
    ente = get_object_or_404(Ente, user=request.user)
    azienda = get_object_or_404(Azienda, pk=pk, ente=ente)
    if request.method == 'POST':
        azienda.delete()
        messages.success(request, "Scheda AZIENDA eliminata.")
        return redirect('ente_aziende_list')
    return render(request, 'portal/ente_azienda_confirm_delete.html', {'azienda': azienda})


@login_required
def ente_detail(request, pk):
    """Страница 18: Просмотр карточки Ente (доступно и Школе, и Ente)"""
    ente = get_object_or_404(Ente, pk=pk)
    return render(request, 'portal/ente_detail.html', {'ente': ente})


@login_required
def azienda_detail(request, pk):
    """Страница 30: Детальный просмотр компании"""
    azienda = get_object_or_404(Azienda, pk=pk)
    return render(request, 'portal/azienda_detail.html', {'azienda': azienda})


@login_required
def scuola_detail(request, pk):
    """Страницы 28 и 29: Детальный просмотр школы организацией ENTE (Read-Only)"""
    scuola = get_object_or_404(Scuola, pk=pk)
    return render(request, 'portal/scuola_detail.html', {'scuola': scuola})


@login_required
@role_required('ENTE')
def ente_istruzioni(request):
    """Страница 26: Инструкции для Ente"""
    return render(request, 'portal/ente_istruzioni.html')

@login_required
@role_required('ENTE')
def ente_scheda_azienda(request):
    if request.method == 'POST':
        form = AziendaForm(request.POST)
        if form.is_valid():
            azienda = form.save(commit=False)
            azienda.ente = request.user.ente_profile  
            azienda.save()
            messages.success(request, 'Scheda AZIENDA salvata.')
            return redirect('ente_hub')
    else:
        form = AziendaForm()
    return render(request, 'portal/ente_scheda_azienda.html', {'form': form})