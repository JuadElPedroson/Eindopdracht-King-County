# Nieuwe kolommen, berekeningen en modellen.
import numpy as np
import pandas as pd

M2_PER_SQFT = 0.092903

# Verder dan 2 km zijn er te weinig huizen voor aparte groepen (bij water 1 huis boven 5 km).
GRENZEN = [0, 250, 500, 1000, 2000, np.inf]
NAMEN = ["0-250 m", "250-500 m", "500 m-1 km", "1-2 km", "meer dan 2 km"]


def maak_kolommen(df):
    df = df.copy()
    # de data staat in vierkante voet, wij rekenen in vierkante meter
    df["m2"] = df["sqft_living"] * M2_PER_SQFT
    df["prijs_per_m2"] = df["price"] / df["m2"]
    df["groep_water"] = pd.cut(df["afstand_water"], bins=GRENZEN, labels=NAMEN, include_lowest=True)
    df["groep_groen"] = pd.cut(df["afstand_groen"], bins=GRENZEN, labels=NAMEN, include_lowest=True)
    return df


def mediaan_per_groep(df, kolom="groep_water"):
    # eerste blik: prijs per m2 per afstandsgroep
    # (uit een csv komt de groep terug als tekst, dit zet de volgorde weer goed)
    df = df.copy()
    df[kolom] = pd.Categorical(df[kolom], categories=NAMEN, ordered=True)
    uit = df.groupby(kolom, observed=True)["prijs_per_m2"].agg(["size", "median"])
    return uit.round(0).reset_index().rename(columns={kolom: "afstandsgroep"})
