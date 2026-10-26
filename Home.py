# Startpagina van het dashboard. Starten met: streamlit run Home.py
import streamlit as st

st.set_page_config(page_title="Titel van de case", layout="wide")

st.title("Titel van de case")
st.write("Hoofdvraag en kort antwoord komen hier.")

# voorbeeld voor later:
# from src.laden import laad_ruw
# from src.schoon import maak_schoon
# df = maak_schoon(laad_ruw())
