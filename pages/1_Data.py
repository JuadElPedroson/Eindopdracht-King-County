# Welke data ik gebruik, hoe ik die koppel en wat er is opgeschoond.
import streamlit as st

from src import dashboard_data

st.set_page_config(page_title="Data", layout="wide")

opschoonlog = dashboard_data.laad_opschoonlog()


def haal_aantal(onderdeel, stap):
    regel = opschoonlog[(opschoonlog["onderdeel"] == onderdeel) & (opschoonlog["stap"] == stap)]
    return met_punt(int(regel["aantal"].iloc[0]))


def met_punt(getal):
    return f"{getal:,}".replace(",", ".")


st.title("Data en opschonen")

st.header("Bronnen")
st.markdown(
    f"""
- **Huizen:** [Kaggle, House Sales in King County](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction). {haal_aantal("huizen", "begin")} verkopen van mei 2014 tot mei 2015, met prijs, oppervlak, kwaliteit en locatie.
- **Water:** [OpenStreetMap](https://www.openstreetmap.org), zelf opgehaald met de [Overpass API](https://overpass-api.de). Meren, rivieren en kustlijn.
- **Groen:** [OpenStreetMap](https://www.openstreetmap.org), zelf opgehaald met de [Overpass API](https://overpass-api.de). Parken.
"""
)

st.caption("Kaartdata: (c) OpenStreetMap contributors. Achtergrondkaart: (c) CARTO.")

st.header("Hoe koppel ik ze?")
st.write(
    "De bronnen hebben geen gemeenschappelijke kolom, dus koppel ik op locatie. "
    "Voor elk huis zoek ik het dichtstbijzijnde stukje water en het dichtstbijzijnde park en reken ik de afstand uit in meters. "
    "Zo krijgt elk huis de nieuwe kolommen afstand_water en afstand_groen. "
    "Daarnaast maak ik de prijs per m2, de afstandsgroepen en de afstand tot het centrum van Seattle."
)

st.header("Hoe schoon ik op?")
dubbel = haal_aantal("huizen", "weg: zelfde huis vaker verkocht (oudste verkoop weg)")
leeg = haal_aantal("huizen", "weg: geen slaapkamer of badkamer")
typefout = haal_aantal("huizen", "weg: meer dan 15 slaapkamers (typefout)")
st.markdown(
    f"""
- **Huizen:** van {haal_aantal("huizen", "begin")} naar {haal_aantal("huizen", "over")} verkopen. Weg zijn {dubbel} oudere verkopen van hetzelfde huis (ik hou de laatste), {leeg} huizen zonder slaapkamer of badkamer en {typefout} huis met 33 slaapkamers (typefout).
- **Water:** van {haal_aantal("water", "objecten_ruw")} naar {haal_aantal("water", "objecten_na")} objecten. Alles ver buiten het gebied van de huizen is weg, net als lege en dubbele punten en kleine objecten (onder 200 m, zoals vijvers en zwembaden). De kustlijn blijft altijd staan.
- **Groen:** van {haal_aantal("groen", "objecten_ruw")} naar {haal_aantal("groen", "objecten_na")} objecten, op dezelfde manier. Hier gaan objecten onder 100 m eruit. Bos heb ik niet opgehaald: dat zijn enorme vlakken waardoor bijna elk huis in het oosten bij bos ligt.
"""
)
st.write(
    "Ik filter eerst en reken daarna. Anders rekent de computer met honderdduizenden punten "
    "en meet je de afstand tot een vijver in een tuin."
)
st.caption("De volledige uitleg staat in DATA_VERANTWOORDING.md.")
