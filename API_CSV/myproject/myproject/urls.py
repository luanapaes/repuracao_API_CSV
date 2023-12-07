from django.urls import path
from myapp import views


urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
    path('api/minhamodel/',views.MinhaModelListCreateView.as_view(),name='minhamodel-list-create'),
    path('usuario/', views.usuario_previsao, name='usuario'),
    path('api/basecomprevisao/', views.BaseComPrecisaoListCreateView.as_view(),
         name='base-com-previsao-list-create'),

]