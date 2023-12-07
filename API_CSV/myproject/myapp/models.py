import uuid
from django.db import models

#modelo da tabela
class FitinsightBase(models.Model):
    months_as_member = models.IntegerField()
    weight = models.CharField(max_length=100)
    days_before = models.IntegerField()
    day_of_week = models.CharField(max_length=3)
    time = models.CharField(max_length=2)
    category = models.CharField(max_length=50)
    attended = models.BooleanField(null=True, blank=True)#deve iniciar vazia e ser preenchida só depois com a ia

    # coluna inicialmente vazia
    # new column
    def __str__(self):
        return f"{self.months_as_member} - {self.weight} - {self.days_before} - {self.day_of_week} - {self.time} - {self.category} - {self.attended}"

# TABELA PARA O DATAFRAME COM A COLUNA ATTENDED PREENCHIDA 
class BaseComPrevisao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    months_as_member = models.IntegerField()
    weight = models.CharField(max_length=100)
    days_before = models.IntegerField()
    day_of_week = models.CharField(max_length=3)
    time = models.CharField(max_length=2)
    category = models.CharField(max_length=50)
    attended = models.BooleanField()

def __str__(self):
    return f"{self.months_as_member} - {self.weight} - {self.days_before} - {self.day_of_week} - {self.time} - {self.category} - {self.attended}"
