# Data

- `raw/` de originele bestanden. Niet aanpassen en niet op GitHub (te groot).
- `processed/` schone, kleine bestanden. Die mogen wel mee naar GitHub, zodat het dashboard draait.

## Wat moet in raw/ staan?
- `kc_house_data.csv`: download van https://www.kaggle.com/datasets/harlfoxem/housesalesprediction (gratis Kaggle-account nodig, knop Download, uitpakken).
- `water_osm.json`: wordt automatisch gemaakt door `python -m src.bouw_data`. Dat haalt het water op bij OpenStreetMap. Gaat het mis (te druk of time-out), wacht dan even en draai het opnieuw.

## Wat komt er in processed/?
- `huizen_met_afstand.csv`: de huizen, schoongemaakt, met afstand tot water en prijs per m2. Dit maakt `python -m src.bouw_data`.
