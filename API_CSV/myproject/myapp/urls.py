from django.urls import path, include
from django.contrib import admin
from django.urls import path
from myapp.views import MinhaModelListCreateView
from myapp.views import BaseComPrecisaoListCreateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('meu_app/', include('myproject.urls')),
    path('api/minhamodel/', MinhaModelListCreateView.as_view(), name='minhamodel-list-create'),
    path('api/basecomprevisao/', BaseComPrecisaoListCreateView,
         name='base-com-previsao-list-create'),
]