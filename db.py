# db.py
import os, re, sqlite3
from contextlib import closing
from pathlib import Path

DEFAULT_DB = os.environ.get(
    "DATOS_DB", str(Path(__file__).parent / "data" / "datos.db")
)

MAX_ROWS = 100

def _connect(db_path):
    # modo solo lectura: SQLite rechaza escrituras aunque se cuele una
    return sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

def list_tables(db_path=DEFAULT_DB):
    with closing(_connect(db_path)) as con:
        rows = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    return [r[0] for r in rows]

def describe_table(table, db_path=DEFAULT_DB):
    if table not in list_tables(db_path):
        raise ValueError(f"Tabla desconocida: {table}")
    with closing(_connect(db_path)) as con:
        cols = con.execute(f'PRAGMA table_info("{table}")').fetchall()
    return [{"name": c[1], "type": c[2]} for c in cols]

def run_select(sql, limit=50, db_path=DEFAULT_DB):
    stmt = sql.strip().rstrip(";")
    if ";" in stmt or not re.match(r"(?is)^\s*select\b", stmt):
        raise ValueError("Solo se permite una sentencia SELECT.")
    limit = max(1, min(limit, MAX_ROWS))
    with closing(_connect(db_path)) as con:
        cur = con.execute(f"SELECT * FROM ({stmt}) LIMIT ?", (limit,))
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
    return {"columns": cols, "rows": rows, "truncated": len(rows) == limit}