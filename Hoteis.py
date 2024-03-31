import pandas as pd

df = pd.read_csv('C:/Users/User/Desktop/Analises de Dados/Dataset/Hotel.Dataset.csv', encoding='latin1')
df

df[' HotelRating'].value_counts().sort_index()

Cont_df_hoteis = df[' HotelCode'].value_counts()
Cont_df_hoteis