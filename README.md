# Eindopdracht King County
Huizenprijzen en leefomgeving: wat is uitzicht (water en groen) waard? Case 6, minor Data Science.

## Links
- Dashboard: draait lokaal, zie Starten hieronder
- GitHub: https://github.com/JuadElPedroson/Eindopdracht-King-County

## Vraag
Hoeveel extra betaal je per vierkante meter voor een huis dichter bij water of groen, en vanaf welke afstand is dat effect weg?

## Antwoord
- Water: huizen binnen 250 m van water zijn ongeveer 19% duurder per m2 (marge 17% tot 20%) dan vergelijkbare huizen verder dan 2 km. De premie loopt terug tot bijna 0 bij 1 km.
- Groen (parken): na controles geen aantoonbare premie.
- Zonder de huizen die in de data al als waterfront staan is de premie binnen 250 m nog 12%.

## Data
Zie ook DATA_VERANTWOORDING.md.
- Huizen: House Sales in King County, USA (Kaggle, 21.613 verkopen van mei 2014 tot mei 2015). https://www.kaggle.com/datasets/harlfoxem/housesalesprediction
- Water en groen: OpenStreetMap (meren, rivieren, kustlijn en parken), opgehaald via de Overpass API op 30 oktober 2026. (c) OpenStreetMap contributors.

## Opschonen
Huizen: van 21.613 naar 21.419 verkopen.
- 1 woning met 33 slaapkamers (typefout) weggehaald
- 16 woningen zonder slaapkamer of badkamer weggehaald (fouten in de data)
- 177 huizen waren twee keer verkocht, van die huizen hou ik de laatste verkoop

Water en groen (OpenStreetMap): eerst filteren, dan rekenen.
- Water: 246.467 punten in 6.472 objecten. Na het weghalen van lege punten, dubbele punten, punten buiten het gebied en kleine objecten (vijvers, zwembaden) blijven 133.435 punten in 1.100 objecten over.
- Groen: 70.761 punten in 3.302 objecten, na filteren 48.162 punten in 1.480 objecten (kleine speeltuintjes weg).
- Per huis reken ik de afstand tot het dichtstbijzijnde punt uit, in meters.

## Wat zit waar (inleveren)
- Code: `Home.py`, `pages/` en `src/`
- Ophaalscript: `src/geo.py` (functie `haal_op`, haalt water en groen op met requests) en `src/bouw_data.py` (draait alle stappen)
- Databestanden: `data/raw/` (origineel, zit alleen in de zip) en `data/processed/`
- Data-verantwoording: `DATA_VERANTWOORDING.md`
- Packages: `requirements.txt`

Het dashboard leest alleen lokale bestanden en roept geen API aan.

## Mappen
- `data/raw/` originele bestanden (staat niet op GitHub, wel in de zip van Brightspace)
- `data/processed/` schoon eindbestand en een lijst van wat er is opgeschoond
- `notebooks/` verkennen en uitproberen
- `src/` de code: laden, opschonen, geo, analyse, grafieken
- `pages/` pagina's van het dashboard: Data, Kaart, Onderbouwing
- `Home.py` startpagina met de vraag en het antwoord

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
