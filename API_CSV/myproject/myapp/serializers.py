from rest_framework import serializers
from .models import FitinsightBase

class MinhaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitinsightBase
        fields = '__all__'