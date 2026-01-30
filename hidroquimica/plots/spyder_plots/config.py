excel_file_path = r"C:\Code\TIP\Balance_hidrico\input\hidroquimica\TablaShape.xlsx"
data_sheet_name = "Termales"
output_plots_path = r"C:\Code\TIP\Balance_hidrico\results\hidroquimica\plots"
output_plots_clustering_path = output_plots_path + r"\clustering"

complejo_volcanico_column_name = "Complejo Volcánico "
complejo_volcanico_name = "Azufral"
not_null_columns = ["pH", "Temperatura (°C)"]

spyder_variables = {
    "ID": "MUESTRA",
    "pH": "pH",
    "Coliformes": "Coliformes totales",
    "As": "Arsénico",
    "NO3": "Nitratos",
    "Pb": "Plomo",
    "Cd": "Cadmio",
    "SO4": "Sulfatos",
}

max_spyder_values = {
    "ID": "Max",
    "pH": 9,
    "Coliformes": 1000,
    "As": 0.2,
    "NO3": 10,
    "Pb": 0.05,
    "Cd": 0.01,
    "SO4": 400,
}


# Molecular weights of cations and anions
iones = {
    "HCO3": 61,
    "CO3": 30,
    "Cl": 35,
    "SO4": 48,
    "Na": 23,
    "Ca": 20,
    "Mg": 12,
    "K": 39,
}
