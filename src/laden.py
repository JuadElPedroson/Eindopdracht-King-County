# Data inlezen. Een functie per bronbestand.
# Draai alles vanuit de hoofdmap van het project, dan kloppen de paden.
import json
import pandas as pd

RAW = "data/raw/"
PROCESSED = "data/processed/"


def laad_huizen():
    # Kaggle: House Sales in King County, USA (kc_house_data.csv)
    return pd.read_csv(RAW + "kc_house_data.csv")


def laad_json(pad):
    # De bestanden die src/geo.py ophaalt bij OpenStreetMap (water en groen)
    with open(pad) as f:
        return json.load(f)


def laad_schoon():
    # Het eindresultaat van src/bouw_data.py: huizen met afstand tot water
    return pd.read_csv(PROCESSED + "huizen_met_afstand.csv")


def laad_log():
    # Wat er tijdens het opschonen is weggehaald (gemaakt door src/bouw_data.py)
    return pd.read_csv(PROCESSED + "opschonen_log.csv")
