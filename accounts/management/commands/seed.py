from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from portal.models import Scuola, Ente, Studente, Azienda

class Command(BaseCommand):
    help='Create demo users and minimal demo data'
    def handle(self,*a,**kw):
        U=get_user_model()
        if not U.objects.filter(username='admin').exists():
            U.objects.create_superuser('admin','admin@example.com','admin123')
            self.stdout.write('admin/admin123')
        scu,created = U.objects.get_or_create(username='scuola_user', defaults={'role':'SCUOLA'})
        if created: scu.set_password('pass12345'); scu.save()
        ent,created = U.objects.get_or_create(username='ente_user', defaults={'role':'ENTE'})
        if created: ent.set_password('pass12345'); ent.save()
        self.stdout.write('scuola_user/pass12345')
        self.stdout.write('ente_user/pass12345')
        # demo domain data
        s,_=Scuola.objects.get_or_create(nome='Liceo Newton', defaults={'indirizzo':'Via Roma 1'})
        e,_=Ente.objects.get_or_create(nome='Associazione Asso', defaults={'contatti':'info@asso.it'})
        Studente.objects.get_or_create(scuola=s, cognome='Rossi', nome='Luca')
        Azienda.objects.get_or_create(ente=e, nome='Tech Srl', settore='IT')
        self.stdout.write(self.style.SUCCESS('Demo data created'))
