import os
from config import *
import shutil

#run the code for each file in a folder

def manage_station_directory(station_name):
    current_file_parent_dir = os.path.dirname(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))
    output_dir = os.path.join(current_file_parent_dir, output_stations, station_name)
    #Crear subdirectory para la estación relativo!!!! por lo que se va a ejecutar en otras maquinas
    print (f"Output directory: {output_dir}")
    if os.path.exists(output_dir):
        # Remove all files and subdirectories in the output directory
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        os.makedirs(output_dir)

measurement_name = "El Paraiso [22]"
manage_station_directory(measurement_name)