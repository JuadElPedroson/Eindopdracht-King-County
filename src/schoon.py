# Opschonen als losse functies, elke functie doet een ding.
import pandas as pd


def streepjes_naar_leeg(df):
    # voorbeeld: return df.replace("-", pd.NA)
    return df


def haal_uitschieters_weg(df):
    # voorbeeld: return df[df["kolom"] >= -60]
    return df


def maak_schoon(df):
    # hier zet je de stappen op een rij
    df = streepjes_naar_leeg(df)
    df = haal_uitschieters_weg(df)
    return df
