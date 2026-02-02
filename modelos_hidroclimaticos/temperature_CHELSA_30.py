import rioxarray
import geopandas as gpd
from shapely.geometry import mapping
import os
from config import *


if not os.path.exists(carpeta_salida_temper):
    os.makedirs(carpeta_salida_temper)

# --- 2. CARGAR POLÍGONO ---
poligono = gpd.read_file(ruta_shape)

# --- 3. DEFINIR PERIODO ---
anio_fin = 2021
anio_inicio = anio_fin - 29

print(f"Iniciando descarga de TEMPERATURA de {anio_inicio} a {anio_fin}...")

# --- 4. BUCLE DE DESCARGA ---
for anio in range(anio_inicio, anio_fin + 1):
    for mes in range(1, 13):
        mes_str = str(mes).zfill(2)

        nombre_final = f"temp_azufral_{anio}_{mes_str}.tif"
        ruta_final = os.path.join(carpeta_salida_temper, nombre_final)

        # MECANISMO DE REINICIO
        if os.path.exists(ruta_final):
            print(f"   ⏭️ Ya existe {nombre_final}, saltando...")
            continue

        # URL de CHELSA para Temperatura (tas)
        url = f"https://os.unil.cloud.switch.ch/chelsa02/chelsa/global/monthly/tas/{anio}/CHELSA_tas_{mes_str}_{anio}_V.2.1.tif"

        print(f"Descargando Temperatura: {anio}-{mes_str}...")

        try:
            with rioxarray.open_rasterio(url, masked=True) as src:
                if poligono.crs != src.rio.crs:
                    poligono = poligono.to_crs(src.rio.crs)

                # Recortar
                recorte = src.rio.clip(poligono.geometry.apply(mapping), poligono.crs)

                # 2. CONVERSIÓN CORRECTA
                # CHELSA tas: (valor_crudo * 0.1) - 273.15
                # Forzamos a float para asegurar precisión decimal
                recorte_celsius = (recorte.astype(float) * 0.1) - 273.15

                # 3. LIMPIEZA DE METADATOS (Fundamental)
                # Eliminamos escalas y offsets previos para que el software GIS no los reaplique
                recorte_celsius.attrs["scale_factor"] = 1.0
                recorte_celsius.attrs["add_offset"] = 0.0
                recorte_celsius.rio.write_nodata(-9999, inplace=True)

                # 4. Guardar como float32
                recorte_celsius.rio.to_raster(
                    ruta_final, dtype="float32", driver="GTiff"
                )
                print(f"   ✅ Guardado: {nombre_final} (°C)")

        except Exception as e:
            print(f"   ⚠️ Falló {anio}-{mes_str}. Error: {e}")

print("\n🚀 ¡PROCESO DE TEMPERATURA FINALIZADO!")
