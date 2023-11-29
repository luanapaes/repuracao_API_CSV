from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
]
