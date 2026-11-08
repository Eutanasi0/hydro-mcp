# build_db.py
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

import pandas as pd


def normalizar(col):
    """'Año de Medición' -> 'ano_de_medicion' (sin tildes ni espacios)."""
    s = unicodedata.normalize("NFKD", str(col)).encode("ascii", "ignore").decode()
    return re.sub(r"\W+", "_", s).strip("_").lower()


def leer_csv(path):
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            df = pd.read_csv(path, encoding=enc, sep=None, engine="python")
            print(f"Leído con codificación: {enc}")
            return df
        except UnicodeDecodeError:
            continue
    raise SystemExit("No pude decodificar el archivo.")


if __name__ == "__main__":
    csv_path, table = sys.argv[1], sys.argv[2]
    df = leer_csv(csv_path)
    df.columns = [normalizar(c) for c in df.columns]

    Path("data").mkdir(exist_ok=True)
    with sqlite3.connect("data/datos.db") as con:
        df.to_sql(table, con, if_exists="replace", index=False)
    print(f"{len(df)} filas, {len(df.columns)} columnas en '{table}'")
    print("Columnas:", list(df.columns))