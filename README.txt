ASSO 3 — FINAL (full)
=====================
Windows / PowerShell
--------------------
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py runserver 8003
python manage.py makemigrations
python manage.py migrate
python manage.py seed
http://127.0.0.1:8003/

URL
---
http://127.0.0.1:8003/
http://127.0.0.1:8003/accounts/login/
http://127.0.0.1:8003/accounts/auth/choose/

DEMO USERS
----------
admin / *****
scuola_user / ********  (SCUOLA)
ente_user / ********     (ENTE)
Passwords are provided separatel
