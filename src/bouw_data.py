# Draait alle beginstappen achter elkaar en schrijft het eindbestand.
# Starten vanuit de hoofdmap van het project: python -m src.bouw_data
import os

import pandas as pd

from src import analyse, geo, laden, schoon

# Centrum van Seattle, voor de controle "centraal wonen"
CENTRUM = (47.6062, -122.3321)


def main():
    log = []  # (onderdeel, stap, aantal), wordt opgeslagen voor het dashboard

    # 1. huizen inlezen en opschonen
    ruw = laden.laad_huizen()
    huizen, stappen = schoon.schoon_huizen(ruw)
    log.append(("huizen", "begin", len(ruw)))
    for stap, aantal in stappen:
        log.append(("huizen", "weg: " + stap, aantal))
    log.append(("huizen", "over", len(huizen)))
    print("Huizen:", len(ruw), "voor,", len(huizen), "na opschonen")
    grens = geo.maak_grens(huizen)

    # 2. per laag: ophalen (alleen als het bestand er nog niet is), filteren, afstand
    lagen = [
        ("water", geo.WATER, 200),
        ("groen", geo.GROEN, 100),
    ]
    for naam, labels, min_grootte in lagen:
        pad = laden.RAW + naam + "_osm.json"
        if not os.path.exists(pad):
            print("Ophalen bij OpenStreetMap:", naam, "(kan een paar minuten duren)...")
            geo.haal_op(grens, labels, pad)
        punten, tel = geo.maak_punten(laden.laad_json(pad), grens, naam, min_grootte)
        print(naam, tel)
        for sleutel, aantal in tel.items():
            log.append((naam, sleutel, aantal))
        huizen["afstand_" + naam], huizen["dichtste_" + naam] = geo.afstand_tot(huizen, punten)

    # 3. controle: afstand tot het centrum van Seattle
    huizen["afstand_centrum"] = geo.afstand_tot_punt(huizen, CENTRUM[0], CENTRUM[1])

    # 4. nieuwe kolommen maken
    huizen = analyse.maak_kolommen(huizen)

    # 5. kleine resultaatbestanden voor het dashboard
    huizen.to_csv(laden.PROCESSED + "huizen_met_afstand.csv", index=False)
    pd.DataFrame(log, columns=["onderdeel", "stap", "aantal"]).to_csv(
        laden.PROCESSED + "opschonen_log.csv", index=False
    )
    print("Klaar:", len(huizen), "huizen in", laden.PROCESSED + "huizen_met_afstand.csv")


if __name__ == "__main__":
    main()
