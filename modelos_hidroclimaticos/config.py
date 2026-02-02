import os
from pathlib import Path


os.environ["GDAL_NUM_THREADS"] = "1"  # Fuerza a usar solo 1 hilo
os.environ["OMP_NUM_THREADS"] = "1"

# 1. Detectar si estamos en Docker o Local
# Si la variable de entorno no existe, devolvemos 'LOCAL'
ENTORNO = os.getenv("APP_ENV", "LOCAL")

# 2. Definir la raíz del proyecto dinámicamente
# Path(__file__).parent.parent obtiene la carpeta raíz desde la subcarpeta 'scripts'
BASE_DIR = Path(__file__).resolve().parent.parent.parent


if ENTORNO == "TEST":
    # Rutas dentro del contenedor (Linux style)
    ruta_shape = "/app/data/shapefiles/area_estudio.shp"
    carpeta_salida_temper = (
        "/app/data/results/modelos_hidroclimaticos/database/temperatura"
    )

else:
    # Rutas en tu PC (Windows style)
    # Usamos .resolve() para que Python gestione las letras de unidad (C:, D:)
    ruta_shape = BASE_DIR / "input" / "shapefiles" / "area_estudio.shp"
    carpeta_salida_temper = (
        BASE_DIR / "results" / "modelos_hidroclimaticos" / "database" / "temperatura"
    )

    if not os.path.exists(carpeta_salida_temper):
        os.makedirs(carpeta_salida_temper)

# Convertir a string para evitar errores con librerías viejas
ruta_shape = str(ruta_shape)
carpeta_salida_temper = str(carpeta_salida_temper)
