# views.py

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

# ------ FAZ A CONVERSAO DOS DADOS CATEGORICOS PARA NUMERICOS ------------------------------------

def obter_dados_da_tabela():
    dados_da_tabela = FitinsightBase.objects.all()

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

    # Aplicar o mapeamento aos dados do modelo
    for dado in dados_da_tabela:
        dado.day_of_week = dia_numero_mapping.get(
            dado.day_of_week, dado.day_of_week)
        dado.time = time_numero_mapping.get(dado.time, dado.time)
        dado.category = categoria_numero_mapping.get(
            dado.category, dado.category)

        # Salvar as alterações no banco de dados
        dado.save()

    return dados_da_tabela

# ---CRIA UM CSV DA TABELA----
import sqlite3
import csv

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

# -------------------------------------------------
import joblib
modelo_ia = joblib.load('modelo_treinado') #MEU PROBLEMA COMEÇA AQUI


#---esse delete apaga o que tem na coluna
# FitinsightBase.objects.all().delete()
