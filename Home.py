# Startpagina: de vraag en het antwoord. Starten met: streamlit run Home.py
import streamlit as st

from src import analyse, dashboard_data

st.set_page_config(page_title="Wat is uitzicht waard?", layout="wide")

premies, r2, aantal_huizen = dashboard_data.bereken_premies()
premies_zonder_waterfront, _, _ = dashboard_data.bereken_premies(waterfront_meenemen=False)

water = premies[premies["laag"] == "water"]
groen = premies[premies["laag"] == "groen"]
water_dichtbij = water.iloc[0]
water_dichtbij_zonder_waterfront = premies_zonder_waterfront.query("laag == 'water'").iloc[0]
verste_groep_water = analyse.waar_premie_stopt(water)
verste_groep_groen = analyse.waar_premie_stopt(groen)

st.title("Wat is uitzicht waard?")
st.write(
    "King County (Seattle): hoeveel extra betaal je per m2 voor een huis dichter bij water of groen, "
    "en vanaf welke afstand is dat weg?"
)

kolom_water, kolom_stopt, kolom_groen = st.columns(3)
kolom_water.metric(
    "Water, binnen 250 m",
    f"+{water_dichtbij['premie_procent']:.0f}%",
    f"marge {water_dichtbij['ondergrens']:.0f}% tot {water_dichtbij['bovengrens']:.0f}%",
    delta_color="off",
)
kolom_stopt.metric("Water: verste groep met premie", verste_groep_water)
kolom_groen.metric("Groen (parken)", "geen premie" if verste_groep_groen is None else verste_groep_groen)

st.header("Antwoord")
st.write(
    f"**Water.** Huizen binnen 250 m van water zijn {water_dichtbij['premie_procent']:.0f}% duurder per m2 "
    f"dan vergelijkbare huizen verder dan 2 km. Dat is ongeveer {water_dichtbij['premie_dollar']:.0f} dollar per m2. "
    f"Bij 250 tot 500 m is dat nog {water.iloc[1]['premie_procent']:.0f}%, bij 500 m tot 1 km {water.iloc[2]['premie_procent']:.0f}%. "
    "Verder dan 1 km is er geen verschil meer met huizen ver weg."
)
st.write(
    "**Groen.** Voor parken vind ik geen premie. Zonder controles lijkt dat wel zo, maar als ik "
    "rekening houden met grootte, kwaliteit en buurt blijft er niets over."
)
st.write(
    f"**Alleen de afstand.** De data heeft zelf een kolom voor huizen aan het water. Laat ik die huizen weg, "
    f"dan is de premie binnen 250 m nog steeds {water_dichtbij_zonder_waterfront['premie_procent']:.0f}%. "
    "Het effect zit dus niet alleen in die ene kolom."
)

st.header("Advies")
st.write(
    f"Tel bij een huis met water binnen 250 m ongeveer {water_dichtbij['premie_procent']:.0f}% bij de prijs per m2, "
    f"bij 250 tot 500 m ongeveer {water.iloc[1]['premie_procent']:.0f}%, en daarboven niet meer dan "
    f"{water.iloc[2]['premie_procent']:.0f}%. Voor groen tel je niets bij."
)
st.caption(f"Gebaseerd op {aantal_huizen} verkopen. De regressie verklaart {r2 * 100:.0f}% van de verschillen in prijs per m2.")
