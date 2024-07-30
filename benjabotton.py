import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO
import traceback

# Imprimir información de diagnóstico
st.write(f"Python version: {sys.version}")
st.write(f"Pandas version: {pd.__version__}")
st.write(f"Numpy version: {np.__version__}")
st.write(f"Matplotlib version: {plt.__version__}")

# Intentar importar openpyxl
try:
    import openpyxl
    st.write(f"Openpyxl version: {openpyxl.__version__}")
except ImportError as e:
    st.error(f"Error al importar openpyxl: {e}")
    st.error("Por favor, asegúrate de que openpyxl está instalado correctamente.")
    sys.exit(1)

def process_data(file_path, sheet_name, col_range, start_row):
    """Procesa los datos del archivo Excel según los parámetros especificados."""
    try:
        start_row = int(start_row) - 1  # Ajustar para índice basado en 0

        # Verificar las hojas disponibles en el archivo
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names

        if sheet_name not in sheet_names:
            st.error(f"Error: La hoja '{sheet_name}' no se encuentra en el archivo.")
            return None

        # Intentar leer el archivo Excel sin especificar el motor
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=col_range, skiprows=start_row)
        return df

    except Exception as e:
        st.error(f"Error detallado: {str(e)}")
        st.error(f"Traceback: {traceback.format_exc()}")
    return None

def generate_pie_chart(df, column, max_data):
    """Genera y muestra un gráfico de torta basado en los datos del DataFrame."""
    try:
        if column not in df.columns:
            st.error(f"Error: La columna '{column}' no se encuentra en el DataFrame.")
            return None

        series = df[column].dropna()
        if series.dtype == object:
            counts = series.value_counts().head(max_data)
        else:
            counts = pd.cut(series, bins=min(max_data, 10)).value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(counts, labels=counts.index.astype(str), autopct='%1.1f%%', startangle=140)
        ax.set_title(f'Distribución de {column}')
        plt.axis('equal')

        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)
        return buf

    except Exception as e:
        st.error(f"Error en generate_pie_chart: {str(e)}")
        st.error(f"Traceback: {traceback.format_exc()}")
        return None

def generate_bar_chart(df, column, max_data):
    """Genera y muestra un gráfico de barras basado en los datos del DataFrame."""
    try:
        if column not in df.columns:
            st.error(f"Error: La columna '{column}' no se encuentra en el DataFrame.")
            return None

        series = df[column].dropna()
        if series.dtype == object:
            counts = series.value_counts().head(max_data)
        else:
            counts = pd.cut(series, bins=min(max_data, 10)).value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(counts.index.astype(str), counts.values)
        ax.set_title(f'Frecuencia de Valores en {column}')
        ax.set_xlabel('Valores')
        ax.set_ylabel('Frecuencia')
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)
        return buf

    except Exception as e:
        st.error(f"Error en generate_bar_chart: {str(e)}")
        st.error(f"Traceback: {traceback.format_exc()}")
        return None

def main():
    """Función principal para ejecutar el proceso ETL usando Streamlit."""
    st.title("Procesador de Datos Excel")

    uploaded_file = st.file_uploader("Cargar archivo Excel", type=["xlsx", "xls", "ods"], key="excel_uploader")

    if uploaded_file is not None:
        sheet_name = st.text_input("Ingrese el nombre de la hoja", key="sheet_name_input")
        col_range = st.text_input("Ingrese el rango de columnas (ej. A:D)", key="col_range_input")
        start_row = st.text_input("Ingrese la fila inicial", key="start_row_input")

        if st.button("Procesar Datos", key="process_data_button"):
            df = process_data(uploaded_file, sheet_name, col_range, start_row)
            if df is not None:
                st.write("Dataset Final:")
                st.dataframe(df)

                chart_type = st.selectbox("¿Qué tipo de gráfico desea generar?", ["Torta", "Barras"], key="chart_type_select")
                column = st.text_input("Ingrese el nombre de la columna para graficar", key="column_input")
                max_data = st.number_input("Ingrese la cantidad máxima de datos a graficar", min_value=1, max_value=100, value=10, key="max_data_input")

                if st.button("Generar Gráfico", key="generate_chart_button"):
                    if column not in df.columns:
                        st.error(f"Error: La columna '{column}' no existe en el DataFrame.")
                    elif df[column].empty:
                        st.error(f"Error: La columna '{column}' está vacía.")
                    else:
                        chart_buf = None
                        if chart_type == "Torta":
                            chart_buf = generate_pie_chart(df, column, max_data)
                        elif chart_type == "Barras":
                            chart_buf = generate_bar_chart(df, column, max_data)
                        
                        if chart_buf:
                            st.image(chart_buf, caption=f'Gráfica de {chart_type} para {column}')
                        else:
                            st.error(f"No se pudo generar la gráfica de {chart_type} para la columna '{column}'.")
                        
                        st.write(f"Información de la columna '{column}':")
                        st.write(f"Tipo de datos: {df[column].dtype}")
                        st.write(f"Valores únicos: {df[column].nunique()}")
                        st.write(f"Muestra de datos: {df[column].head().tolist()}")

if __name__ == "__main__":
    main()