# Imagen optimizada para geociencias (trae GDAL, PROJ, GEOS instalados)
FROM pangeo/pangeo-notebook:latest

# Directorio de trabajo en el contenedor
WORKDIR /app

# Creamos las carpetas necesarias
RUN mkdir -p /app/data/shapefiles
RUN mkdir -p /app/data/results/modelos_hidroclimaticos/database/temperatura

# Copiamos los archivos de requerimientos primero para aprovechar la cache
COPY requirements.txt .

# Instalamos las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código y el archivo config.py
COPY . .

# Variable para que Python no guarde buffer y veas los prints en tiempo real
ENV PYTHONUNBUFFERED=1

# Ajuste Crítico: Agregar la subcarpeta al path de Python
ENV PYTHONPATH="${PYTHONPATH}:/app/modelos_hidroclimaticos"

# Comando para ejecutar el script
CMD ["python", "modelos_hidroclimaticos/temperature_CHELSA_30.py"]