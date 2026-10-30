# De statistiek achter het antwoord: eerst zonder controles, dan met.
import pandas as pd
import streamlit as st

from src import analyse, dashboard_data, grafieken

st.set_page_config(page_title="Onderbouwing", layout="wide")

huizen = dashboard_data.laad_huizen()
premies, r2, aantal_huizen = dashboard_data.bereken_premies()
premies_zonder_waterfront, _, aantal_zonder_waterfront = dashboard_data.bereken_premies(waterfront_meenemen=False)

medianen_water = analyse.mediaan_per_groep(huizen, "groep_water").assign(laag="water")
medianen_groen = analyse.mediaan_per_groep(huizen, "groep_groen").assign(laag="groen")
medianen = pd.concat([medianen_water, medianen_groen])
oppervlak_per_groep = analyse.mediaan_per_groep(huizen, "groep_water", "m2")

ruw_water = medianen_water["median"].iloc[0] / medianen_water["median"].iloc[-1] - 1
ruw_groen = medianen_groen["median"].iloc[0] / medianen_groen["median"].iloc[-1] - 1
water = premies[premies["laag"] == "water"]
groen = premies[premies["laag"] == "groen"]
water_zonder_waterfront = premies_zonder_waterfront[premies_zonder_waterfront["laag"] == "water"]
verste_groep_water = analyse.waar_premie_stopt(water)

st.title("Onderbouwing")
st.write("Is de premie voor water echt, of liggen die huizen gewoon in een dure buurt? Zo heb ik dat uitgezocht.")

st.header("1. Eerste blik, zonder controles")
links, rechts = st.columns(2)
with links:
    st.plotly_chart(grafieken.staaf_mediaan(medianen))
    st.caption(f"Dichtbij lijkt water {ruw_water * 100:.0f}% en groen {ruw_groen * 100:.0f}% duurder dan ver weg.")
with rechts:
    st.plotly_chart(grafieken.staaf_kenmerk(oppervlak_per_groep, "Mediaan woonoppervlak (m2)"))
    st.caption("Maar huizen dicht bij water zijn ook groter en van hogere kwaliteit. Een eerlijke vergelijking moet daarvoor corrigeren.")

st.header("2. Met controles")
st.plotly_chart(grafieken.staaf_premie(premies))
st.caption(
    "Premie ten opzichte van vergelijkbare huizen verder dan 2 km. Het streepje is het 95% interval: "
    "raakt het de 0, dan is er geen aantoonbaar verschil. "
    f"Water houdt {water.iloc[0]['premie_procent']:.0f}% over, groen niets."
)

links, rechts = st.columns(2)
with links:
    st.header("3. Waar houdt het op?")
    st.plotly_chart(grafieken.staaf_premie_water(water))
    st.caption(
        f"Aantoonbaar duurder tot en met {verste_groep_water}. Binnen 250 m is dat ongeveer "
        f"{water.iloc[0]['premie_dollar']:.0f} dollar per m2. Bij 1 tot 2 km raakt het interval de 0."
    )
with rechts:
    st.header("4. Is het alleen de waterfront-kolom?")
    waterfront_vergelijking = pd.concat([
        water.assign(huizen="Alle huizen"),
        water_zonder_waterfront.assign(huizen="Zonder waterfront"),
    ])
    st.plotly_chart(grafieken.staaf_waterfront(waterfront_vergelijking))
    st.caption(
        "De data heeft een kolom voor huizen direct aan het water. Zonder die huizen "
        f"({aantal_zonder_waterfront:,} over) blijft de premie bestaan.".replace(",", ".")
    )

st.header("5. Het model")
st.write(
    "Ik verklaar de log van de prijs per m2. Door de log lees je de coefficienten als procenten. "
    "Naast de afstandsgroepen van water en groen controleer ik voor: woonoppervlak, perceeloppervlak, "
    "kwaliteit (grade), staat (condition), bouwjaar, afstand tot het centrum van Seattle en postcode."
)
kolom_n, kolom_r2 = st.columns(2)
kolom_n.metric("Aantal huizen", f"{aantal_huizen:,}".replace(",", "."))
kolom_r2.metric("R2", f"{r2:.2f}")
st.caption(f"R2 {r2:.2f} betekent dat het model {r2 * 100:.0f}% van de verschillen in prijs per m2 verklaart.")

st.header("6. Voorbehoud")
st.markdown(
    """
- Dit is een verband en geen bewijs dat water de oorzaak is. Dingen die ik niet kan meten, zoals het echte uitzicht of de staat van de keuken, kunnen meespelen.
- De data gaat over een jaar (mei 2014 tot mei 2015) en over een regio. In andere jaren of steden kan het anders zijn.
- Afstand is gemeten tot het dichtstbijzijnde punt op de rand van het water of park, dus niet tot een strand of een uitzicht.
"""
)
