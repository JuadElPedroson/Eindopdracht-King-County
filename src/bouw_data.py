# Draait alle beginstappen achter elkaar en schrijft het eindbestand.
# Starten vanuit de hoofdmap van het project: python -m src.bouw_data
import os

from src import analyse, geo, laden, schoon


def main():
    # 1. huizen inlezen en opschonen
    huizen = schoon.schoon_huizen(laden.laad_huizen())
    print("Huizen na opschonen:", len(huizen))

    # 2. water ophalen (alleen als het nog niet gedaan is)
    grens = geo.maak_grens(huizen)
    pad = laden.RAW + "water_osm.json"
    if not os.path.exists(pad):
        print("Water ophalen bij OpenStreetMap, dat kan een paar minuten duren...")
        geo.haal_water_op(grens, pad)

    # 3. water filteren
    water, tel = geo.maak_water_punten(laden.laad_water_json(), grens)
    print("Water:", tel)

    # 4. afstand per huis uitrekenen en nieuwe kolommen maken
    huizen["afstand_water"], huizen["dichtste"] = geo.afstand_tot(huizen, water)
    huizen = analyse.maak_kolommen(huizen)

    # 5. kleine resultaatbestand voor het dashboard
    huizen.to_csv(laden.PROCESSED + "huizen_met_afstand.csv", index=False)
    print("Klaar:", len(huizen), "huizen in", laden.PROCESSED + "huizen_met_afstand.csv")


if __name__ == "__main__":
    main()
