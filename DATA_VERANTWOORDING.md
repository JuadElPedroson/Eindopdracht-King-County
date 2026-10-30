# Data-verantwoording

**Huizen.** Kaggle, House Sales in King County, USA (harlfoxem/housesalesprediction). Gedownload op 30 oktober 2026 als kc_house_data.csv: 21.613 verkopen van 2 mei 2014 tot 27 mei 2015. Met de hand gedownload, want Kaggle vraagt om een login.

**Water en groen.** OpenStreetMap, opgehaald met een script (`src/geo.py`, functie `haal_op`) via de Overpass API en de bibliotheek requests, op 30 oktober 2026. Water: natural=water en natural=coastline. Groen: leisure=park. Het zoekvak is het gebied om de huizen heen. De bestanden staan in data/raw/ en het dashboard roept de API niet aan.

**Samenvoegen.** Er is geen gedeelde sleutel. Per huis zoek ik het dichtstbijzijnde punt van het water en van het groen en reken de afstand uit in meters (cKDTree). Alle 21.419 schone huizen houden een afstand, dus er vallen geen rijen af bij het samenvoegen. Het eindbestand is data/processed/huizen_met_afstand.csv (21.419 rijen, 30 kolommen).

**Wat er misging.**
- Huizen: 194 verwijderd. 1 woning met 33 slaapkamers, 16 zonder slaapkamer of badkamer, en 177 keer een huis dat twee keer is verkocht (ik hou de laatste verkoop).
- Water: 246.467 punten in 6.472 objecten, na filteren 133.435 punten in 1.100 objecten. Lege, dubbele en kleine objecten (vijvers, zwembaden) zijn weggehaald.
- Groen: 70.761 punten in 3.302 objecten, na filteren 48.162 punten in 1.480 objecten. Bos is niet opgehaald: dat zijn enorme vlakken waardoor bijna elk huis in het oosten bij bos ligt.
- Afstandsgroepen verder dan 2 km zijn samengevoegd, want bij water zat er 1 huis boven 5 km.
- Afstanden zijn een vlakke benadering en gaan tot het dichtstbijzijnde punt op de rand van het water of park. Dat is een aanname.
