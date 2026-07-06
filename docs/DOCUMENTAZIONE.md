# Documentazione Progetto ASSO 3 Final (Full)

## Panoramica
Il progetto **ASSO 3 — FINAL (full)** è un'applicazione web sviluppata con il framework **Django** (Python).  
L'obiettivo principale del portale è la gestione dei **PCTO** (Percorsi per le Competenze Trasversali e per l'Orientamento), facilitando l'interazione tra le **Scuole** (e i loro studenti) e gli **Enti** (agenzie o aziende ospitanti).

## Architettura Tecnica
*   **Framework**: Django 4.2.13
*   **Linguaggio**: Python 3.11+
*   **Database**: SQLite (configurazione di default)
*   **Frontend**: Django Template Language (HTML/CSS)

## Struttura del Progetto
Il progetto è organizzato in "Apps" Django:
1.  **`asso3`**: Cartella di configurazione principale (settings, urls, wsgi).
2.  **`accounts`**: Gestione autenticazione utenti e ruoli (Login, Logout, Modello Utente personalizzato).
3.  **`portal`**: Core del sistema. Contiene la logica di business per Scuole ed Enti, i modelli dei dati e le view.

## Attori e Ruoli
Il sistema prevede diversi tipi di utenti, distinti dal campo `role` nel modello Utente:

### 1. Amministratore (Admin)
*   Accesso completo al pannello di amministrazione Django (`/admin`).
*   Gestione utenti, permessi e dati globali.

### 2. Scuola (Role: `SCUOLA`)
Rappresenta un istituto scolastico.
*   **Dashboard**: `scuola_hub`
*   **Funzionalità**:
    *   Gestione scheda anagrafica della Scuola.
    *   **Gestione Studenti**: Inserimento, modifica ed eliminazione delle schede studenti.
    *   **Consultazione**: Visualizzazione dell'elenco degli Enti disponibili.

### 3. Ente (Role: `ENTE`)
Rappresenta un ente partner o un'agenzia che fa da tramite per le aziende.
*   **Dashboard**: `ente_hub`
*   **Funzionalità**:
    *   Gestione scheda anagrafica dell'Ente.
    *   **Gestione Aziende**: L'Ente può creare e gestire molteplici "Aziende" collegate al proprio profilo (CRUD completo).
    *   **Consultazione**: Visualizzazione dell'elenco delle Scuole.

## Modelli Dati (Database)
I principali modelli definiti in `portal/models.py` e `accounts/models.py` sono:

*   **User (`accounts.User`)**: Estende l'utente base di Django aggiungendo il campo `role` (SCUOLA o ENTE).
*   **Ente (`portal.Ente`)**: Collegato 1-a-1 con un `User` (ruolo ENTE). Contiene contatti e servizi extra.
*   **Azienda (`portal.Azienda`)**: Collegata a un `Ente` (Relazione 1-a-Molti). Rappresenta la singola azienda ospitante gestita dall'Ente.
*   **Scuola (`portal.Scuola`)**: Contiene codice meccanografico e dati statistici (num. studenti, PCTO da attivare).
*   **Studente (`portal.Studente`)**: Collegato a una `Scuola` (Relazione 1-a-Molti). Contiene dati anagrafici dello studente.

## Funzionalità e Flussi
*   **Area Pubblica**:
    *   Landing page, Chi Siamo, Scopo, FAQ.
    *   Liste pubbliche di Scuole e Aziende (in sola lettura).
*   **Autenticazione**:
    *   Login/Logout gestiti dall'app `accounts`.
    *   Accesso alle aree riservate protetto da decoratori `@login_required` e `@role_required`.

## Istruzioni di Avvio (da README)
1.  Creazione ambiente virtuale: `py -3.11 -m venv .venv`
2.  Attivazione: `.\.venv\Scripts\Activate.ps1`
3.  Installazione dipendenze: `pip install -r requirements.txt`
4.  Migrazione DB: `python manage.py migrate`
5.  (Opzionale) Seed dati demo: `python manage.py seed`
6.  Avvio server: `python manage.py runserver 8003`

**URL Principale**: `http://127.0.0.1:8003/`

## Note
*   Il codice contiene commenti che descrivono le recenti modifiche alle relazioni dei modelli (es. collegamento `Ente -> User`).
*   La logica di filtraggio degli studenti per scuola è predisposta ma parzialmente da implementare/restringere nelle view (vedi `TODO` nel codice).
