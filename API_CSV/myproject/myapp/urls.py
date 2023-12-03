from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('meu_app/', include('myproject.urls')),
    path('app_flask/', include('meu_app_flask.urls')),
]
