from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.urls import reverse
# правильные импорты форм
from .forms import RoleLoginForm, ScuolaFullSignupForm, EnteFullSignupForm
from .models import ActivationToken, User
from django.core.signing import TimestampSigner
signer = TimestampSigner()


class RoleLoginView(LoginView):
    template_name='accounts/login.html'
    def get_success_url(self): return '/post-login'

class RoleLogoutView(LogoutView):
    next_page='/'

from django.shortcuts import redirect

def post_login(request):
    # Если пользователь не вошёл — на страницу логина
    if not request.user.is_authenticated:
        return redirect('login')

    # Проверяем, есть ли параметр "next" (например, при входе на защищённую страницу)
    next_page = request.GET.get('next')
    if next_page:
        return redirect(next_page)

    # Проверяем роль пользователя
    if request.user.role == 'SCUOLA':
        return redirect('scuola_hub')
    elif request.user.role == 'ENTE':
        return redirect('ente_hub')

    # Если просто зашли повторно на post-login — возвращаем на landing
    if request.path.endswith('/post-login'):
        return redirect('landing')

    # На случай отсутствия роли или ошибок
    return redirect('landing')




def login_options(request):
    # Если пользователь уже вошёл, отправляем его сразу на нужную страницу
    if request.user.is_authenticated:
        if request.user.role == 'SCUOLA':
            return redirect('scuola_hub')
        elif request.user.role == 'ENTE':
            return redirect('ente_hub')
        else:
            return redirect('landing')
    # Если не вошёл — показать выбор роли
    return render(request, 'portal/login_options.html')



    signer = TimestampSigner()  # токен со временем

def signup_scuola_full(request):
    if request.method == 'POST':
        form = ScuolaFullSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # создаём токен
            raw = signer.sign(user.pk)  # подпишем ID пользователя
            token = ActivationToken.objects.create(user=user, token=raw)

            # DEMO: показываем ссылку на экране
            activation_url = f"/accounts/activate/{token.token}/"
            messages.info(request, "Demo: copia il link di attivazione qui sotto.")

            return render(request, 'accounts/signup_done_demo.html', {
                'activation_url': activation_url
            })
    else:
        form = ScuolaFullSignupForm()

    return render(request, 'accounts/signup_scuola_full.html', {'form': form})


from django.contrib.auth import login

def activate(request, token):
    rec = get_object_or_404(ActivationToken, token=token, used=False)
    try:
        user_pk = signer.unsign(token, max_age=604800)
    except SignatureExpired:
        messages.error(request, "Link di attivazione scaduto.")
        return redirect('/accounts/login/')
    except BadSignature:
        messages.error(request, "Link di attivazione non valido.")
        return redirect('/accounts/login/')

    if int(user_pk) != rec.user_id:
        messages.error(request, "Link non valido.")
        return redirect('/accounts/login/')

    user = rec.user
    user.is_active = True
    user.save()
    rec.used = True
    rec.save()

    login(request, user)
    messages.success(request, "Account attivato con successo.")

    if getattr(user, 'role', '') == 'SCUOLA':
        target = 'scuola_hub'
    elif getattr(user, 'role', '') == 'ENTE':
        target = 'ente_dati'
    else:
        target = 'dashboard'   # fallback, если роль неизвестна

    return redirect(target)


def signup_ente_full(request):
    if request.method == "POST":
        form = EnteFullSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # генерим «демо»-ссылку активации
            raw = signer.sign(user.pk)
            token = ActivationToken.objects.create(user=user, token=raw)

            # генерируем ссылку активации
            activation_url = f"/accounts/activate/{token.token}/"

            # показываем пользователю кликабельный линк
            return render(
                request,
                "accounts/signup_done_demo.html",
                {"activation_url": activation_url}
            )
    else:
        form = EnteFullSignupForm()

    return render(request, "accounts/signup_ente_full.html", {"form": form})