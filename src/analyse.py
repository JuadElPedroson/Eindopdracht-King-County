# Nieuwe kolommen, berekeningen en het regressiemodel.
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

M2_PER_SQFT = 0.092903

# Verder dan 2 km zijn er te weinig huizen voor aparte groepen (bij water 1 huis boven 5 km).
GRENZEN = [0, 250, 500, 1000, 2000, np.inf]
NAMEN = ["0-250 m", "250-500 m", "500 m-1 km", "1-2 km", "meer dan 2 km"]
VERGELIJKING = "meer dan 2 km"


def maak_kolommen(df):
    df = df.copy()
    # de data staat in vierkante voet, ik reken in vierkante meter
    df["m2"] = df["sqft_living"] * M2_PER_SQFT
    df["prijs_per_m2"] = df["price"] / df["m2"]
    df["groep_water"] = pd.cut(df["afstand_water"], bins=GRENZEN, labels=NAMEN, include_lowest=True)
    df["groep_groen"] = pd.cut(df["afstand_groen"], bins=GRENZEN, labels=NAMEN, include_lowest=True)
    return df


def mediaan_per_groep(df, kolom, waarde="prijs_per_m2"):
    """Mediaan van een kolom (standaard prijs per m2) per afstandsgroep, zonder controles."""
    df = df.copy()
    # uit een csv komt de groep terug als tekst, dit zet de volgorde weer goed
    df[kolom] = pd.Categorical(df[kolom], categories=NAMEN, ordered=True)
    uit = df.groupby(kolom, observed=True)[waarde].agg(["size", "median"])
    return uit.round(0).reset_index().rename(columns={kolom: "afstandsgroep"})


def draai_regressie(huizen):
    """Verklaart de log van prijs per m2 met de afstandsgroepen en een paar controles.

    De groep 'meer dan 2 km' is het vergelijkingspunt. De coefficient van een groep
    zegt dus hoeveel duurder (in procent) die huizen zijn dan huizen ver weg.
    """
    huizen = huizen.copy()
    huizen["afstand_centrum_km"] = huizen["afstand_centrum"] / 1000
    ver_weg = f'Treatment("{VERGELIJKING}")'
    formule = (
        f"np.log(prijs_per_m2) ~ C(groep_water, {ver_weg}) + C(groep_groen, {ver_weg})"
        " + np.log(m2) + np.log(sqft_lot) + grade + condition + yr_built"
        " + afstand_centrum_km + C(zipcode)"
    )
    return smf.ols(formule, data=huizen).fit()


def premie_tabel(model, huizen):
    """Premie per afstandsgroep in procent en in dollar per m2, met een 95% interval."""
    intervallen = model.conf_int()
    rijen = []
    for laag in ["water", "groen"]:
        ver_weg = huizen["groep_" + laag] == VERGELIJKING
        basisprijs = huizen.loc[ver_weg, "prijs_per_m2"].median()
        for groep in NAMEN[:-1]:
            naam = f'C(groep_{laag}, Treatment("{VERGELIJKING}"))[T.{groep}]'
            premie = np.exp(model.params[naam]) - 1
            onder, boven = np.exp(intervallen.loc[naam]) - 1
            rijen.append({
                "laag": laag,
                "afstandsgroep": groep,
                "premie_procent": premie * 100,
                "ondergrens": onder * 100,
                "bovengrens": boven * 100,
                "premie_dollar": premie * basisprijs,
                "dollar_onder": onder * basisprijs,
                "dollar_boven": boven * basisprijs,
            })
    return pd.DataFrame(rijen)


def waar_premie_stopt(premies_van_een_laag):
    """De verste groep waarvan het hele interval boven 0 ligt. None als er geen is."""
    echt_hoger = premies_van_een_laag[premies_van_een_laag["ondergrens"] > 0]
    if echt_hoger.empty:
        return None
    return echt_hoger["afstandsgroep"].iloc[-1]
