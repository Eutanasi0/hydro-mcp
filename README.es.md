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
