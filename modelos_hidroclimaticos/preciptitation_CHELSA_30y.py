import rioxarray
import geopandas as gpd
from shapely.geometry import mapping
import os
from config import *

if not os.path.exists(carpeta_salida_precip):
    os.makedirs(carpeta_salida_precip)

# --- 2. CARGAR POLÍGONO ---
poligono = gpd.read_file(ruta_shape)

# --- 3. DEFINIR PERIODO (30 AÑOS) ---
anio_fin = 2021
anio_inicio = anio_fin - 29  # Esto nos da 30 años exactos (1992-2021)

print(f"Iniciando descarga histórica de {anio_inicio} a {anio_fin}...")

# --- 4. BUCLE ANIDADO (AÑOS Y MESES) ---
for anio in range(anio_inicio, anio_fin + 1):
    for mes in range(1, 13):
        mes_str = str(mes).zfill(2)

        # Nombre único para cada archivo
        nombre_final = f"prec_azufral_{anio}_{mes_str}.tif"
        ruta_final = os.path.join(carpeta_salida_precip, nombre_final)

        # MECANISMO DE REINICIO: Si el archivo ya existe, saltar al siguiente
        if os.path.exists(ruta_final):
            # Opcional: imprimir solo algunos para no llenar la pantalla
            continue

        # URL de CHELSA (Nueva estructura confirmada)
        url = f"https://os.unil.cloud.switch.ch/chelsa02/chelsa/global/monthly/pr/{anio}/CHELSA_pr_{mes_str}_{anio}_V.2.1.tif"

        print(f"Descargando: {anio}-{mes_str}...")

        try:
            with rioxarray.open_rasterio(url, masked=True) as src:
                # Alinear coordenadas una sola vez o cuando cambie
                if poligono.crs != src.rio.crs:
                    poligono = poligono.to_crs(src.rio.crs)

                # Recortar al AOI
                recorte = src.rio.clip(poligono.geometry.apply(mapping), poligono.crs)

                # Guardar
                recorte.rio.to_raster(ruta_final)
                print(f"   ✅ Guardado: {nombre_final}")

        except Exception as e:
            print(f"   ⚠️ No se pudo obtener {anio}-{mes_str}. Error: {e}")
            # Si un año entero falla, es posible que no esté en esa carpeta (ej. años muy viejos)
            # pero para 1992-2021 la estructura suele ser estable.

print("\n🚀 ¡PROCESO FINALIZADO O COMPLETADO HASTA DONDE FUE POSIBLE!")
