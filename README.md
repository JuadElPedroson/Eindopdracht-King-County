# Eindopdracht King County
Huizenprijzen en leefomgeving: wat is uitzicht (water en groen) waard? Case 6, minor Data Science.

## Links
- Dashboard: (vul in na het publiceren)
- GitHub: https://github.com/JuadElPedroson/Eindopdracht-King-County

## Vraag
Hoeveel extra betaal je per vierkante meter voor een huis dichter bij water of groen, en vanaf welke afstand is dat effect weg?

## Antwoord
(vul in na de analyse)

## Data
- Huizen: House Sales in King County, USA (Kaggle, 21.613 verkopen van mei 2014 tot mei 2015). https://www.kaggle.com/datasets/harlfoxem/housesalesprediction
- Water en groen: OpenStreetMap (meren, rivieren, kustlijn en parken), opgehaald via de Overpass API op 30 oktober 2026. (c) OpenStreetMap contributors.

## Opschonen
Huizen: van 21.613 naar 21.419 verkopen.
- 1 woning met 33 slaapkamers (typefout) weggehaald
- 16 woningen zonder slaapkamer of badkamer weggehaald (fouten in de data)
- 177 huizen waren twee keer verkocht, van die huizen houden we de laatste verkoop

Water en groen (OpenStreetMap): eerst filteren, dan rekenen.
- Water: 246.467 punten in 6.472 objecten. Na het weghalen van lege punten, dubbele punten, punten buiten het gebied en kleine objecten (vijvers, zwembaden) blijven 133.435 punten in 1.100 objecten over.
- Groen: 70.761 punten in 3.302 objecten, na filteren 48.162 punten in 1.480 objecten (kleine speeltuintjes weg).
- Per huis rekenen we de afstand tot het dichtstbijzijnde punt uit, in meters.

## Mappen
- `data/raw/` originele bestanden (blijft lokaal, staat niet op GitHub)
- `data/processed/` schoon eindbestand en een lijst van wat er is opgeschoond
- `notebooks/` verkennen en uitproberen
- `src/` de code: laden, opschonen, geo, analyse, grafieken
- `pages/` pagina's van het dashboard
- `Home.py` startpagina van het dashboard

## Starten
Het dashboard werkt direct met `data/processed/huizen_met_afstand.csv`, de data hoeft niet opnieuw opgehaald te worden.

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

Alles opnieuw maken (niet nodig om het dashboard te draaien): download `kc_house_data.csv` van Kaggle, zet het in `data/raw/` en draai `python -m src.bouw_data`. Water en groen worden dan opnieuw opgehaald (een paar minuten).
