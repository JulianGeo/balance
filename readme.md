# Format Ideam
El script de formatear los datos del ideam genera 3 excels con datos:
* raw: solo datos, solamente organizados
* z_scores: los z scores de los datos
* cleaned: raw quitando los z_scores

# Hidroquímica
Este folder contiene funcionalidades:

## Preprocesamiento hidroquímico
* Cálculo de balances iónicos
* Generación de stats básicos [en proceso]

## PCA análysis
* Cálculo de PC y generación de plots básicos y dendográmas para visualizar resultados

## Creación de plots básicos
* Histográmas



# Mixing regression
Realiza la solución de un par de ecuaciones lineales para encontrar las fracciones de mezcla de dos endmembers dada la concentración de los dos endmembers y la de la mezcla.

Está automatizado para considerar y realizar iteraciones con varias muestras del mismo punto.