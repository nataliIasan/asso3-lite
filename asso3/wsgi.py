import os
from django.core.wsgi import get_wsgi_application

# Imposta il modulo delle impostazioni predefinito di Django per il progetto "asso3"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asso3.settings')

# Inizializza l'applicazione WSGI di Django per il server web
application = get_wsgi_application()
