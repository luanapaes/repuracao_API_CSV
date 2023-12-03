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
                obter_dados_da_tabela()

            return JsonResponse({'message': 'Dados do CSV foram salvos com sucesso.'})
    else:
        form = CSVUploadForm()

    return render(request, 'usuarios/upload_csv.html', {'form': form})

# ------ pega a tabela ------------------------------------------------------------------------

# def obter_dados_da_tabela():
#     dados_da_tabela = FitinsightBase.objects.all()

#     return dados_da_tabela
# dados_tabela = obter_dados_da_tabela() #retona tudo que tem na tabela
# ----------------------------------------------------------------------------------------------

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

#------------------------------------------------------------------------------------------------------
# # pega a coluna vazia
# coluna_attended = FitinsightBase.objects.values_list('attended', flat=True)
# print(coluna_attended)

#-------------------------------------------------------------------------------------------
# previsoes = modelo_ia.predict(attended_coluna) # coloca a coluna gerada em uma variavel

#---esse delete apaga o que tem na coluna
# FitinsightBase.objects.all().delete()

# ---------- usado para exibir o json da tabela -----------------------------
class MinhaModelListCreateView(generics.ListCreateAPIView):
    queryset = FitinsightBase.objects.all()
    serializer_class = MinhaModelSerializer
