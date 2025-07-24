# Importando as bibliotecas necessárias
import pandas as pd
import plotly.express as px
import streamlit as st

# Gerando o dashboard
st.title('Análise de carros americanos')

# Carregando o Dataframe vehicles.csv
st.write('Data Used')
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

# Gerando o dashboard
st.title('Análise de carros americanos')

st.header('Histograma')
type_manufacturer = car_data.groupby(['manufacturer', 'type'])['days_listed'].count().reset_index()
fig_hist = px.histogram(type_manufacturer, x= 'manufacturer',y= 'days_listed', color= 'type', title= 'Vehicles types by Manufacturer')
st.plotly_chart(fig_hist)