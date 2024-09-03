import streamlit as st
import pandas as pd
import requests
import zipfile
import io

# URL del archivo comprimido
zip_url_resultados = 'https://www.argentina.gob.ar/sites/default/files/2023_generales_1.zip'

# Descargar el archivo ZIP
response = requests.get(zip_url_resultados)
zip_file_resultados = zipfile.ZipFile(io.BytesIO(response.content))

# Listar los archivos dentro del ZIP
archivo_csv = '2023_Generales/ResultadoElectorales_2023_Generales.csv'

# Leer el archivo CSV en chunks
chunksize = 10**6  # Ajusta este tamaño según la capacidad de memoria disponible
chunks = []
for chunk in pd.read_csv(zip_file_resultados.open(archivo_csv), usecols=['distrito_nombre', 'circuito_id', 'cargo_nombre', 'agrupacion_nombre', 'votos_cantidad'], chunksize=chunksize, low_memory=False):
    # Filtrar cada chunk
    chunk_filtered = chunk[chunk['distrito_nombre'] == 'Buenos Aires']
    chunks.append(chunk_filtered)

# Concatenar todos los chunks
csv_df = pd.concat(chunks, ignore_index=True)

# Título de la aplicación
st.title('Resultados Electorales 2023')

# Mostrar los primeros datos para verificar la carga correcta
st.write('**Datos Cargados:**')
st.dataframe(csv_df.head())

# Agregar un selectbox para seleccionar el cargo
cargos = csv_df['cargo_nombre'].unique()
cargo_seleccionado = st.selectbox('Selecciona un Cargo:', cargos)

# Filtrar los datos según el cargo seleccionado
df_filtrado = csv_df[csv_df['cargo_nombre'] == cargo_seleccionado]

# Agregar un selectbox para seleccionar el circuito_id
circuitos = df_filtrado['circuito_id'].unique()
circuito_seleccionado = st.selectbox('Selecciona un Circuito ID:', circuitos)

# Filtrar los datos según el circuito seleccionado
df_filtrado = df_filtrado[df_filtrado['circuito_id'] == circuito_seleccionado]

# Agrupar por agrupacion_nombre y sumar votos_cantidad
df_resultado = df_filtrado.groupby('agrupacion_nombre')['votos_cantidad'].sum().reset_index()

# Mostrar la tabla resultante
st.write(f'**Resultados para el Cargo: {cargo_seleccionado} y Circuito ID: {circuito_seleccionado}**')
st.dataframe(df_resultado)

