# Importando as bibliotecas necessárias
import pandas as pd
import plotly.express as px
import streamlit as st

# Carregando o Dataframe vehicles.csv
car_data = pd.read_csv('vehicles.csv')

# Coluna model_year
car_data['model_year'] = car_data['model_year'].fillna(9999)
car_data['model_year'] = car_data['model_year'].astype(int)

# Coluna cylinders
car_data['cylinders'] = car_data['cylinders'].fillna(0)

# Coluna odometer
car_data['odometer'] = car_data['odometer'].fillna(car_data['odometer'].median()).astype(int)

# Coluna paint_color
car_data['paint_color'] = car_data['paint_color'].fillna('unknown')

# Coluna date_posted
car_data['date_posted'] = pd.to_datetime(car_data['date_posted'])

# Criando uma nova coluna manufacturer e modificando a coluna model
car_data['manufacturer'] = car_data['model'].str.split(' ').str[0]
car_data['model'] = car_data['model'].str.split(' ').str[1]

# Modificando a ordem das colunas
colunas = car_data.columns.tolist()
colunas.remove('manufacturer')
colunas.insert(2, 'manufacturer')
car_data = car_data[colunas]

# Gerando o dashboard. Área dos dados.
st.title('Análise de Carros Americanos')
st.header('Data Viewer')
st.subheader('Esses são os dados utilizados para fazer o dashboard')
st.dataframe(car_data)

# Tipos por fabricante
st.write('Selecione como você gostaria de ver os dados de tipos por fabricante')
tf_hist_chart = st.checkbox('Histograma')
tf_scatter_chart = st.checkbox('Dispersão')
type_manufacturer = car_data.groupby(['manufacturer', 'type'])['days_listed'].count().reset_index()

if tf_hist_chart:
    st.write('Criando um histograma para o conjunto de dados de anúncios de vendas de carros.')
    fig_hist = px.histogram(type_manufacturer, x= 'manufacturer', y= 'days_listed', color= 'type', title= 'Vehicles types by Manufacturer')
    st.plotly_chart(fig_hist)

if tf_scatter_chart:
    st.write('Criando um gráfico de disperção para o conjunto de dados de anúncios de vendas de carros.')
    fig_scatter = px.scatter(type_manufacturer, x= 'manufacturer', y= 'days_listed', color= 'type', title= 'vehicles types by manufacturer')
    st.plotly_chart(fig_scatter)