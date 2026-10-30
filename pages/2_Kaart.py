# Kaart van alle huizen, met filters op afstand.
import streamlit as st

from src import dashboard_data, grafieken

st.set_page_config(page_title="Kaart", layout="wide")

# per keuze: kolom, titel van de legenda en kleurschaal (bij afstand is dichtbij geel)
KLEUR_KEUZES = {
    "Prijs per m2": ("prijs_per_m2", "Prijs per m2 (dollar)", "Viridis"),
    "Afstand tot water": ("afstand_water", "Afstand tot water (m)", "Viridis_r"),
    "Afstand tot groen": ("afstand_groen", "Afstand tot groen (m)", "Viridis_r"),
}

huizen = dashboard_data.laad_huizen()

st.sidebar.header("Kaart aanpassen")
kleur_keuze = st.sidebar.selectbox("Kleur op", list(KLEUR_KEUZES))
laag = st.sidebar.radio("Filter op afstand tot", ["water", "groen"])
max_afstand = st.sidebar.slider("Maximale afstand (m)", 250, 5000, 2000, step=250)
met_waterfront = st.sidebar.checkbox("Huizen aan het water (waterfront) meenemen", value=True)

zichtbaar = huizen[huizen["afstand_" + laag] <= max_afstand]
if not met_waterfront:
    zichtbaar = zichtbaar[zichtbaar["waterfront"] == 0]

st.title("Waar liggen de dure huizen?")
st.write(
    "Elke stip is een verkocht huis. Kleur op prijs per m2: de duurste huizen liggen rond Lake Washington en langs de kust. "
    "Kleur op afstand tot water: je ziet ringen rond de meren."
)

if zichtbaar.empty:
    st.warning("Geen huizen met deze keuzes. Zet de maximale afstand hoger.")
    st.stop()

kolom_aantal, kolom_prijs, kolom_afstand = st.columns(3)
kolom_aantal.metric("Huizen op de kaart", f"{len(zichtbaar):,}".replace(",", "."))
kolom_prijs.metric("Mediaan prijs per m2", f"{zichtbaar['prijs_per_m2'].median():.0f} dollar")
kolom_afstand.metric(f"Mediaan afstand tot {laag}", f"{zichtbaar['afstand_' + laag].median():.0f} m")

kolom, legenda_titel, kleurschaal = KLEUR_KEUZES[kleur_keuze]
kaart = grafieken.kaart_huizen(zichtbaar, kolom, legenda_titel, kleurschaal)
st.plotly_chart(kaart)
st.caption(
    "De kleurschaal loopt van het 5e tot het 95e percentiel, zodat een paar extreme huizen de kaart niet bepalen. "
    "Let op: ook het centrum en de buurt spelen mee in de prijs. Daarom controleer ik daarvoor op de pagina Onderbouwing."
)
