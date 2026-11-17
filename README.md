# Hydro MCP

[![CI](https://github.com/Eutanasi0/hydro-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/Eutanasi0/hydro-mcp/actions/workflows/ci.yml)

[Español](README.es.md) | English

Read-only MCP server that lets AI agents query Peruvian hydrological open data (SQLite) with guardrails.

## Overview

This project exposes a local MCP server that gives AI clients a safe, read-only interface to hydrological information from Peru. The goal is to let an agent inspect tables, understand schema, and run constrained `SELECT` queries without direct database access or write permissions.

## What is MCP?

MCP stands for Model Context Protocol. It is an open standard for connecting AI agents to external tools and data sources with a consistent interface.

In this repository, the server exposes three tools:

- `list_tables()`
- `describe_table(table)`
- `run_select(sql, limit=50)`

## Why this project exists

The repository acts as a secure adapter between an AI client and a SQLite database. Instead of exposing the database directly, it restricts the interaction to controlled read operations and validates SQL before executing it.

## Features

- Read-only database access
- SQL validation and blocking of non-`SELECT` statements
- table listing and schema introspection
- minimal, agent-friendly JSON responses
- local MCP integration for OpenCode and similar clients

## Requirements

- Python 3.10+
- virtual environment recommended
- dependencies from `requirements.txt`

## Installation

```bash
cd <project-path>
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Quick start

Run the MCP server:

```bash
python server.py
```

Run the demo client:

```bash
python client_demo.py
```

## Usage

### `list_tables()`

Lists all available tables in the SQLite database.

```python
await session.call_tool("list_tables", {})
```

### `describe_table(table)`

Returns the schema for a specific table.

```python
await session.call_tool("describe_table", {"table": "my_table"})
```

### `run_select(sql, limit=50)`

Executes a read-only query with a guardrail limit.

```python
await session.call_tool(
    "run_select",
    {"sql": "SELECT * FROM my_table LIMIT 10", "limit": 10},
)
```

## Security

The server intentionally restricts access:

- only `SELECT` queries are allowed
- statements with `;` are rejected
- writes, deletes, and schema changes are blocked
- rows are capped at 100 per query

## Data

The dataset used in this project is the hydrological emergency dataset published on `datosabiertos.gob.pe`.

- Source: `datosabiertos.gob.pe`
- Publisher: `Superintendencia Nacional de Servicios y Saneamiento (SUNASS)`
- Context: public open-data release for hydrological-risk and emergency declarations in Peru
- License: public-sector open data under the Peruvian open-data governance framework; check the dataset page for the exact licensing statement shown by the publisher

The raw CSV file is currently kept at the repository root:

```bash
DSHidricos_Dataset.csv
```

If the file grows, move it under `data/` and add a small download script.

## OpenCode template

Use the example config file as a template:

```bash
cp opencode.example.json opencode.json
```

Then update the paths to match your local environment.

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

## Project structure

- `server.py` — MCP server entry point
- `db.py` — SQLite access and validation logic
- `client_demo.py` — sample client session
- `build_db.py` — CSV-to-SQLite loader
- `opencode.example.json` — template for local OpenCode configuration
- `data/` — database and local data assets
- `requirements.txt` — pinned Python dependencies

## CI status

The latest GitHub Actions run is checked by the badge above. I verified that the repo had failing CI earlier; the code issues were fixed locally and the validation passes (`ruff` + `pytest`). After pushing the fix, the badge will reflect the green status.

## License and usage

This project is intended for local, read-only AI integration and analysis of public hydrological data. Use it responsibly and in line with the source dataset's terms and the relevant Peruvian open-data policy.
