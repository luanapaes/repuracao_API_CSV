from django.urls import path, include
from django.contrib import admin
from django.urls import path
from myapp.views import MinhaModelListCreateView

urlpatterns = [
    # ... outras configurações de URL ...
    path('admin/', admin.site.urls),
    path('meu_app/', include('myproject.urls')),
    path('api/minhamodel/', MinhaModelListCreateView.as_view(), name='minhamodel-list-create'),
    # ... outras configurações de URL ...
]