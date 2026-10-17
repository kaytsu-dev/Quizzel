# Quizzel

Quiz locale in italiano sulle capitali europee. All’avvio scegli tra un quiz di 10 domande a scelta multipla, 10 domande aperte oppure un quiz misto con 5 domande per tipo. Le domande vengono mescolate a ogni tentativo e ogni risposta corretta vale 10 punti. I risultati vengono aggiunti a `punteggi/punteggi.csv`.

Ogni tentativo viene inoltre aggiunto al file `punteggi/<username>.txt`, con le risposte fornite e, in caso di errore, la risposta corretta. Per consultare i riepiloghi in un semplice elenco interattivo nel terminale, esegui `python visualizza_risposte.py`.

## Requisiti

Python 3.9 o successivo.

## Installazione e avvio

Apri un terminale nella cartella del progetto e lancia:

```bash
python -m venv .venv
```

Attiva l’ambiente virtuale:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Installa Flask e avvia l’app:

```bash
pip install -r requirements.txt
python app.py
```

Poi apri **http://127.0.0.1:5000** nel browser. Per terminare il server, premi `Ctrl+C` nel terminale. Il file CSV viene creato automaticamente al primo invio del quiz e i tentativi successivi vengono accodati.

Domande e risposte corrette sono contenute nel codice, quindi il quiz non richiede Internet per funzionare. Le capitali sono state verificate con la [mappa geografica Eurostat](https://ec.europa.eu/eurostat/documents/15216629/15559935/KS-FK-22-001-EN-N.pdf/1cb9d295-6868-70e3-0319-4725040cfdb8?download=true&t=1670407603869) e la pubblicazione ufficiale UE [Let’s explore Europe](https://op.europa.eu/webpub/com/lets-explore-europe/en/).
