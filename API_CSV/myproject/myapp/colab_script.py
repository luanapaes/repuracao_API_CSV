import pandas as pd
import requests
import joblib
from .models import FitinsightBase

# Carregar o DataFrame original
data_limpo = joblib.load(FitinsightBase) #minha base de dados sqlite

# Mapeamento entre dias da semana e números
dia_numero_mapping = {
    'Sun': 1,
    'Mon': 2,
    'Tue': 3,
    'Wed': 4,
    'Thu': 5,
    'Fri': 6,
    'Sat': 7
}

# Aplicar o mapeamento à coluna 'day_of_week'
if 'day_of_week' in data_limpo.columns:
    data_limpo['day_of_week'] = data_limpo['day_of_week'].map(dia_numero_mapping).fillna(data_limpo['day_of_week'])
else:
    data_limpo['day_of_week'] = data_limpo['day_of_week'].map(dia_numero_mapping)

# Mapeamento entre 'PM' e 'AM' e números
time_numero_mapping = {
    'PM': 0,
    'AM': 1
}

# Aplicar o mapeamento à coluna 'time'
if 'time' in data_limpo.columns:
    data_limpo['time'] = data_limpo['time'].map(time_numero_mapping).fillna(data_limpo['time'])
else:
    data_limpo['time'] = data_limpo['time'].map(time_numero_mapping)

# Mapeamento entre categorias e números
categoria_numero_mapping = {
    'Strength': 1,
    'HIIT': 2,
    'Cycling': 3,
    'Yoga': 4,
    'Others': 5,
    'Aqua': 6
}

# Aplicar o mapeamento à coluna 'category'
if 'category' in data_limpo.columns:
    data_limpo['category'] = data_limpo['category'].map(categoria_numero_mapping).fillna(data_limpo['category'])
else:
    data_limpo['category'] = data_limpo['category'].map(categoria_numero_mapping)

# Criar um novo DataFrame chamado 'data_IA_tratado'
data_IA_tratado = data_limpo.copy()

# Salvar o novo DataFrame em um arquivo CSV chamado 'data_IA_tratado.csv'
data_IA_tratado.to_csv('myapp/data_IA_tratado.csv', index=False)

# Recebe o novo dataframe e o coloca em uma variável para jogá-lo na IA
data_IA_tratado = pd.read_csv('myapp/data_IA_tratado.csv')
X = data_IA_tratado.drop('attended', axis=1) # remove a coluna que não será necessária

# Carregar o modelo treinado a partir do arquivo pkl usando joblib
modelo_ia = joblib.load('modelo_treinado.pkl') # Pelo nome e não pelo caminho

# Gerar previsões
previsoes = modelo_ia.predict(X)

# Enviar previsões para o backend
url = "http://127.0.0.1:8000/api/minhamodel/"
data = {'previsoes': previsoes.tolist()}  # Converta para lista para garantir a serialização correta
response = requests.post(url, json=data)

# Verificar a resposta
if response.status_code == 200:
    print("Previsões enviadas com sucesso para o backend.")
else:
    print("Erro ao enviar previsões para o backend.")
    print(response.text)
