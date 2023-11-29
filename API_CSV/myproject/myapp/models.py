from django.db import models


class FitinsightBase(models.Model):
    months_as_member = models.IntegerField()
    weight = models.CharField(max_length=100)
    days_before = models.IntegerField()
    day_of_week = models.CharField(max_length=3)
    time = models.CharField(max_length=2)
    category = models.CharField(max_length=50)
    attended = models.BooleanField()
    presence = models.BooleanField(null=True, blank=True)
    
    # coluna inicialmente vazia
    # new column

