# RELAZIONE TECNICA: Piattaforma ASSO
## Alternanza Scolastica e Sportello d'Orientamento (Versione 3)

> **Nota:** Questo documento definisce l'architettura delle informazioni, i flussi utente e i modelli dati della piattaforma digitale ASSO.

---

## 1. Introduzione e Obiettivi del Sistema
La piattaforma **ASSO** nasce con l'obiettivo di semplificare, digitalizzare e monitorare la collaborazione tra gli **Istituti Scolastici** (Scuole) e gli **Enti coordinatori** (Enti), facilitando l'attivazione dei percorsi formativi (**FSL / PCTO**) per gli studenti con certificazione.

---

## 2. Architettura dei Ruoli Utente
Il sistema prevede tre livelli di accesso, ciascuno con permessi e visibilità differenti:

| Ruolo | Permessi e Funzionalità Principali |
| :--- | :--- |
| **Ospite (Guest / Public)** | Navigazione sulla Landing Page, consultazione delle FAQ e visualizzazione degli elenchi pubblici delle Scuole e delle Aziende partner. |
| **Scuola (Istituto)** | Gestione della scheda anagrafica della scuola, inserimento della situazione degli studenti certificati (suddivisi per anno), monitoraggio degli FSL attivati e consultazione dell'elenco degli Enti disponibili. |
| **Ente (Organizzazione)** | Gestione del proprio profilo e del budget delle doti, gestione completa (inserimento, modifica, eliminazione, archiviazione anno) delle Aziende partner collegate, consultazione delle schede delle Scuole. |

---

## 3. Specifica dei Modelli Dati (Database Schema)
In base ai form e ai template del portale, la base dati è strutturata su tre entità principali:

### Modello: Scuola (Profilo Istituto)
* **Nome Scuola** (Testo)
* **Codice Meccanografico** (Testo, Unico)
* **Email** (Email)
* **Telefono** (Testo)
* **Indirizzo** (Testo)
* **Studenti 5° anno** (Numero)
* **Studenti 4° anno** (Numero)
* **Studenti Triennio** (Numero)
* *Campi calcolati:*
    * **Studenti certificati totali** (Somma degli studenti del 3°, 4° e 5° anno)
    * **FSL da attivare** (Obiettivo dell'Anno Scolastico)
    * **FSL attivati** (Tirocini effettivamente avviati)
    * **FSL ancora da attivare** (Differenza tra obiettivo e attivati)

### Modello: Ente (Profilo Ente)
* **Nome Ente** (Testo)
* **Codice Fiscale** (Testo, Unico)
* **Telefono** (Testo)
* **Email** (Email)
* **Doti disponibili** (Numero / Budget)
* **Servizi Extra** (Area di testo per consulenza, formazione, ecc.)

### Modello: Azienda (Collegata all'Ente)
* **Nome Azienda** (Testo)
* **Referente e Contatti** (Testo)
* **Settore Operativo** (Testo)
* **FSL attivati nell'anno in corso** (Numero)
* **FSL totali storici** (Numero, sola lettura)
* **Note / Osservazioni** (Area di testo)

---

## 4. Mappa delle Schermate e Flussi di Navigazione (Sitemap)

### Area Pubblica (Accesso Libero)
* **Landing Page (`landing.html`):** Presentazione del progetto, sezione "Chi siamo", link rapidi ai servizi.
* **FAQ (`faq.html`):** Fisarmonica interattiva per le risposte alle domande frequenti.
* **Scuole Pubbliche (`scuole_public.html`):** Lista delle scuole registrate con indirizzo (senza dati sensibili degli studenti).
* **Aziende Pubbliche (`aziende_public.html`):** Lista delle aziende partner sul territorio.
* **Login Options (`login_options.html`):** Pagina di reindirizzamento per l'accesso o la registrazione mirata (Scuola o Ente).

### Area Riservata: Scuola
* **Hub Scuola (`scuola_hub.html`):** Pannello di controllo principale.
* **Scheda Scuola (`scuola_scheda_scuola_detail.html` / `_form.html`):** Visualizzazione e modifica dei dati di contatto dell'istituto.
* **Situazione Studenti (`scuola_situazione_studenti.html`):** Form di aggiornamento dei dati relativi alle certificazioni e agli FSL attivati.
* **Visualizza Enti (`scuola_visibili.html`):** Elenco degli Enti partner con link ai dettagli dei contatti e delle doti disponibili (`ente_detail.html`).

### Area Riservata: Ente
* **Hub Ente (`ente_hub.html`):** Pannello di controllo principale.
* **Scheda Ente (`ente_dati_detail.html` / `_form.html`):** Gestione del profilo dell'Ente e delle doti finanziarie.
* **Le mie aziende (`ente_aziende_list.html`):** Tabella interattiva per la gestione delle aziende collegate, con modale dinamica per l'eliminazione rapida.
* **Azienda Form (`azienda_form.html`):** Creazione e modifica dell'azienda, con la funzionalità speciale di **Chiusura Anno** (Modale di conferma per azzerare i tirocini correnti e sommarli allo storico totale).
* **Visualizza Scuole (`ente_visibili.html`):** Elenco delle scuole registrate per monitorare le loro necessità.