# Opschonen als losse functies, elke functie doet een ding.
# Het opschonen van de water-data staat in geo.py, want dat hoort bij de geo-stappen.
import pandas as pd


def schoon_huizen(df):
    df = df.copy()

    # de datum is tekst zoals 20141013T000000
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%dT%H%M%S")

    # zonder prijs, oppervlak of plek kunnen we niets
    df = df.dropna(subset=["price", "sqft_living", "lat", "long"])
    df = df[(df["price"] > 0) & (df["sqft_living"] > 0)]

    # dezelfde verkoop twee keer erin
    df = df.drop_duplicates(subset=["id", "date"])

    # een woning heeft 33 slaapkamers, dat is een typefout
    df = df[df["bedrooms"] <= 15]

    return df.reset_index(drop=True)
