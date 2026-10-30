# Grafieken als functies, zodat ze op meerdere pagina's te gebruiken zijn.
import plotly.express as px

from src.analyse import NAMEN

KLEUREN = {"water": "#1f77b4", "groen": "#2ca02c"}


def kaart_huizen(huizen, kleur_kolom, kleur_titel, kleurschaal):
    """Kaart met een stip per huis. De kleurschaal loopt van het 5e tot het 95e percentiel,
    anders bepalen een paar dure uitschieters de hele schaal."""
    laag, hoog = huizen[kleur_kolom].quantile([0.05, 0.95])
    figuur = px.scatter_map(
        huizen,
        lat="lat",
        lon="long",
        color=kleur_kolom,
        range_color=[laag, hoog],
        color_continuous_scale=kleurschaal,
        hover_data={"price": ":,.0f", "prijs_per_m2": ":.0f", "afstand_water": ":.0f",
                    "afstand_groen": ":.0f", "lat": False, "long": False},
        labels={"price": "Prijs (dollar)", "prijs_per_m2": "Prijs per m2",
                "afstand_water": "Afstand water (m)", "afstand_groen": "Afstand groen (m)"},
        center={"lat": 47.47, "lon": -121.95},
        zoom=8.7,
        height=620,
        opacity=0.7,
        map_style="carto-positron",
    )
    figuur.update_traces(marker_size=5)
    figuur.update_layout(coloraxis_colorbar_title=kleur_titel, margin=dict(l=0, r=0, t=0, b=0))
    return figuur


def staaf_mediaan(medianen):
    """Mediaan prijs per m2 per afstandsgroep, water en groen naast elkaar."""
    figuur = px.bar(
        medianen,
        x="afstandsgroep",
        y="median",
        color="laag",
        barmode="group",
        color_discrete_map=KLEUREN,
        category_orders={"afstandsgroep": NAMEN},
        labels={"afstandsgroep": "Afstand", "median": "Mediaan prijs per m2 (dollar)", "laag": ""},
        height=380,
    )
    return figuur


def staaf_premie(premies):
    """Premie per afstandsgroep in procent, met het 95% interval als streepje."""
    premies = premies.assign(
        fout_boven=premies["bovengrens"] - premies["premie_procent"],
        fout_onder=premies["premie_procent"] - premies["ondergrens"],
    )
    figuur = px.bar(
        premies,
        x="afstandsgroep",
        y="premie_procent",
        color="laag",
        barmode="group",
        error_y="fout_boven",
        error_y_minus="fout_onder",
        color_discrete_map=KLEUREN,
        category_orders={"afstandsgroep": NAMEN},
        labels={"afstandsgroep": "Afstand", "premie_procent": "Premie (%)", "laag": ""},
        height=380,
    )
    figuur.add_hline(y=0, line_width=1, line_color="gray")
    return figuur


def staaf_kenmerk(medianen, y_titel):
    """Mediaan van een kenmerk (bijvoorbeeld oppervlak) per afstand tot water."""
    figuur = px.bar(
        medianen,
        x="afstandsgroep",
        y="median",
        color_discrete_sequence=[KLEUREN["water"]],
        category_orders={"afstandsgroep": NAMEN},
        labels={"afstandsgroep": "Afstand tot water", "median": y_titel},
        height=380,
    )
    return figuur


def staaf_premie_water(premies_water):
    """Premie bij water. Blauw als het interval boven 0 ligt, grijs als het de 0 raakt."""
    premies_water = premies_water.assign(
        fout_boven=premies_water["bovengrens"] - premies_water["premie_procent"],
        fout_onder=premies_water["premie_procent"] - premies_water["ondergrens"],
        zekerheid=(premies_water["ondergrens"] > 0).map({True: "aantoonbaar duurder", False: "niet aantoonbaar"}),
    )
    figuur = px.bar(
        premies_water,
        x="afstandsgroep",
        y="premie_procent",
        color="zekerheid",
        error_y="fout_boven",
        error_y_minus="fout_onder",
        color_discrete_map={"aantoonbaar duurder": KLEUREN["water"], "niet aantoonbaar": "#b0b0b0"},
        category_orders={"afstandsgroep": NAMEN},
        hover_data={"premie_dollar": ":.0f", "fout_boven": False, "fout_onder": False},
        labels={"afstandsgroep": "Afstand tot water", "premie_procent": "Premie (%)",
                "premie_dollar": "Dollar per m2", "zekerheid": ""},
        height=380,
    )
    figuur.add_hline(y=0, line_width=1, line_color="gray")
    return figuur


def staaf_waterfront(premies_water_twee_groepen):
    """Premie bij water, met en zonder de huizen die in de data als waterfront staan."""
    figuur = px.bar(
        premies_water_twee_groepen,
        x="afstandsgroep",
        y="premie_procent",
        color="huizen",
        barmode="group",
        color_discrete_map={"Alle huizen": KLEUREN["water"], "Zonder waterfront": "#9ecae1"},
        category_orders={"afstandsgroep": NAMEN},
        labels={"afstandsgroep": "Afstand tot water", "premie_procent": "Premie (%)", "huizen": ""},
        height=380,
    )
    figuur.add_hline(y=0, line_width=1, line_color="gray")
    return figuur
