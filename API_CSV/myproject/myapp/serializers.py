from rest_framework import serializers
from .models import FitinsightBase
from .models import BaseComPrevisao

class MinhaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitinsightBase
        fields = '__all__'


class BaseComPrevisaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseComPrevisao
        fields = '__all__'
