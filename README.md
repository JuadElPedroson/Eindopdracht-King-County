# DS_test
even als oefening

## Vraag
Case 6, King County (richting A): hoeveel extra betaal je per vierkante meter voor een huis dichter bij water, en vanaf welke afstand is dat effect weg?

## Data
- Huizen: House Sales in King County, USA (Kaggle, 21.613 verkopen). https://www.kaggle.com/datasets/harlfoxem/housesalesprediction
- Water: OpenStreetMap, meren, rivieren en kustlijn, opgehaald via de Overpass API. Datum van ophalen: vul in.

## Mappen
- `data/raw/` originele bestanden, nooit aanpassen en blijft lokaal (staat niet op GitHub)
- `data/processed/` schone, kleine bestanden die het dashboard nodig heeft
- `notebooks/` verkennen en uitproberen
- `src/` de code die we hergebruiken: laden, opschonen, geo, analyse, grafieken
- `pages/` pagina's van het dashboard (alleen als het een Streamlit dashboard wordt)
- `Home.py` startpagina van het dashboard

## Starten
Mac:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Windows (PowerShell):

    py -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

Daarna, vanuit de hoofdmap:

1. Download `kc_house_data.csv` van Kaggle en zet het in `data/raw/`.
2. Draai `python -m src.bouw_data`. Dat schoont de huizen op, haalt het water op (een paar minuten, alleen de eerste keer), rekent de afstand per huis uit en schrijft `data/processed/huizen_met_afstand.csv`.
3. Open `notebooks/01_verkennen.ipynb` of start het dashboard met `streamlit run Home.py`.
