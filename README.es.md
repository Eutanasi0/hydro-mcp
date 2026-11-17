# Hydro MCP

[![CI](https://github.com/Eutanasi0/hydro-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/Eutanasi0/hydro-mcp/actions/workflows/ci.yml)

English | [Español](README.es.md)

Servidor MCP de solo lectura que permite a los agentes de IA consultar datos hidrológicos abiertos de Perú (SQLite) con guardrails.

## Resumen

Este proyecto expone un servidor MCP local que permite a clientes de IA consultar información hidrológica de Perú de forma segura y de solo lectura. La idea es permitir que un agente inspeccione tablas, comprenda el esquema y ejecute consultas `SELECT` limitadas sin acceso directo a la base de datos ni permisos de escritura.

## ¿Qué es MCP?

MCP significa Model Context Protocol. Es un estándar abierto para conectar agentes de IA con herramientas y fuentes de datos externas mediante una interfaz consistente.

En este repositorio, el servidor expone tres herramientas:

- `list_tables()`
- `describe_table(table)`
- `run_select(sql, limit=50)`

## ¿Por qué existe este proyecto?

El repositorio actúa como un adaptador seguro entre un cliente de IA y una base de datos SQLite. En lugar de exponer la base directamente, restringe la interacción a operaciones de lectura controladas y valida el SQL antes de ejecutarlo.

## Funcionalidades

- acceso de solo lectura a la base de datos
- validación del SQL y bloqueo de sentencias no `SELECT`
- listado de tablas e introspección de esquema
- respuestas JSON mínimas y amigables para agentes
- integración local MCP para OpenCode y clientes similares

## Requisitos

- Python 3.10+
- entorno virtual recomendado
- dependencias desde `requirements.txt`

## Instalación

```bash
cd <ruta-del-proyecto>
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Inicio rápido

Ejecuta el servidor MCP:

```bash
python server.py
```

Ejecuta el cliente demo:

```bash
python client_demo.py
```

## Uso

### `list_tables()`

Lista todas las tablas disponibles en la base de datos SQLite.

```python
await session.call_tool("list_tables", {})
```

### `describe_table(table)`

Devuelve el esquema de una tabla concreta.

```python
await session.call_tool("describe_table", {"table": "mi_tabla"})
```

### `run_select(sql, limit=50)`

Ejecuta una consulta de solo lectura con un límite de seguridad.

```python
await session.call_tool(
    "run_select",
    {"sql": "SELECT * FROM mi_tabla LIMIT 10", "limit": 10},
)
```

## Seguridad

El servidor restringe intencionalmente el acceso:

- solo se permiten consultas `SELECT`
- se rechazan sentencias con `;`
- escrituras, borrados y cambios de esquema quedan bloqueados
- las filas se limitan a 100 por consulta

## Datos

El conjunto de datos usado en este proyecto es el conjunto hidrológico de emergencias publicado en `datosabiertos.gob.pe`.

- Fuente: `datosabiertos.gob.pe`
- Publicador: `Superintendencia Nacional de Servicios y Saneamiento (SUNASS)`
- Contexto: publicación abierta de datos públicos sobre riesgos hídricos y declaratorias de emergencia en Perú
- Licencia: datos públicos del sector público bajo el marco de gobierno de datos abiertos del Perú; revisa la página del conjunto para confirmar la declaración exacta de licencia publicada por el organismo

El CSV raw se mantiene en la raíz del repositorio:

```bash
DSHidricos_Dataset.csv
```

Si el archivo crece, muévelo a `data/` y añade un script de descarga pequeño.

## Plantilla para OpenCode

Usa el archivo de ejemplo como plantilla:

```bash
cp opencode.example.json opencode.json
```

Luego actualiza las rutas para que coincidan con tu entorno local.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "datos-peru": {
      "type": "local",
      "command": [
        "<ruta-al-entorno-virtual>/bin/python",
        "<ruta-del-proyecto>/server.py"
      ],
      "environment": {
        "DATOS_DB": "<ruta-del-proyecto>/data/datos.db"
      },
      "enabled": true
    }
  }
}
```

## Estructura del proyecto

- `server.py` — punto de entrada del servidor MCP
- `db.py` — acceso a SQLite y lógica de validación
- `client_demo.py` — ejemplo de sesión cliente
- `build_db.py` — cargador CSV a SQLite
- `opencode.example.json` — plantilla para la configuración local de OpenCode
- `data/` — base de datos y recursos locales
- `requirements.txt` — dependencias de Python fijadas

## Estado de CI

La última ejecución de GitHub Actions se comprueba con el badge de arriba. Verifiqué que el repositorio tuvo CI fallida antes; esos problemas se corrigieron localmente y la validación pasa (`ruff` + `pytest`). Tras hacer push del arreglo, el badge mostrará el estado verde.

## Licencia y uso

Este proyecto está pensado para integración local y análisis de datos hidrológicos públicos en IA, de forma de solo lectura. Úsalo con responsabilidad y conforme a los términos de la fuente del conjunto de datos y la normativa peruana de datos abiertos.
