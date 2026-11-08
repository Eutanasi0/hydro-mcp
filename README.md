# Hydro MCP

This project implements an MCP (Model Context Protocol) server for querying a SQLite database with hydrological data from Peru. The goal is to allow an AI model to access structured information from the Peruvian water sector in a secure way without granting write permissions or direct database access.

## What is an MCP?

MCP stands for Model Context Protocol, an open standard that enables AI models to connect with external tools, services, and data sources in a consistent and secure way.

In practical terms, an MCP server exposes a set of functions or tools that an AI client can invoke. This avoids forcing the model to implement custom logic for each system and allows external sources to be integrated through a standardized interface.

In this project, the server exposes tools to:

- list tables available in the database
- describe the schema of a table
- run read-only `SELECT` queries on hydrological data from Peru

## What does this repository do?

The repository includes a local server that acts as an intermediary between an AI client and a SQLite database containing hydrological information from Peru. The access layer is designed to limit query scope and reduce the risk of misuse.

### Available tools

- `list_tables()`: returns the tables available in the database.
- `describe_table(table)`: returns the name and type of each column in a table.
- `run_select(sql, limit=50)`: executes a safe, limited read query.

The main database access logic is implemented in `db.py`, while the MCP exposure is defined in `server.py`.

## Project structure

- `server.py`: MCP server exposing the public tools.
- `db.py`: SQLite connection and security validation logic.
- `client_demo.py`: example Python client that connects to the server.
- `build_db.py`: script to load a CSV with hydrological data from Peru into SQLite.
- `opencode.json`: configuration for integrating this MCP with OpenCode.
- `data/`: folder containing the database and related resources.
- `requirements.txt`: project dependencies.

## Requirements

- Python 3.x
- recommended virtual environment
- dependencies installed from `requirements.txt`

## Installation

```bash
cd <project-path>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick start

### Run the server

```bash
python server.py
```

The server runs by default with `stdio` transport, which is the standard mode for local MCP integration.

### Test the connection with the example client

```bash
python client_demo.py
```

This script opens an MCP session and calls `list_tables()` to verify that the server responds correctly.

## Using the tools

### `list_tables()`

Returns the list of tables available in the database.

Example:

```python
await session.call_tool("list_tables", {})
```

### `describe_table(table)`

Returns the schema for a specific table, including the name and type of each column.

Example:

```python
await session.call_tool("describe_table", {"table": "my_table"})
```

### `run_select(sql, limit=50)`

Executes a read-only `SELECT` query. The server validates the statement to prevent unauthorized operations.

Example:

```python
await session.call_tool(
    "run_select",
    {"sql": "SELECT * FROM my_table LIMIT 10", "limit": 10}
)
```

### Security constraints

- only accepts `SELECT` statements
- blocks queries containing `;`
- does not allow writes or DDL/DML operations
- limits returned rows to a maximum of 100

## OpenCode configuration

The `opencode.json` file is prepared to integrate this server with OpenCode. The configuration points to the virtual environment interpreter and the server entry point.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "datos-peru": {
      "type": "local",
      "command": [
        "<path-to-virtualenv>/bin/python",
        "<path-to-project>/server.py"
      ],
      "environment": {
        "DATOS_DB": "<path-to-project>/data/datos.db"
      },
      "enabled": true
    }
  }
}
```

This allows the AI client to detect and use the server tools as part of the available context.

## Database

The SQLite database for the project is typically located at:

```bash
data/datos.db
```

You can change the path using the `DATOS_DB` environment variable:

```bash
export DATOS_DB=/path/to/your/database.db
python server.py
```

## Load data from CSV

If you want to create or replace the database from a CSV containing Peruvian hydrological data, use `build_db.py`.

```bash
python build_db.py data.csv table_name
```

The script:

- reads the CSV
- normalizes column names
- saves the data to SQLite

## Security and design

This server is designed for controlled, secure operation:

- only allows read access
- blocks statements that could modify the database
- limits the volume of data returned
- reduces the risk surface for AI integration

This makes it suitable for AI-assisted analysis of hydrological data from Peru, but it does not replace broader access control policies in production environments.

## Typical usage flow

1. register this server as an MCP in the AI client
2. the model discovers the available tools
3. requests `list_tables()` to see the available data
4. inspects a table schema with `describe_table()`
5. runs a `SELECT` with `run_select()`
6. the client uses the results as context to answer or analyze the hydrological information

## Summary

This repository demonstrates a practical pattern for integrating AI models with real data via MCP, centered on hydrological information from Peru. The central idea is to expose only the necessary operations while keeping database access under control.

It is especially useful for:

- AI-guided analysis of water resources
- queries on Peruvian data and water management
- assistants that require real-world context
- integration of models with hydrological information systems

This README can be easily extended with more SQL examples, instructions for additional MCP clients, or deployment documentation.

---

# Hydro MCP

Este proyecto implementa un servidor MCP (Model Context Protocol) para consultar una base de datos SQLite con datos hidrológicos de Perú. El objetivo es permitir que un modelo de IA acceda a información estructurada del sector hídrico peruano de forma segura, sin otorgarle permisos de escritura ni acceso directo a la base de datos.

## ¿Qué es un MCP?

MCP significa Model Context Protocol, un estándar abierto que permite conectar modelos de IA con herramientas externas, servicios y fuentes de datos de manera consistente y segura.

En la práctica, un servidor MCP expone un conjunto de funciones o herramientas que un cliente de IA puede invocar. Esto evita que el modelo tenga que implementar lógica específica para cada sistema y permite integrar fuentes externas a través de una interfaz estandarizada.

En este proyecto, el servidor expone herramientas para:

- listar tablas disponibles en la base de datos
- describir el esquema de una tabla
- ejecutar consultas `SELECT` de solo lectura sobre datos hidrológicos de Perú

## ¿Qué hace este repositorio?

El repositorio incluye un servidor local que actúa como intermediario entre un cliente de IA y una base de datos SQLite con información hidrológica del Perú. La capa de acceso está diseñada para limitar el alcance de las consultas y reducir el riesgo de uso indebido.

### Herramientas disponibles

- `list_tables()`: devuelve las tablas disponibles en la base de datos.
- `describe_table(table)`: devuelve el nombre y tipo de cada columna de una tabla.
- `run_select(sql, limit=50)`: ejecuta una consulta de lectura segura y limitada.

La lógica principal de acceso a la base de datos está en `db.py`, mientras que la exposición como herramientas MCP se realiza en `server.py`.

## Estructura del proyecto

- `server.py`: servidor MCP con las herramientas públicas.
- `db.py`: conexión a SQLite y validaciones de seguridad.
- `client_demo.py`: ejemplo de cliente Python que se conecta al servidor.
- `build_db.py`: script para cargar un CSV con datos hidrológicos de Perú en SQLite.
- `opencode.json`: configuración para integrar este MCP con OpenCode.
- `data/`: carpeta con la base de datos y recursos relacionados.
- `requirements.txt`: dependencias del proyecto.

## Requisitos

- Python 3.x
- entorno virtual recomendado
- dependencias instaladas desde `requirements.txt`

## Instalación

```bash
cd <ruta-del-proyecto>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Inicio rápido

### Ejecutar el servidor

```bash
python server.py
```

El servidor se inicia por defecto con transporte `stdio`, que es el modo más común para integración local con clientes MCP.

### Probar la conexión con el cliente de ejemplo

```bash
python client_demo.py
```

Este script abre una sesión MCP y llama a `list_tables()` para verificar que el servidor responde correctamente.

## Uso de las herramientas

### `list_tables()`

Devuelve la lista de tablas disponibles en la base de datos.

Ejemplo:

```python
await session.call_tool("list_tables", {})
```

### `describe_table(table)`

Devuelve el esquema de una tabla concreta, incluyendo el nombre y tipo de cada columna.

Ejemplo:

```python
await session.call_tool("describe_table", {"table": "mi_tabla"})
```

### `run_select(sql, limit=50)`

Ejecuta una consulta `SELECT` de solo lectura. El servidor valida la sentencia para impedir operaciones no permitidas.

Ejemplo:

```python
await session.call_tool(
    "run_select",
    {"sql": "SELECT * FROM mi_tabla LIMIT 10", "limit": 10}
)
```

### Restricciones de seguridad

- solo admite sentencias `SELECT`
- bloquea consultas con punto y coma `;`
- no permite escrituras ni operaciones DDL/DML
- limita el número de filas devueltas a un máximo de 100

## Configuración con OpenCode

El archivo `opencode.json` está preparado para integrar este servidor con OpenCode. La configuración apunta al intérprete del entorno virtual y al ejecutable del servidor.

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

Esto permite que el cliente de IA detecte y use las herramientas del servidor como parte del contexto disponible.

## Base de datos

La base de datos SQLite del proyecto normalmente se ubica en:

```bash
data/datos.db
```

Puedes cambiar la ruta con la variable de entorno `DATOS_DB`:

```bash
export DATOS_DB=/ruta/a/tu/base.db
python server.py
```

## Cargar datos desde CSV

Si deseas crear o reemplazar la base de datos a partir de un archivo CSV con información hidrológica peruana, puedes usar `build_db.py`.

```bash
python build_db.py datos.csv nombre_tabla
```

El script:

- lee el CSV
- normaliza los nombres de columnas
- guarda los datos en SQLite

## Seguridad y diseño

Este servidor está pensado para operar en un entorno controlado y seguro:

- solo permite lectura
- bloquea instrucciones que puedan modificar la base de datos
- limita el volumen de datos devueltos
- reduce la superficie de riesgo para la integración con IA

Esto lo hace adecuado para análisis asistido por modelos sobre datos hídricos de Perú, pero no sustituye una política de acceso a datos más amplia en entornos productivos.

## Flujo típico de uso

1. se registra este servidor como MCP en el cliente de IA
2. el modelo descubre las herramientas disponibles
3. solicita `list_tables()` para ver qué datos existen
4. consulta el esquema de una tabla con `describe_table()`
5. ejecuta una `SELECT` con `run_select()`
6. el cliente usa los resultados como contexto para responder o analizar la información hidrológica peruana

## Resumen

Este repositorio demuestra un patrón práctico para integrar modelos de IA con datos reales mediante MCP, centrado en información hidrológica de Perú. La idea central es exponer solo las operaciones necesarias y mantener el acceso a la base de datos bajo control.

Es especialmente útil para:

- análisis guiado por IA sobre recursos hídricos
- consultas sobre datos del Perú y gestión del agua
- asistentes que requieren contexto real
- integración de modelos con sistemas de información hidrológica

Este README puede adaptarse fácilmente para incluir más ejemplos específicos de SQL, instrucciones para distintos clientes MCP o documentación adicional de despliegue.
