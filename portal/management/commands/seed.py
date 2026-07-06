from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from portal.models import Scuola, Ente, Azienda

class Command(BaseCommand):
    def handle(self,*a,**k):
        U = get_user_model()
        if not U.objects.filter(username='scuola_user').exists():
            U.objects.create_user(username='scuola_user', password='pass12345', role='SCUOLA', email='scuola@demo.it')
        if not U.objects.filter(username='ente_user').exists():
            U.objects.create_user(username='ente_user', password='pass12345', role='ENTE', email='ente@demo.it')

        s,_ = Scuola.objects.get_or_create(nome='Liceo Demo', defaults={'numero_studenti':300})
        e,_ = Ente.objects.get_or_create(nome_ente='Associazione Demo', info_contatto='demo@ente.it')
        Azienda.objects.get_or_create(ente=e, nome_azienda='Alfa S.r.l.', settore='IT', referente_contatto='Mario Rossi')
        self.stdout.write('Users: scuola_user/pass12345, ente_user/pass12345; demo dati creati.')