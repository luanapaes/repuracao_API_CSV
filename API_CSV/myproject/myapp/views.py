# No arquivo views.py do seu aplicativo (myapp)
import pandas as pd
import csv
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import generics
from .models import FitinsightBase
from .serializers import MinhaModelSerializer
from .forms import CSVUploadForm
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
modelo_ia_path = os.path.join(BASE_DIR, 'myapp', 'models', 'pkl', 'modelo_arvore_decisao.pkl')

# Verifique se o arquivo existe antes de tentar carregar
if os.path.exists(modelo_ia_path):
    try:
        modelo_ia = joblib.load(modelo_ia_path)
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        modelo_ia = None
else:
    print(f"Erro: O arquivo {modelo_ia_path} não foi encontrado.")
    modelo_ia = None

class MinhaModelListCreateView(generics.ListCreateAPIView):
    queryset = FitinsightBase.objects.all()
    serializer_class = MinhaModelSerializer

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)

            dia_numero_mapping = {
                'Sun': 1,
                'Mon': 2,
                'Tue': 3,
                'Wed': 4,
                'Thu': 5,
                'Fri': 6,
                'Sat': 7
            }

            time_numero_mapping = {
                'PM': 0,
                'AM': 1
            }

            categoria_numero_mapping = {
                'Strength': 1,
                'HIIT': 2,
                'Cycling': 3,
                'Yoga': 4,
                'Others': 5,
                'Aqua': 6
            }

            if modelo_ia is not None:  # Verifica se o modelo foi carregado corretamente
                for row in csv_reader:
                    row['day_of_week'] = dia_numero_mapping.get(row['day_of_week'], row['day_of_week'])
                    row['time'] = time_numero_mapping.get(row['time'], row['time'])
                    row['category'] = categoria_numero_mapping.get(row['category'], row['category'])

                    instance = FitinsightBase(
                        months_as_member=row['months_as_member'],
                        weight=row['weight'],
                        days_before=row['days_before'],
                        day_of_week=row['day_of_week'],
                        time=row['time'],
                        category=row['category'],
                    )

                    instance.save()

                    dados = pd.DataFrame({
                        'months_as_member': [row['months_as_member']],
                        'weight': [row['weight']],
                        'days_before': [row['days_before']],
                        'day_of_week': [row['day_of_week']],
                        'time': [row['time']],
                        'category': [row['category']],
                    })

                    previsao = modelo_ia.predict(dados)

                    instance.attended = previsao[0]
                    instance.save()

                return JsonResponse({'message': 'Dados do CSV foram salvos com sucesso.'})
            else:
                return JsonResponse({'error': 'O modelo não foi carregado corretamente.'})
    else:
        form = CSVUploadForm()

    return render(request, 'usuarios/upload_csv.html', {'form': form})
