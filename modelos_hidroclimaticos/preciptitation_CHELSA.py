import rioxarray
import geopandas as gpd
from shapely.geometry import mapping
import os
from config import *

if not os.path.exists(carpeta_salida_precip):
    os.makedirs(carpeta_salida_precip)

# --- 2. CARGAR TU POLÍGONO ---
poligono = gpd.read_file(ruta_shape)
print("✅ Polígono del Azufral cargado.")

# --- 3. BUCLE DE DESCARGA (NUEVA RUTA UNIL 2020) ---
for mes in range(1, 13):
    mes_str = str(mes).zfill(2)

    # URL EXACTA basada en tu descubrimiento:
    # Nota que el mes va antes que el año en el nombre del archivo: pr_01_2020
    url = f"https://os.unil.cloud.switch.ch/chelsa02/chelsa/global/monthly/pr/2020/CHELSA_pr_{mes_str}_2020_V.2.1.tif"

    print(f"Intentando descargar Mes {mes_str}...")

    try:
        # Abrir el raster remoto
        with rioxarray.open_rasterio(url, masked=True) as src:
            # Alinear coordenadas si es necesario
            if poligono.crs != src.rio.crs:
                poligono = poligono.to_crs(src.rio.crs)

            # Recortar al área de interés
            recorte = src.rio.clip(poligono.geometry.apply(mapping), poligono.crs)

            # Guardar en tu PC
            nombre_final = f"precipitacion_azufral_2020_{mes_str}.tif"
            ruta_final = os.path.join(carpeta_salida_precip, nombre_final)
            recorte.rio.to_raster(ruta_final)

            print(f"   ✅ ¡Éxito! Guardado: {nombre_final}")

    except Exception as e:
        print(f"   ❌ Falló Mes {mes_str}. Error: {e}")

print("\n🚀 ¡PROCESO COMPLETADO! Ya puedes ver los 12 meses en tu carpeta.")
