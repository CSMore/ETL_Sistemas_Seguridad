# 🧩 ETL – Inventario POS

## 📘 Descripción general

Este pipeline integra y transforma datos de inventario provenientes de múltiples fuentes locales (archivos Excel y CSV), garantizando la **calidad, consistencia y unificación** de la información antes de su carga en la base de datos.

El objetivo principal es disponer de un **proceso automatizado** que permita consolidar los inventarios de los distintos puntos de venta (POS) en una sola fuente confiable.

---

## 📥 Extracción de datos

### Fuentes de entrada

Los datos provienen de diferentes archivos almacenados en el directorio `data/raw/`:

- `Inventario POS 1.xlsx`
- `Inventario POS 2.xlsx`
- `Inventario_3.csv`

El proceso detecta el tipo de archivo y aplica el método de lectura adecuado:

```python
for p in rutas:
    if p.endswith(".csv"):
        df = pd.read_csv(p, sep=",", encoding="utf-8-sig")
    elif p.endswith(".xlsx"):
        df = pd.read_excel(p)
    dfs.append(df)
```

Finalmente, todos los `DataFrames` se concatenan en uno solo para su posterior limpieza:

```python
df_final = pd.concat(dfs, ignore_index=True)
```

---

## 🧹 Limpieza y estandarización

### Reglas aplicadas

1. **Normalización de texto:**

   - Conversión a minúsculas.
   - Eliminación de acentos, caracteres especiales y espacios innecesarios.
   - Sustitución de valores nulos por cadenas vacías.

   ```python
   def limpiar_texto(txt):
       if pd.isna(txt):
           return ""
       txt = str(txt)
       txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("ascii")
       txt = re.sub(r"\s+", " ", txt).strip().lower()
       return txt
   ```
2. **Homogeneización de nombres de columnas:**

   - Todas las columnas se normalizan con nombres en minúsculas y sin espacios.
   - Se renombran campos críticos para mantener coherencia entre las fuentes.
3. **Eliminación de duplicados:**

   - Se eliminan registros repetidos según claves como `codigo_producto` o `descripcion`.
4. **Filtrado de registros vacíos:**

   - Se descartan filas donde faltan datos esenciales como `cantidad` o `precio_unitario`.
5. **Conversión de tipos de datos:**

   - Se asegura que los campos numéricos y de fecha tengan el formato correcto (`float`, `datetime`, etc.).

---

## ⚙️ Transformaciones adicionales

Durante la transformación, se realizan pasos clave para enriquecer el dataset:

- Cálculo de **campos derivados** (por ejemplo, `total_inventario = cantidad * precio_unitario`).
- Limpieza de **valores atípicos** (por ejemplo, precios negativos o cantidades fuera de rango).
- Reordenamiento de columnas para mantener una estructura lógica.

Ejemplo:

```python
df_final["total_inventario"] = df_final["cantidad"] * df_final["precio_unitario"]
df_final = df_final[df_final["cantidad"] > 0]
```

Estas reglas aseguran que los datos cargados sean **coherentes, comparables y analíticamente útiles**.

---

## 💾 Carga de datos

### Método: **Upsert (inserción o actualización masiva)**

La función `bulk_upsert_inventario()` realiza una **carga masiva con detección de duplicados**.
Esto significa que si un registro ya existe en la base de datos, se actualiza; si no, se inserta.

```python
from etl.db import bulk_upsert_inventario
bulk_upsert_inventario(df_final)
```

#### Justificación del método:

- **Eficiencia:** se insertan o actualizan miles de registros en bloque, reduciendo tiempos de ejecución.
- **Consistencia:** evita duplicar inventarios previamente cargados.
- **Escalabilidad:** permite ejecutar el pipeline de forma periódica sin limpiar la tabla completa.

---

## 🧠 Registro y manejo de errores

- Se usa `logger_setup.py` para capturar eventos, errores y tiempos de ejecución.
- Los errores en lectura o carga se manejan con bloques `try-except`, registrando el detalle en el log.
- Esto permite monitorear el pipeline y detectar problemas sin interrumpir la ejecución.

---

## 🗂️ Estructura del proyecto

```
ETL_Sistemas_Seguridad/
│
├── data/
│   ├── raw/                # Archivos de entrada
│   └── processed/          # Archivos limpios o transformados
│
├── etl/
│   ├── logger_setup.py     # Configuración de logs
│   ├── db.py               # Conexión y operaciones con la base de datos
│   └── etl_inventario.py   # Lógica principal del pipeline
│
├── main.py                 # Script de ejecución del ETL
└── README.md               # Documentación del pipeline
```

---

## 🔐 Variables de entorno (.env)

Las credenciales de la base de datos se gestionan mediante un archivo **`.env`** (no se versiona) para mantener la seguridad.

Para ello se debe crear un archivo .env en la raíz del proyecto con el siguiente contenido y reemplazando los valores por los correspondientes a la conexión real con la base de datos:

```
DB_HOST=localhost
DB_NAME=dw_inventory
DB_USER=etl_user
DB_PASSWORD=CHANGE_ME

```


---



## 🚀 Ejecución

1. Activar entorno virtual (si aplica):

   ```bash
   .venv\Scripts\activate     # En Windows
   source .venv/bin/activate  # En Linux/Mac
   ```
2. Ejecutar el script principal:

   ```bash
   python -m  etl.pipeline
   ```
3. Verificar los logs en la carpeta `logs/` para confirmar la correcta ejecución del proceso.

---

## 📊 Diagrama de flujo del pipeline

```mermaid
flowchart TD
    A[Extracción de múltiples fuentes<br>(Excel, CSV)] --> B[Limpieza de texto y columnas]
    B --> C[Transformaciones<br>(cálculos, tipos, filtros)]
    C --> D[Unificación de DataFrames]
    D --> E[Validación de calidad de datos]
    E --> F[Upsert en base de datos]
    F --> G[Logs y monitoreo de errores]
```

---

## ❓ Soporte y guía adicional

En caso de tener dudas sobre cómo ejecutar correctamente el pipeline, refiérase al siguiente documento con las instrucciones detalladas:

👉 [Guía oficial para correr el pipeline y la base de datos (PDF)](https://github.com/KrisSo03/ETL_Sistemas_Seguridad/blob/aff5f7c0229186f95e516249f0c353d94b0ef94f/etl/Proyecto%20-%20Intrucciones%20para%20correr%20pipeline%20y%20BD.pdf)

Este documento explica paso a paso la configuración del entorno, la conexión a la base de datos y la ejecución completa del proceso ETL.

---

## 🧾 Autoría

**Proyecto ETL de Inventario POS**
Versión 1.0 — Noviembre 2025
