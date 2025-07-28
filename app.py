# Importando as bibliotecas necessárias
import pandas as pd
import plotly.express as px
import streamlit as st

# Carregando o Dataframe vehicles.csv
car_data = pd.read_csv('vehicles.csv')

# Coluna odometer
car_data['odometer'] = car_data['odometer'].fillna(car_data['odometer'].median())
car_data['odometer'] = car_data['odometer'].astype(int)

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
# Área dos dados.
st.title('Dados de Carros Americanos')
st.header('Visualização dos dados')
st.subheader('Carros Americanos')
st.dataframe(car_data)

# Quantidade de carros tipos por fabricante Histograma. GRAFICO 1
st.header('Tipos de carros por fabricantes')
hist_chart = st.button('Histograma')
type_manufacturer = car_data.groupby(['manufacturer', 'type'])['days_listed'].count().reset_index()

if hist_chart:
    st.write('Histograma quantidade de carros por fabricantes')
    fig_hist = px.histogram(type_manufacturer,
                            x='manufacturer',
                            y='days_listed',
                            color='type',
                            labels={'manufacturer': 'Fabricantes', 'sum of days_listed': 'Quantidade'})
    st.plotly_chart(fig_hist)

# Distribuição da Condição dos carros por ano
st.header('Distribuição da condição dos carros por ano')
scatter_chart = st.button('Dispersão')

if scatter_chart:
    st.write('Criando um gráfico de condição dos carros por ano')
    fig_scatter = px.scatter(car_data,
                            x='model_year',
                            y='price',
                            color='condition',
                            labels={'model_year': 'Ano do modelo', 'price': 'Valor'})
    st.plotly_chart(fig_scatter)

# Gerando uma checkbox para análise de tipos de combustíveis
st.header('Tipos de combustíveis')
st.write('Como gostaria de ver os dados: ')
fuel_hist = st.checkbox('Histograma')
fuel_hist_group = car_data.groupby(['fuel', 'type'])['manufacturer'].count().reset_index()
fuel_scatt = st.checkbox('Distribuição')

# Gerando os gráfico de acordo com a escolha
if fuel_hist:
    st.write('Criando um histograma')
    fig_fuel_hist = px.histogram(fuel_hist_group,
                                x='fuel',
                                y='manufacturer',
                                color='type',
                                histnorm='count',
                                title='histograma dos combustíveis',
                                labels={'fuel': 'Combustível', 'manufacturer': 'Fabricante'})
    st.plotly_chart(fig_fuel_hist)

if fuel_scatt:
    st.write('Criando um gráfico de distribuição')
    fig_fuel_scatt = px.scatter(car_data,
                                x='manufacturer',
                                y='price',
                                color='fuel',
                                title='Distribuição dos combustíveis',
                                labels={'manufacturer': 'Fabricante', 'price': 'Valor'})
    st.plotly_chart(fig_fuel_scatt)

# Comparação da distribuição de preços
st.header('Escolha dois fabricantes e compare seus preços')
fabricante_1 = car_data['manufacturer'].unique().tolist()

# Gerando a primeira escolha de fabricante
choice_1 = st.selectbox('Selecione um fabricante: ', options=fabricante_1)

# Excluindo a primeira opção da lista para segunda seleção
fabricante_2 = [car for car in fabricante_1 if car != choice_1]

# Gerando um segunda escolha de fabricante
choice_2 = st.selectbox('Selecione outro fabricante: ', options=fabricante_2)

# Filtragem dos dados selecionados
car_data_fab1 = car_data[car_data['manufacturer'] == choice_1]
car_data_fab2 = car_data[car_data['manufacturer'] == choice_2]

# Concatenação dos dados para gerar o gráfico
car_data_2 = pd.concat([car_data_fab1, car_data_fab2])

# Gerando um histograma baseado nas opções
st.write('Criando um Histograma baseado nas fabricantes selecionadas')
fig_choices = px.histogram(car_data_2,
                        x='price',
                        color='manufacturer',
                        histnorm='percent',
                        labels={'price': 'Valor', 'percent': 'Porcentagem'})
st.plotly_chart(fig_choices)
