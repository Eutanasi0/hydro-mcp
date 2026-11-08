import logging, sys
from mcp.server.mcpserver import MCPServer
import db

logging.basicConfig(stream=sys.stderr, level=logging.INFO)  # nunca print()
mcp = MCPServer("datos-peru")

@mcp.tool()
def list_tables() -> list[str]:
    """Lista las tablas disponibles en la base de datos."""
    return db.list_tables()

@mcp.tool()
def describe_table(table: str) -> list[dict]:
    """Devuelve el nombre y tipo de cada columna de una tabla."""
    return db.describe_table(table)

@mcp.tool()
def run_select(sql: str, limit: int = 50) -> dict:
    """Ejecuta una consulta SELECT de solo lectura (máximo 100 filas)."""
    return db.run_select(sql, limit)

if __name__ == "__main__":
    mcp.run()  # transporte stdio por defecto