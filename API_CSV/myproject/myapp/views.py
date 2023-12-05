# views.py
import uuid
from django.db import transaction

from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import sqlite3

import os
from .forms import CSVUploadForm
from .serializers import MinhaModelSerializer
from .serializers import BaseComPrevisaoSerializer
from .models import FitinsightBase
from .models import BaseComPrevisao
from rest_framework import generics
from django.shortcuts import render
from django.http import JsonResponse
import csv
import sys
sys.path.append(
    "C:/Users/notebook/Documents/API_csv/ambientev/Lib/site-packages")

modelo_treinado = 'API_CSV/myproject/myapp/modelo_treinado.pkl'


def usuario_previsao(request):
    return render(request, 'usuarios/usuario.html')

# ---------- usado para exibir o json da tabela -----------------------------


class MinhaModelListCreateView(generics.ListCreateAPIView):
    queryset = FitinsightBase.objects.all()
    serializer_class = MinhaModelSerializer

class BaseComPrecisaoListCreateView(generics.ListCreateAPIView):
    queryset = BaseComPrevisao.objects.all()
    serializer_class = BaseComPrevisaoSerializer

# FUNÇÕES


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)

            for row in csv_reader:

                instance = FitinsightBase(
                    months_as_member=row['months_as_member'],
                    weight=row['weight'],
                    days_before=row['days_before'],
                    day_of_week=row['day_of_week'],
                    time=row['time'],
                    category=row['category'],
                )

                instance.save()  # salva um modelo do csv que o usuário inserio

            return JsonResponse({'message': 'Dados do CSV foram salvos com sucesso.'})
    else:
        form = CSVUploadForm()

    return render(request, 'usuarios/upload_csv.html', {'form': form})


# ------ FAZ A CONVERSAO DOS DADOS CATEGORICOS PARA NUMERICOS ----------------------------------
# views.py
import sqlite3
import pandas as pd
import os
from .forms import CSVUploadForm
from .serializers import MinhaModelSerializer
from .models import FitinsightBase
from rest_framework import generics
from django.shortcuts import render
from django.http import JsonResponse
import csv
import sys
sys.path.append(
    "C:/Users/notebook/Documents/API_csv/ambientev/Lib/site-packages")

modelo_treinado = 'API_CSV/myproject/myapp/modelo_treinado.pkl'


def usuario_previsao(request):
    return render(request, 'usuarios/usuario.html')

# ---------- usado para exibir o json da tabela -----------------------------


class MinhaModelListCreateView(generics.ListCreateAPIView):
    queryset = FitinsightBase.objects.all()
    serializer_class = MinhaModelSerializer


# FUNÇÕES


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)

            for row in csv_reader:

                instance = FitinsightBase(
                    months_as_member=row['months_as_member'],
                    weight=row['weight'],
                    days_before=row['days_before'],
                    day_of_week=row['day_of_week'],
                    time=row['time'],
                    category=row['category'],
                )

                instance.save()  # salva um modelo do csv que o usuário inserio

            return JsonResponse({'message': 'Dados do CSV foram salvos com sucesso.'})
    else:
        form = CSVUploadForm()

    return render(request, 'usuarios/upload_csv.html', {'form': form})


# ------ FAZ A CONVERSAO DOS DADOS CATEGORICOS PARA NUMERICOS ----------------------------------
data_limpo = pd.read_csv('myapp\saida.csv')
# print(data_limpo)


# -- FAZ O CARREGAMENTO DO MODELO DE IA
def carregar_modelo_treinado(modelo):
    import joblib
    return joblib.load(modelo)


downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
caminho_modelo = os.path.join(downloads_path, 'modelo_arvore_decisao (4).pkl')
modelo_treinado = carregar_modelo_treinado(caminho_modelo)



# -- FAZ A CONVERSAO DOS DADOS PARA NUMERICOS E GERA A PREVISAO PARA PREENCHER A COLUNA ATTENDED
def obter_dados_da_tabela(tabela):
    dados_da_tabela = tabela

    # Mapeamento entre 'Sun' e 'Sat' e números
    dia_numero_mapping = {
        'Sun': 1,
        'Mon': 2,
        'Tue': 3,
        'Wed': 4,
        'Thu': 5,
        'Fri': 6,
        'Sat': 7
    }

    # Mapeamento entre 'PM' e 'AM' e números
    time_numero_mapping = {
        'PM': 0,
        'AM': 1
    }

    # Mapeamento entre categorias e números
    categoria_numero_mapping = {
        'Strength': 1,
        'HIIT': 2,
        'Cycling': 3,
        'Yoga': 4,
        'Others': 5,
        'Aqua': 6
    }

    # Criar um novo DataFrame chamado 'data_IA_tratado'
    data_IA_tratado = dados_da_tabela.copy()

    # Aplicar o mapeamento aos dados do modelo
    data_IA_tratado['day_of_week'] = data_IA_tratado['day_of_week'].map(dia_numero_mapping).fillna(data_IA_tratado['day_of_week'])
    data_IA_tratado['time'] = data_IA_tratado['time'].map(time_numero_mapping).fillna(data_IA_tratado['time'])
    data_IA_tratado['category'] = data_IA_tratado['category'].map(categoria_numero_mapping).fillna(data_IA_tratado['category'])

    # Remover a coluna 'attended' e id que estavam no csv do usuario

    data_IA_tratado = data_IA_tratado.drop('attended', axis=1)
    # Remover a coluna 'id' antes de fazer previsões
    data_IA_tratado = data_IA_tratado.drop('id', axis=1)

    # reordenando as colunas como no modelo
    colunas_esperadas = ['months_as_member', 'weight', 'days_before', 'day_of_week', 'time', 'category']

    # atribuindo o novo formato de colunas 
    data_IA_tratado = data_IA_tratado[colunas_esperadas]

    # Carregar o modelo
    modelo_ia = modelo_treinado

    # realizar as previsões
    previsoes = modelo_ia.predict(data_IA_tratado)

    # # Adicionar a coluna 'attended' ao DataFrame
    data_IA_tratado['attended'] = previsoes

    # # Salvar o novo DataFrame em um arquivo CSV
    data_IA_tratado.to_csv('myapp\data_IA_tratado.csv', index=False)
    print(data_IA_tratado)

    return data_IA_tratado

obter_dados_da_tabela(data_limpo)


# ---- COLOCANDO O NOVO DATAFRAME COM A PREVISÃO NO BANCO DE DADOS ---------------
arquivo_csv_com_previsao = 'myapp/data_IA_tratado.csv'

banco_de_dados = 'db.sqlite3'

# Nome da tabela no SQLite3
nome_tabela = 'myapp_basecomprevisao'

dados_csv = pd.read_csv(arquivo_csv_com_previsao)
# Adicionar uma coluna 'id' ao DataFrame com valores padrão
dados_csv['id'] = [str(uuid.uuid4()) for _ in range(len(dados_csv))]
# gera um id aleatorio já que minha base não tem

conexao = sqlite3.connect(banco_de_dados)

# Salvar os dados do DataFrame na tabela do SQLite3
dados_csv.to_sql(nome_tabela, conexao, if_exists='replace', index=False)

# Fechar a conexão com o banco de dados
conexao.close()

#apaga o q tem na tabela
# BaseComPrevisao.objects.all().delete()

# ---CRIA UM CSV DA TABELA----
# Conectar ao banco de dados SQLite
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Executar a consulta SQL para obter os dados da tabela
cursor.execute('SELECT * FROM myapp_fitinsightbase')

# Obter as colunas da tabela
colunas = [descricao[0] for descricao in cursor.description]

# Obter os dados da tabela
dados = cursor.fetchall()

# Fechar a conexão com o banco de dados
conn.close()

# Escrever os dados em um arquivo CSV
nome_arquivo_csv = 'saida.csv'
with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as arquivo_csv:
    writer = csv.writer(arquivo_csv)

    # Escrever o cabeçalho (nomes das colunas)
    writer.writerow(colunas)

    # Escrever os dados
    writer.writerows(dados)

print(f'Tabela exportada para {nome_arquivo_csv}')

