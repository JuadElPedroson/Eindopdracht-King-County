# Data

- `raw/` de originele bestanden. Niet aanpassen. Niet op GitHub (te groot), maar wel in de zip die ik heb ingeleverd.
- `processed/` schone, kleine bestanden. Die mogen wel mee naar GitHub, zodat het dashboard draait.

## Wat moet in raw/ staan?
- `kc_house_data.csv`: download van https://www.kaggle.com/datasets/harlfoxem/housesalesprediction (gratis Kaggle-account nodig, knop Download, uitpakken).
- `water_osm.json` en `groen_osm.json`: worden automatisch gemaakt door `python -m src.bouw_data`. Dat haalt water en parken op bij OpenStreetMap. Gaat het mis (te druk of time-out), wacht dan even en draai het opnieuw.

## Wat komt er in processed/?
- `huizen_met_afstand.csv`: de huizen, schoongemaakt, met afstand tot water, groen en centrum en prijs per m2. Dit maakt `python -m src.bouw_data`.
