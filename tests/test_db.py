# tests/test_db.py
import sqlite3, pytest
import db

@pytest.fixture
def path(tmp_path):
    p = tmp_path / "t.db"
    with sqlite3.connect(p) as con:
        con.execute("CREATE TABLE personas (id INTEGER, nombre TEXT)")
        con.executemany("INSERT INTO personas VALUES (?, ?)",
                        [(i, f"n{i}") for i in range(200)])
    return str(p)

def test_list_tables(path):
    assert db.list_tables(path) == ["personas"]

def test_limit_se_respeta(path):
    r = db.run_select("SELECT * FROM personas", limit=500, db_path=path)
    assert len(r["rows"]) == db.MAX_ROWS and r["truncated"]

@pytest.mark.parametrize("sql", [
    "DROP TABLE personas",
    "SELECT 1; DROP TABLE personas",
    "DELETE FROM personas",
])
def test_rechaza_no_select(path, sql):
    with pytest.raises(ValueError):
        db.run_select(sql, db_path=path)

def test_tabla_desconocida(path):
    with pytest.raises(ValueError):
        db.describe_table("no_existe", db_path=path)