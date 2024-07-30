import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO

def process_data(file):
    """Procesa los datos del archivo Excel automáticamente usando la primera hoja."""
    try:
        # Leer el archivo Excel usando openpyxl
        df = pd.read_excel(file, engine='openpyxl')
        return df

    except Exception as e:
        st.error(f"Error: Ocurrió un error durante el proceso: {str(e)}")
    return None

def generate_pie_chart(df, column, max_data):
    """Genera y muestra un gráfico de torta basado en los datos del DataFrame."""
    if column not in df.columns:
        st.error(f"Error: La columna '{column}' no se encuentra en el DataFrame.")
        return None

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
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
    ax.set_title(f'Distribución de {column}')
    plt.axis('equal')  # Igualar el aspecto para que sea un círculo

    # Guardar la gráfica en un buffer y retornar la imagen
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf

def generate_bar_chart(df, column, max_data):
    """Genera y muestra un gráfico de barras basado en los datos del DataFrame."""
    if column not in df.columns:
        st.error(f"Error: La columna '{column}' no se encuentra en el DataFrame.")
        return None

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

    # Crear la gráfica de barra
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(counts.index, counts.values)
    ax.set_title(f'Frecuencia de Valores en {column}')
    ax.set_xlabel('Valores')
    ax.set_ylabel('Frecuencia')
    ax.grid(True, axis='y')

    # Guardar la gráfica en un buffer y retornar la imagen
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf

def main():
    """Función principal para ejecutar el proceso ETL usando Streamlit."""
    st.title("Procesador de Datos Excel")

    uploaded_file = st.file_uploader("Cargar archivo Excel", type=["xlsx"], key="excel_uploader")

    if uploaded_file is not None:
        df = process_data(uploaded_file)
        if df is not None:
            st.write("Dataset Final:")
            st.dataframe(df)

            chart_type = st.selectbox("¿Qué tipo de gráfico desea generar?", ["Torta", "Barras"], key="chart_type_select")
            column = st.text_input("Ingrese el nombre de la columna para graficar", key="column_input")
            max_data = st.number_input("Ingrese la cantidad máxima de datos a graficar", min_value=1, max_value=100, value=10, key="max_data_input")

            if st.button("Generar Gráfico", key="generate_chart_button"):
                if chart_type == "Torta":
                    chart_buf = generate_pie_chart(df, column, max_data)
                    if chart_buf:
                        st.image(chart_buf, caption=f'Gráfica de Torta para {column}')
                elif chart_type == "Barras":
                    chart_buf = generate_bar_chart(df, column, max_data)
                    if chart_buf:
                        st.image(chart_buf, caption=f'Gráfica de Barras para {column}')

if __name__ == "__main__":
    main()
