# Importando as bibliotecas
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist



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
rkHoteisMais = qtdHoteis['countyName'].value_counts().sort_values(ascending=False).head(5)

plt.figure(figsize=(9, 5))
plt.bar(rkHoteisMais.index, rkHoteisMais.values, color='lightgreen')

# Adiconando os labels no topo das barras
for x, y in zip(rkHoteisMais.index, rkHoteisMais.values):
    plt.text(x, y, str(y), ha='center', va='bottom')
     
plt.xlabel('Paises')
plt.ylabel('QtdHotéis')
plt.title('Paises que contém mais Hotéis')
plt.tight_layout()

# Ranking dos 5 paises que contem menos hotéis no Dataset
rkHoteisMenos = qtdHoteis['countyName'].value_counts().sort_values(ascending=True).head(5)

plt.figure(figsize=(9, 5))
plt.bar(rkHoteisMenos.index, rkHoteisMenos.values, color='red')

# Adiconando os labels no topo das barras
for x, y in zip(rkHoteisMenos.index, rkHoteisMenos.values):
    plt.text(x, y, str(y), ha='center', va='bottom')
     
plt.xlabel('Paises')
plt.ylabel('QtdHotéis')
plt.title('Paises que contém menos Hotéis')
plt.tight_layout()

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


# CRIAÇÃO DE UM MODELO NLP PARA CRIAR UMA ANALISE DE SENTIMENTO DA AVALIAÇÃO DO CLIENTE

# Pré-processamento dos dados
qtdHoteis['HotelFacilities'] = qtdHoteis['HotelFacilities'].astype(str) # Transformando a coluna em String
qtdHoteis['HotelFacilities'] = qtdHoteis['HotelFacilities'].str.lower() # Minuscula

qtdHoteis['HotelFacilities'] = qtdHoteis['HotelFacilities'].apply(word_tokenize) # Tokenização

# Criando uma lista de palavras para fazer a limpeza dos dados de Facillities
stopWords = set(stopwords.words('english'))
custom_stopwords = ['li', 'p', 'el', 'may', 'property', 'gouna', 'mi', 'hotel', 'site', 'available', 'plastic', 'number'
                    , 'comprehensive', 'policy', 'water', 'bottles', 'reusable', 'free', 'nearby', 'cleaning'
                    , 'guest', 'dispenser', 'toiletries', 'airport', 'local', 'front', 'food', 'service', 'dry', 'desk'
                    , 'products', 'energy', 'source', 'solar', 'bulk', 'grey', 'system', 'breakfast', 'used', 'furniture'
                    , 'straws', 'soda', 'stirrers', 'recycling', 'swimming', 'cups', 'tableware', 'sailing','areas', 'rooms'
                    , 'accommodation', 'services', 'internet', 'guests', 'terrace', 'private', 'physical', 'facilities'
                    , 'laundry', 'throughout', 'staff', 'key', 'heating', 'area', 'distancing','safety', 'sun', 'family'
                    , 'shared', 'provided', 'towels', 'air', 'conditioning', 'protocols', 'follow', 'directed', 'invoice'
                    , 'room', 'use', 'linens', 'authorities', 'authority', 'chemicals', 'guidelines', 'accordance', 'effective'
                    , 'coronavirus', 'disinfected', 'stays', 'washed', 'hand', 'menus', 'followed', 'rules', 'cashless'
                    , 'payment', 'access', 'sanitizer', 'storage', 'allowed', 'fire', 'extinguishers', 'accessible', 'bbq'
                    , 'additional', 'daily' 'charge', 'housekeeping', 'daily', 'charge', 'cutlery', 'plates', 'glasses'
                    , 'sanitized', 'removed', 'luggage', 'first', 'aid', 'kit', 'stationary', 'printed', '(', ')', 'onsite'
                    , 'common', 'surcharge', 'shuttle', 'check-in/check-out', 'designated', 'currency', 'car', 'hire'
                    , 'exchange', 'ironing', 'newspapaers'
                   ]
stopWords.update(custom_stopwords)
qtdHoteis['HotelFacilities'] = qtdHoteis['HotelFacilities'].apply(lambda x: [word for word in x if word not in stopWords])

# criando um dicionario para adicionar as facilities com respectivos valores de rating
facilityRating = {}

# Adicionando os valores e as facilites no dicionário
for index, row in qtdHoteis.iterrows():
    for facility in row['HotelFacilities']:
        if facility not in facilityRating:
            facilityRating[facility] = []
        facilityRating[facility].append(row['StarRating'])
        
 # Calculando a média para trazer a média de entre os ratings de cada facility       
facilityAvgRating = {facility: sum(ratings)/len(ratings) for facility, ratings in facilityRating.items()} # Average Rating
sortedAvg = sorted(facilityAvgRating.items(), key=lambda x: [1], reverse=True) # Average Sorted

topFacilities = [facility[0] for facility in sortedAvg[:10]] # Top 10
avgRating = [facility[1] for facility in sortedAvg[:10]] # Average Rating

# Criando o gráfico para trazer o top 10 de facility e as médias do StarRating 
plt.figure(figsize=(10,6))
plt.barh(topFacilities, avgRating, color= 'skyblue', label= 'Average Rating')

for facility, rating in zip(topFacilities, avgRating):
    plt.text(rating, facility, str(round(rating, 2)), ha='left', va='center', color='black', fontsize=10)
    
plt.xlabel('Average Rating')
plt.title('Top 10 Facilities by Average Rating')
plt.gca().invert_yaxis()
plt.show()