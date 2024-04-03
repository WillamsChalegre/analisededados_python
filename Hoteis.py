# Importando as bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Acessando o dataset
df = pd.read_csv('C:/Users/User/Desktop/Analises de Dados/_Dataset/Hotel.Dataset.csv', encoding='latin1')
df

# Analisando as informações e tipos das colunas
df.info()

# Retirando os espaços que continha no titulos das colunas
df.columns = df.columns.str.replace(' ', '')
df.info()

# Analisando os dados da coluna HotelRating
df['HotelRating'].unique()

# Criando a coluna de StarRating
# Função para criação da coluna
def mapeando_stars (value):
    if value == 'OneStar':
        return 1
    elif value == 'TwoStar':
        return 2
    elif value == 'ThreeStar':
        return 3
    elif value == 'FourStar':
        return 4
    elif value == 'FiveStar':
        return 5
    elif value == 'All':
        return 5
    else:
        return None
    
# Criando a coluna
df['StarRating'] = df['HotelRating'].apply(lambda x: mapeando_stars(x))
df.info()


# ANALISE DO STAR RATING

# Contando o total de hóteis
df['HotelCode'].nunique()

# Mantendo os dados unicos de HotelCode
qtdHoteis = df.drop_duplicates(subset=['HotelCode'])
qtdHoteis['HotelCode'].count()


# Contando quantidade de hoteis por starRating
qtdHoteis['StarRating'].value_counts()

# Descobrindo a média e mediana de starRating
media_star = round(qtdHoteis['StarRating'].mean(),2)
media_star
mediana_star = round(qtdHoteis['StarRating'].median(),2)
mediana_star

# Adicionando numa variavel a quantidade de hoteis por starRating
hotelStar = qtdHoteis['StarRating'].value_counts().sort_index()
mediaHotelStar = hotelStar.mean()
medianaHotelStar = hotelStar.median()

# CRIANDO O PRIMEIRO GRÁFICO RELACIONADO A QUANTIADDE DE HOTEIS POR STAR RATING
# Mapeando as cores para o gráfico de barra
mapeando_cores = {
    1: '#FF6347', # Red
    2: '#FF6347', # Red
    3: '#FFD700', # Yellow
    4: '#32CD32', # Green
    5: '#32CD32', # Green
}
cores = [mapeando_cores[star] for star in hotelStar.index]


plt.figure(figsize=(9, 5))
plt.bar(hotelStar.index, hotelStar.values, color=cores)

# Adiconando os labels no topo das barras
for x, y in zip(hotelStar.index, hotelStar.values):
    plt.text(x, y, str(y), ha='center', va='bottom')
    
plt.axhline(y=medianaHotelStar, color='gray', linestyle='--')    
#plt.axhline(y=mediaHotelStar, color='red', linestyle='--')  
plt.xlabel('StarRating')
plt.ylabel('QtdHotéis')
plt.title('Quantidade de Hoteis por Star Rating')
plt.tight_layout()


# ANALISE DOS TOP 5 DOS PAISES POR STAR RATING

# Ranking dos 5 paises que contem mais hotéis no Dataset
qtdHoteis['countyName'].value_counts().sort_values(ascending=False).head(5)

# Ranking dos 5 Paises que tem mais Hóteis 5 estrelas
rkStar5 = qtdHoteis[qtdHoteis['StarRating']==5].groupby('countyName').size().sort_values(ascending=False).head(5)

# Ranking dos 5 Paises que tem mais Hóteis 4 estrelas
rkStar4 = qtdHoteis[qtdHoteis['StarRating']==4].groupby('countyName').size().sort_values(ascending=False).head(5)

# Ranking dos 5 Paises que tem mais Hóteis 3 estrelas
rkStar3 = qtdHoteis[qtdHoteis['StarRating']==3].groupby('countyName').size().sort_values(ascending=False).head(5)

# Ranking dos 5 Paises que tem mais Hóteis 2 estrelas
rkStar2 = qtdHoteis[qtdHoteis['StarRating']==2].groupby('countyName').size().sort_values(ascending=False).head(5)

# Ranking dos 5 Paises que tem mais Hóteis 1 estrelas
rkStar1 = qtdHoteis[qtdHoteis['StarRating']==1].groupby('countyName').size().sort_values(ascending=False).head(5)

# Criando uam tabela com StarRating 
rkCountryStar = pd.DataFrame(qtdHoteis, columns=['StarRating'])
# Retirando os valores duplicados
rkCountryStar = rkCountryStar.drop_duplicates()

# Função para a criação da nova coluna de lista de paises por rating
def countrys (row):
    if row['StarRating'] == 1:
        return rkStar1.index.tolist()
    elif row['StarRating'] == 2:
        return rkStar2.index.tolist()
    elif row['StarRating'] == 3:
        return rkStar3.index.tolist()
    elif row['StarRating'] == 4:
        return rkStar4.index.tolist()
    elif row['StarRating'] == 5:
        return rkStar5.index.tolist()
    else:
        return None
    
# Criando nova coluna de lista dos top 5 paises por rating   
rkCountryStar['Countrys'] = rkCountryStar.apply(countrys, axis=1)
rkCountryStar = rkCountryStar.sort_values(by='StarRating', ascending=True)
rkCountryStar