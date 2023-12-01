# views.py
import pandas as pd
import csv
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics

from .models import FitinsightBase
from .serializers import MinhaModelSerializer
from .forms import CSVUploadForm

arvore_de_decisao = 'models\modelo_arvore_decisao.pkl'

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

                instance.save() #salva um modelo do csv que o usuário inserio

            return JsonResponse({'message': 'Dados do CSV foram salvos com sucesso.'})
    else:
        form = CSVUploadForm()

    return render(request, 'usuarios/upload_csv.html', {'form': form})

# ------ pega a tabela --------------------------------------------------------------------------

def obter_dados_da_tabela():
    dados_da_tabela = FitinsightBase.objects.all()

    return dados_da_tabela
dados_tabela = obter_dados_da_tabela()#retona tudo que tem na tabela  

# ----------- função para preencher a coluna vazia ----------------------------------------------------
from django.db import connection

def preencher_coluna_attended(nome_tabela, modelo_path):
    # Consulta para obter todos os dados da tabela FitinsightBase
    consulta_sql = f"SELECT * FROM {nome_tabela}"

    # Carregar os dados diretamente do SQLite usando a conexão do Django
    with connection.cursor() as cursor:
        cursor.execute(consulta_sql)
        colunas = [desc[0] for desc in cursor.description]
        data_limpo = pd.DataFrame(cursor.fetchall(), columns=colunas)

    # Mapeamento entre dias da semana e números
    dia_numero_mapping = {'Sun': 1, 'Mon': 2, 'Tue': 3, 'Wed': 4, 'Thu': 5, 'Fri': 6, 'Sat': 7}
    data_limpo['day_of_week'] = data_limpo['day_of_week'].map(dia_numero_mapping).fillna(data_limpo['day_of_week'])

    # Mapeamento entre 'PM' e 'AM' e números
    time_numero_mapping = {'PM': 0, 'AM': 1}
    data_limpo['time'] = data_limpo['time'].map(time_numero_mapping).fillna(data_limpo['time'])

    # Mapeamento entre categorias e números
    categoria_numero_mapping = {'Strength': 1, 'HIIT': 2, 'Cycling': 3, 'Yoga': 4, 'Others': 5, 'Aqua': 6}
    data_limpo['category'] = data_limpo['category'].map(categoria_numero_mapping).fillna(data_limpo['category'])

    # Criar um novo DataFrame chamado 'data_IA_tratado'
    data_IA_tratado = data_limpo.copy()

    # Remover a coluna 'attended' para a predição
    X = data_IA_tratado.drop('attended', axis=1)

    import joblib
    # Carregar o modelo treinado
    modelo_ia = joblib.load(modelo_path)

    # Fazer previsões
    previsoes = modelo_ia.predict(X)

    # Adicionar as previsões ao DataFrame original
    data_com_a_previsao = data_limpo.copy()
    data_com_a_previsao['attended'] = previsoes

    return data_com_a_previsao

# ----------------------------------------------------
data_com_a_previsao = preencher_coluna_attended(dados_tabela, arvore_de_decisao) 
# roda a função com a tabela real e com a arvore de decisão

# coloca os valores da gerados pela ia na coluna 
for index, row in data_com_a_previsao.iterrows():
    FitinsightBase.objects.filter(id=row['id']).update(attended=row['attended'])


# ---------- usado para exibir o json da tabela -----------------------------
class MinhaModelListCreateView(generics.ListCreateAPIView):
    queryset = FitinsightBase.objects.all()
    serializer_class = MinhaModelSerializer