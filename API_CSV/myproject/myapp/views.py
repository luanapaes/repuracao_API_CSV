# views.py
import csv
from django.http import JsonResponse
from .models import FitinsightBase
from django.shortcuts import render


def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(decoded_file)

        for row in csv_reader:
            FitinsightBase.objects.create(
                months_as_member=row['months_as_member'],
                weight=row['weight'],  # Corrigir a chave 'weight' aqui
                days_before=row['days_before'],
                day_of_week=row['day_of_week'],
                time=row['time'],
                category=row['category'],
                # Converta para um valor booleano
                attended=row['attended'] == '1',
            )

        return JsonResponse({'message': 'Dados do CSV foram salvos com sucesso.'})

    # Redireciona para uma página ou retorne a página atual após o envio
    return render(request, 'usuarios/upload_csv.html')
