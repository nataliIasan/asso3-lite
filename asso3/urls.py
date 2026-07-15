from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Pannello di amministrazione Django
    path('admin/', admin.site.urls),
    
    # Rotte delle applicazioni del progetto
    path('', include('portal.urls')),
    path('accounts/', include('accounts.urls')),
    
    # Reindirizzamento di sistema dopo un login con successo
    path('post-login/', lambda request: redirect('/accounts/post-login', permanent=False)),
]