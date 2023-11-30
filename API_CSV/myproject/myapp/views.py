# views.py
import csv
from django.http import HttpResponse
from django.http import JsonResponse
from .models import FitinsightBase
from django.shortcuts import render
from rest_framework import generics
from .serializers import MinhaModelSerializer
import sqlite3



from .forms import CSVUploadForm

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)

            for row in csv_reader:
                FitinsightBase.objects.create(
                    months_as_member=row['months_as_member'],
                    weight=row['weight'],
                    days_before=row['days_before'],
                    day_of_week=row['day_of_week'],
                    time=row['time'],
                    category=row['category'],
                )

            return JsonResponse({'message': 'Dados do CSV foram salvos com sucesso.'})
    else:
        form = CSVUploadForm()

    return render(request, 'usuarios/upload_csv.html', {'form': form})


class MinhaModelListCreateView(generics.ListCreateAPIView):
    queryset = FitinsightBase.objects.all()
    serializer_class = MinhaModelSerializer