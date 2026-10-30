# Data en berekeningen voor het dashboard. Streamlit onthoudt de uitkomst (cache_data),
# zodat de regressie niet bij elke klik opnieuw draait.
import streamlit as st

from src import analyse, laden


@st.cache_data
def laad_huizen():
    return laden.laad_schoon()


@st.cache_data
def bereken_premies(waterfront_meenemen=True):
    huizen = laden.laad_schoon()
    if not waterfront_meenemen:
        huizen = huizen[huizen["waterfront"] == 0]
    model = analyse.draai_regressie(huizen)
    return analyse.premie_tabel(model, huizen), model.rsquared, int(model.nobs)


@st.cache_data
def laad_opschoonlog():
    return laden.laad_log()
