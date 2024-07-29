import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def select_file():
    """Solicita al usuario que ingrese la ruta del archivo Excel."""
    file_path = input("Ingrese la ruta del archivo Excel (por ejemplo, C:/ruta/archivo.xlsx): ")
    if not os.path.isfile(file_path):
        print("Error: El archivo no existe.")
        return None
    return file_path

def process_data(file_path, sheet_name, col_range, start_row):
    """Procesa los datos del archivo Excel según los parámetros especificados."""
    try:
        start_row = int(start_row) - 1  # Ajustar para índice basado en 0

        # Verificar las hojas disponibles en el archivo
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names

        if sheet_name not in sheet_names:
            print(f"Error: La hoja '{sheet_name}' no se encuentra en el archivo.")
            return None

        # Leer el archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=col_range, skiprows=start_row)
        return df

    except ValueError:
        print("Error: El valor de la fila inicial debe ser un número entero.")
    except Exception as e:
        print(f"Error: Ocurrió un error durante el proceso: {str(e)}")
    return None

def show_dataframe(df):
    """Muestra el DataFrame en la consola."""
    print("\nDataset Final:")
    print(df)

def generate_pie_chart(df, column, max_data, file_path):
    """Genera y guarda un gráfico de torta basado en los datos del DataFrame."""
    if column not in df.columns:
        print(f"Error: La columna '{column}' no se encuentra en el DataFrame.")
        return

    # Manejo de valores no finitos para columnas categóricas
    if df[column].dtype == object:
        counts = df[column].dropna().value_counts()
    else:
        series = df[column].dropna()  # Eliminar NA
        series = series[series != float('inf')]  # Eliminar inf
        rounded_values = series.round().astype(int)
        counts = rounded_values.value_counts()

    # Limitar la cantidad de datos a graficar
    if len(counts) > max_data:
        counts = counts.head(max_data)

    # Crear la gráfica de torta
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
    plt.title(f'Distribución de {column}')
    plt.axis('equal')  # Igualar el aspecto para que sea un círculo

    # Guardar la gráfica
    output_folder = os.path.dirname(file_path)
    output_path = os.path.join(output_folder, f'distribucion_{column}.png')
    plt.savefig(output_path)
    plt.close()

    print(f"Gráfica de torta guardada en {output_path}")

def generate_bar_chart(df, column, max_data, file_path):
    """Genera y guarda un gráfico de barras basado en los datos del DataFrame."""
    if column not in df.columns:
        print(f"Error: La columna '{column}' no se encuentra en el DataFrame.")
        return

    # Manejo de valores no finitos para columnas categóricas
    if df[column].dtype == object:
        counts = df[column].dropna().value_counts()
    else:
        series = df[column].dropna()  # Eliminar NA
        series = series[series != float('inf')]  # Eliminar inf
        rounded_values = series.round().astype(int)
        counts = rounded_values.value_counts()

    # Limitar la cantidad de datos a graficar
    if len(counts) > max_data:
        counts = counts.head(max_data)

    # Crear la gráfica de barras
    plt.figure(figsize=(10, 6))
    plt.bar(counts.index, counts.values)
    plt.title(f'Frecuencia de Valores en {column}')
    plt.xlabel('Valores')
    plt.ylabel('Frecuencia')
    plt.grid(True, axis='y')

    # Guardar la gráfica
    output_folder = os.path.dirname(file_path)
    output_path = os.path.join(output_folder, f'frecuencia_{column}.png')
    plt.savefig(output_path)
    plt.close()

    print(f"Gráfica de barras guardada en {output_path}")

def main():
    """Función principal para ejecutar el proceso ETL desde la línea de comandos."""
    file_path = select_file()
    if file_path is None:
        return

    sheet_name = input("Ingrese el nombre de la hoja: ").strip()
    col_range = input("Ingrese el rango de columnas (ej. A:D): ").strip()
    start_row = input("Ingrese la fila inicial: ").strip()

    df = process_data(file_path, sheet_name, col_range, start_row)
    if df is not None:
        show_dataframe(df)

        chart_type = input("¿Qué tipo de gráfico desea generar? (1: Torta, 2: Barras): ").strip()
        column = input("Ingrese el nombre de la columna para graficar: ").strip()
        max_data = input("Ingrese la cantidad máxima de datos a graficar: ").strip()

        if not max_data.isdigit():
            print("Error: La cantidad máxima de datos debe ser un número entero.")
            return

        max_data = int(max_data)

        if chart_type == "1":
            generate_pie_chart(df, column, max_data, file_path)
        elif chart_type == "2":
            generate_bar_chart(df, column, max_data, file_path)
        else:
            print("Error: Opción de gráfico no válida.")

if __name__ == "__main__":
    main()
