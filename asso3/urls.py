from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Панель администратора
    path('admin/', admin.site.urls),
    
    # Подключаем маршруты наших приложений
    path('', include('portal.urls')),
    path('accounts/', include('accounts.urls')),
    
    # Системный редирект после успешного входа
    path('post-login', lambda request: redirect('/accounts/post-login', permanent=False)),
]