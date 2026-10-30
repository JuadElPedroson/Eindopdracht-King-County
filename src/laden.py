# Data inlezen. Een functie per bronbestand.
# Draai alles vanuit de hoofdmap van het project, dan kloppen de paden.
import json
import pandas as pd

RAW = "data/raw/"
PROCESSED = "data/processed/"


def laad_huizen():
    # Kaggle: House Sales in King County, USA (kc_house_data.csv)
    return pd.read_csv(RAW + "kc_house_data.csv")


def laad_water_json():
    # Het bestand dat src/geo.py ophaalt bij OpenStreetMap
    with open(RAW + "water_osm.json") as f:
        return json.load(f)


def laad_schoon():
    # Het eindresultaat van src/bouw_data.py: huizen met afstand tot water
    return pd.read_csv(PROCESSED + "huizen_met_afstand.csv")
