# Opschonen als losse functies, elke functie doet een ding.
# Het opschonen van water en groen staat in geo.py, want dat hoort bij de geo-stappen.
import pandas as pd


def schoon_huizen(df):
    # Geeft de schone data terug, plus een lijstje met wat er per stap is weggehaald.
    log = []
    df = df.copy()

    # de datum is tekst zoals 20141013T000000
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%dT%H%M%S")

    # zonder prijs, oppervlak of plek kan ik niets
    n = len(df)
    df = df.dropna(subset=["price", "sqft_living", "lat", "long"])
    df = df[(df["price"] > 0) & (df["sqft_living"] > 0)]
    log.append(("geen prijs, oppervlak of plek", n - len(df)))

    # een woning heeft 33 slaapkamers, dat is een typefout
    n = len(df)
    df = df[df["bedrooms"] <= 15]
    log.append(("meer dan 15 slaapkamers (typefout)", n - len(df)))

    # een woning zonder slaapkamer of badkamer bestaat niet, dat zijn fouten in de data
    n = len(df)
    df = df[(df["bedrooms"] > 0) & (df["bathrooms"] > 0)]
    log.append(("geen slaapkamer of badkamer", n - len(df)))

    # sommige huizen zijn twee keer verkocht, ik hou de laatste verkoop
    n = len(df)
    df = df.sort_values("date").drop_duplicates(subset="id", keep="last")
    log.append(("zelfde huis vaker verkocht (oudste verkoop weg)", n - len(df)))

    return df.sort_index().reset_index(drop=True), log
