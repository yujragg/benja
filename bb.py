import pandas as pd
import numpy as np
import random

# Configuración para la generación de datos aleatorios
np.random.seed(0)  # Para reproducibilidad
random.seed(0)     # Para reproducibilidad

# Número de registros
num_records = 50

# Listas de nombres y apellidos ficticios para generar nombres aleatorios
first_names = ['Ana', 'Luis', 'Carlos', 'Maria', 'Jorge', 'Laura', 'Pedro', 'Sofia', 'Juan', 'Marta',
               'Alejandro', 'Isabel', 'Miguel', 'Paola', 'Antonio', 'Gabriela', 'Daniel', 'Carmen', 'Rafael', 'Elena']
last_names = ['García', 'Martínez', 'López', 'Hernández', 'González', 'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Vázquez']

# Generación de nombres aleatorios combinando nombres y apellidos
def generate_names(num):
    names = []
    for _ in range(num):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        names.append(f'{first_name} {last_name}')
    return names

# Generación de notas aleatorias entre 0 y 10
def generate_grades(num):
    return np.random.randint(0, 11, size=num)

# Crear el DataFrame
data = {
    'Nombre': generate_names(num_records),
    'Matemáticas': generate_grades(num_records),
    'Lenguaje': generate_grades(num_records),
    'Inglés': generate_grades(num_records),
    'Sociales': generate_grades(num_records),
    'Artes': generate_grades(num_records)
}

df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo Excel
output_file = 'datos_estudiantes.xlsx'
df.to_excel(output_file, index=False)

print(f"Archivo '{output_file}' creado exitosamente.")
