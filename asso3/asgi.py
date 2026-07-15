import os
from django.core.asgi import get_asgi_application

# Imposta il modulo delle impostazioni predefinito di Django per il progetto "asso3"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asso3.settings')

# Inizializza l'applicazione ASGI di Django per gestire le richieste asincrone
application = get_asgi_application()
