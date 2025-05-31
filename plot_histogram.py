import numpy as np
import matplotlib.pyplot as plt
from config import *

def plot_multiyear_monthly_histogram(
        df, 
        title, 
        y_tag,
        output_path
        ):
    """
    Plots a histogram of multiyear monthly data with standard deviation lines on each bar.
    
    Parameters:
        df (pd.DataFrame): DataFrame with first column as year, next 12 columns as monthly data.
        title (str): Title of the plot.
    """
    # Spanish month abbreviations
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
             'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    # Extract only the monthly data (assume first column is year)
    monthly_data = df.iloc[:, 1:13]
    
    # Calculate mean and std for each month
    means = monthly_data.mean(axis=0)
    stds = monthly_data.std(axis=0)
    
    x = np.arange(12)
    
    fig, ax = plt.subplots(figsize=(10,6))
    bars = ax.bar(x, means, yerr=stds, capsize=5, color='skyblue', edgecolor='black')
    
    ax.set_xticks(x)
    ax.set_xticklabels(meses)
    ax.set_ylabel(y_tag)
    ax.set_title(title)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    fig.savefig(output_path)
    
    plt.tight_layout()
    plt.show()

# Ejemplo de uso:
# df = pd.read_csv('tu_archivo.csv')
# plot_multiyear_monthly_histogram(df, "Histograma Mensual Multianual")
