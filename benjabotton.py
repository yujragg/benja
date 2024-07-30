import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from io import BytesIO

# Configuración de Streamlit
st.title('Análisis de Datos Académicos')

# Cargar el archivo Excel usando el cargador de archivos de Streamlit
archivo_excel = st.file_uploader("Sube tu archivo Excel", type="xlsx")

if archivo_excel:
    try:
        # Cargar los datos
        data = pd.read_excel(archivo_excel)

        # Mostrar las primeras filas del dataset
        st.write(data.head())

        # Verificar las columnas del DataFrame
        if 'IQ' not in data.columns or 'Country' not in data.columns:
            st.error("El archivo debe contener las columnas 'IQ' y 'Country'.")
        else:
            # Función para graficar y mostrar gráficos en Streamlit
            def plot_and_show(data, x, y, title, xlabel, ylabel, plot_type='line', color='blue'):
                plt.figure(figsize=(10, 6))
                if plot_type == 'line':
                    sns.lineplot(x=x, y=y, data=data, color=color)
                elif plot_type == 'bar':
                    sns.barplot(x=x, y=y, data=data, color=color)
                plt.title(title)
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)
                plt.grid(True)
                st.pyplot(plt.gcf())
                plt.close()

            # Visualización de datos generales
            st.subheader('Distribución del IQ por País')
            plot_and_show(data, 'Country', 'IQ', 'Distribución del IQ por País', 'País', 'IQ', 'bar', 'skyblue')

            st.subheader('IQ de las Personalidades Académicas')
            plot_and_show(data, 'Name', 'IQ', 'IQ de las Personalidades Académicas', 'Nombre', 'IQ', 'bar', 'lightgreen')

            # Seleccionar una persona para el análisis de regresión lineal
            nombres = data['Name'].unique()
            nombre_seleccionado = st.selectbox("Selecciona una persona", nombres)

            # Filtrar datos para la persona seleccionada
            data_persona = data[data['Name'] == nombre_seleccionado]

            if not data_persona.empty:
                # Realizar la regresión lineal
                X = data_persona[['Birth Year']].values
                y = data_persona['IQ'].values

                # Ajustar modelo de regresión lineal
                model = LinearRegression()
                model.fit(X, y)
                predictions = model.predict(X)
                r2 = r2_score(y, predictions)

                # Graficar la regresión lineal
                plt.figure(figsize=(10, 6))
                sns.scatterplot(x='Birth Year', y='IQ', data=data_persona, color='blue')
                sns.lineplot(x=data_persona['Birth Year'], y=predictions, color='red')
                plt.title(f'Regresión Lineal: IQ de {nombre_seleccionado}')
                plt.xlabel('Año de Nacimiento')
                plt.ylabel('IQ')
                plt.grid(True)
                st.pyplot(plt.gcf())
                plt.close()

                # Mostrar el valor de R²
                st.write(f'Precisión de la regresión lineal (R²) para {nombre_seleccionado}: {r2:.2f}')
            else:
                st.warning("No hay suficientes datos para realizar la regresión lineal.")

    except pd.errors.EmptyDataError:
        st.error("El archivo está vacío. Por favor, verifique el contenido del archivo.")
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
else:
    st.info("Por favor, sube un archivo Excel para comenzar.")
