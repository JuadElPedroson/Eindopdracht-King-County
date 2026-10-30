# Geo-stappen: water en groen ophalen, eerst filteren, dan afstand uitrekenen.
# Alles komt uit OpenStreetMap (Overpass API).
import urllib.parse
import urllib.request

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

OVERPASS = "https://overpass-api.de/api/interpreter"

# Midden van het gebied. Hiermee rekenen we graden om naar meters.
LAT0 = 47.5
LON0 = -122.0
METER_PER_GRAAD_LAT = 111000
METER_PER_GRAAD_LON = 111000 * np.cos(np.radians(LAT0))

# Wat we ophalen: per laag een lijst met OpenStreetMap-labels (sleutel, waarde).
WATER = [("natural", "water"), ("natural", "coastline")]
GROEN = [("leisure", "park")]
# Bos kan ook, maar dat zijn enorme vlakken en een veel groter bestand:
# GROEN = [("leisure", "park"), ("landuse", "forest")]


def maak_grens(huizen, marge=0.05):
    # Het vak om alle huizen heen, met wat extra ruimte. (zuid, west, noord, oost)
    return (
        huizen["lat"].min() - marge,
        huizen["long"].min() - marge,
        huizen["lat"].max() + marge,
        huizen["long"].max() + marge,
    )


def naar_meters(lat, lon):
    # Vlakke benadering, voor dit gebied klopt dat op minder dan 1 procent.
    x = (np.asarray(lon) - LON0) * METER_PER_GRAAD_LON
    y = (np.asarray(lat) - LAT0) * METER_PER_GRAAD_LAT
    return x, y


def haal_op(grens, labels, pad):
    # Haalt de objecten met deze labels op en slaat ze op. Kan een paar minuten duren.
    zuid, west, noord, oost = grens
    vak = f"({zuid},{west},{noord},{oost})"
    delen = ""
    for sleutel, waarde in labels:
        delen += f'way["{sleutel}"="{waarde}"]{vak};relation["{sleutel}"="{waarde}"]{vak};'
    vraag = f"[out:json][timeout:180];({delen});out geom;"
    verzoek = urllib.request.Request(
        OVERPASS,
        data=urllib.parse.urlencode({"data": vraag}).encode(),
        headers={"User-Agent": "studieproject-king-county"},
    )
    with urllib.request.urlopen(verzoek, timeout=300) as antwoord:
        tekst = antwoord.read().decode("utf-8")
    with open(pad, "w") as f:
        f.write(tekst)


def maak_punten(data, grens, naam, min_grootte=200, marge=0.1):
    # Eerst filteren, dan rekenen: van de ruwe OpenStreetMap-data
    # blijft een tabel met punten langs de rand van de objecten over.
    zuid, west, noord, oost = grens
    rijen = []
    for element in data["elements"]:
        lijnen = []
        if element["type"] == "way":
            lijnen.append(element.get("geometry"))
        elif element["type"] == "relation":
            for lid in element.get("members", []):
                lijnen.append(lid.get("geometry"))
        object_naam = element["type"] + str(element["id"])
        soort = "kust" if element.get("tags", {}).get("natural") == "coastline" else naam
        for lijn in lijnen:
            for punt in lijn or []:
                # soms is een punt leeg (een gat), die slaan we over
                if punt and "lat" in punt and "lon" in punt:
                    rijen.append((object_naam, soort, punt["lat"], punt["lon"]))

    punten = pd.DataFrame(rijen, columns=["object", "soort", "lat", "lon"])
    tel = {"objecten_ruw": punten["object"].nunique(), "punten_ruw": len(punten)}

    # alleen punten in en vlak om het gebied van de huizen
    punten = punten[
        punten["lat"].between(zuid - marge, noord + marge)
        & punten["lon"].between(west - marge, oost + marge)
    ]
    punten = punten.drop_duplicates(subset=["object", "lat", "lon"]).copy()

    # naar meters, dan kunnen we de grootte en afstand uitrekenen
    punten["x"], punten["y"] = naar_meters(punten["lat"], punten["lon"])

    # kleine objecten weg (vijvers, zwembaden, speeltuintjes). De kustlijn laten we
    # altijd staan, want die staat in stukjes in de data en elk stukje kan klein zijn.
    groep = punten.groupby("object")
    breedte = groep["x"].transform("max") - groep["x"].transform("min")
    hoogte = groep["y"].transform("max") - groep["y"].transform("min")
    groot = (breedte >= min_grootte) | (hoogte >= min_grootte)
    punten = punten[groot | (punten["soort"] == "kust")].reset_index(drop=True)

    tel["objecten_na"] = punten["object"].nunique()
    tel["punten_na"] = len(punten)
    return punten, tel


def afstand_tot(huizen, punten):
    # Per huis de afstand (in meter) tot het dichtstbijzijnde punt.
    boom = cKDTree(np.column_stack([punten["x"], punten["y"]]))
    x, y = naar_meters(huizen["lat"], huizen["long"])
    afstand, plek = boom.query(np.column_stack([x, y]))
    soort = punten["soort"].to_numpy()[plek]
    return afstand, soort


def afstand_tot_punt(huizen, lat, lon):
    # Afstand (in meter) van elk huis tot een vast punt, bijvoorbeeld het centrum.
    x, y = naar_meters(huizen["lat"], huizen["long"])
    px, py = naar_meters(lat, lon)
    return np.sqrt((x - px) ** 2 + (y - py) ** 2)
