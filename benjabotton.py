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

def generate_pie_chart(df, column):
    """Genera y muestra un gráfico de torta basado en los datos del DataFrame."""
    if column not in df.columns:
        st.error(f"Error: La columna '{column}' no se encuentra en el DataFrame.")
        return None

    # Manejo de valores no finitos para columnas categóricas
    counts = df[column].dropna().value_counts()

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

def generate_bar_chart(df, column):
    """Genera y muestra un gráfico de barras basado en los datos del DataFrame."""
    if column not in df.columns:
        st.error(f"Error: La columna '{column}' no se encuentra en el DataFrame.")
        return None

    # Manejo de valores no finitos para columnas categóricas
    counts = df[column].dropna().value_counts()

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

            # Supongamos que las siguientes columnas están disponibles y son relevantes para graficar.
            columns_to_plot = ['Name', 'Country', 'Field of Expertise', 'IQ', 'Achievements', 'Birth Year', 'Gender', 'Notable Works', 'Awards', 'Education', 'Influence']

            for column in columns_to_plot:
                if column in df.columns:
                    st.subheader(f'Gráfico para la columna: {column}')
                    
                    if df[column].dtype == object:  # Si es una columna categórica
                        chart_buf = generate_pie_chart(df, column)
                    else:  # Si es una columna numérica
                        chart_buf = generate_bar_chart(df, column)

                    if chart_buf:
                        st.image(chart_buf, caption=f'Gráfica de {column}')
                else:
                    st.warning(f"La columna '{column}' no se encuentra en el DataFrame.")

if __name__ == "__main__":
    main()
