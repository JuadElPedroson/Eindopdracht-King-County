# DS_test
even als oefening

## Vraag
Schrijf hier de hoofdvraag in een zin.

## Data
Bron, link en datum waarop je het hebt gedownload (APA).

## Mappen
- `data/raw/` originele bestanden, nooit aanpassen en blijft lokaal (staat niet op GitHub)
- `data/processed/` schone, kleine bestanden die het dashboard nodig heeft
- `notebooks/` verkennen en uitproberen
- `src/` de code die we hergebruiken: laden, opschonen, analyse, grafieken
- `pages/` pagina's van het dashboard (alleen als het een Streamlit dashboard wordt)
- `Home.py` startpagina van het dashboard

## Starten
Mac:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    streamlit run Home.py

Windows (PowerShell):

    py -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    streamlit run Home.py

Zet de originele data in `data/raw/` (zie `data/README.md`).
