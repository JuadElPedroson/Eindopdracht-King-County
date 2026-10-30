# Geo-stappen: water ophalen, eerst filteren, dan afstand uitrekenen.
# Het water komt uit OpenStreetMap (Overpass API).
import json
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


def haal_water_op(grens, pad="data/raw/water_osm.json"):
    # Haalt meren, rivieren en kustlijn op. Dit kan een paar minuten duren.
    zuid, west, noord, oost = grens
    vak = f"({zuid},{west},{noord},{oost})"
    vraag = (
        "[out:json][timeout:180];("
        f'way["natural"="water"]{vak};'
        f'way["natural"="coastline"]{vak};'
        f'relation["natural"="water"]{vak};'
        ");out geom;"
    )
    verzoek = urllib.request.Request(
        OVERPASS,
        data=urllib.parse.urlencode({"data": vraag}).encode(),
        headers={"User-Agent": "studieproject-king-county"},
    )
    with urllib.request.urlopen(verzoek, timeout=300) as antwoord:
        tekst = antwoord.read().decode("utf-8")
    with open(pad, "w") as f:
        f.write(tekst)


def maak_water_punten(data, grens, min_grootte=200, marge=0.1):
    # Eerst filteren, dan rekenen: van de ruwe OpenStreetMap-data
    # blijft een tabel met punten langs de rand van het water over.
    zuid, west, noord, oost = grens
    rijen = []
    for element in data["elements"]:
        lijnen = []
        if element["type"] == "way":
            lijnen.append(element.get("geometry"))
        elif element["type"] == "relation":
            for lid in element.get("members", []):
                lijnen.append(lid.get("geometry"))
        naam = element["type"] + str(element["id"])
        soort = "kust" if element.get("tags", {}).get("natural") == "coastline" else "water"
        for lijn in lijnen:
            for punt in lijn or []:
                # soms is een punt leeg (een gat), die slaan we over
                if punt and "lat" in punt and "lon" in punt:
                    rijen.append((naam, soort, punt["lat"], punt["lon"]))

    water = pd.DataFrame(rijen, columns=["object", "soort", "lat", "lon"])
    tel = {"objecten_ruw": water["object"].nunique(), "punten_ruw": len(water)}

    # alleen punten in en vlak om het gebied van de huizen
    water = water[
        water["lat"].between(zuid - marge, noord + marge)
        & water["lon"].between(west - marge, oost + marge)
    ]
    water = water.drop_duplicates(subset=["object", "lat", "lon"]).copy()

    # naar meters, dan kunnen we de grootte en afstand uitrekenen
    water["x"], water["y"] = naar_meters(water["lat"], water["lon"])

    # kleine vijvers en zwembaden weg. De kustlijn laten we altijd staan,
    # want die staat in stukjes in de data en elk stukje kan klein zijn.
    groep = water.groupby("object")
    breedte = groep["x"].transform("max") - groep["x"].transform("min")
    hoogte = groep["y"].transform("max") - groep["y"].transform("min")
    groot = (breedte >= min_grootte) | (hoogte >= min_grootte)
    water = water[groot | (water["soort"] == "kust")].reset_index(drop=True)

    tel["objecten_na"] = water["object"].nunique()
    tel["punten_na"] = len(water)
    return water, tel


def afstand_tot(huizen, water):
    # Per huis de afstand (in meter) tot het dichtstbijzijnde waterpunt.
    boom = cKDTree(np.column_stack([water["x"], water["y"]]))
    x, y = naar_meters(huizen["lat"], huizen["long"])
    afstand, plek = boom.query(np.column_stack([x, y]))
    soort = water["soort"].to_numpy()[plek]
    return afstand, soort
