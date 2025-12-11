file_name = r"C:\Code\TIP\Balance_hidrico\input\estaciones_ideam\Est. Barbascal.xlsx"
output_stations = r"results\estaciones"
input_stations = r"input\estaciones_ideam"
sheet_name = "Data"
# Minimum number of months per year with data to keep a station
min_months_per_year = 4
months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
z_score_threshold = 1.65

variable_labels = {
    "PRECIPITACION": "Precipitación [mm]",
    "TEMPERATURA": "degC",
    "BRILLO SOLAR": "Horas/sol",
    "CAUDAL": "Caudal [m3/s]",
    "DIR VIENTO": "Sector",
    "VEL VIENTO": "Velocidad [m/s]",
}
