# views.py
import sys 
sys.path.append("C:/Users/notebook/Documents/API_csv/ambientev/Lib/site-packages")

import pandas as pd
import csv
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics

from .models import FitinsightBase
from .serializers import MinhaModelSerializer
from .forms import CSVUploadForm


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
dados_tabela = obter_dados_da_tabela() #retona tudo que tem na tabela  


# ---------- usado para exibir o json da tabela -----------------------------
class MinhaModelListCreateView(generics.ListCreateAPIView):
    queryset = FitinsightBase.objects.all()
    serializer_class = MinhaModelSerializer