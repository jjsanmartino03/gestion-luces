from django.db import models
from django.contrib.auth.models import User
import datetime

class Aulas(models.Model):
    numero = models.IntegerField()
    ip = models.CharField(max_length=30, unique=True)
    last_signal_date = models.DateTimeField(default=datetime.datetime.now())

class Sensores(models.Model):
    class Tipo(models.TextChoices):
        FOTOSENSIBLE = 'fotosensible', 'fotosensible'
        RELE = 'rele', 'rele'
    aula = models.ForeignKey(Aulas, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=30, choices=Tipo.choices)

class Interacciones(models.Model):
    class Tipo(models.TextChoices):
        ENCENDIDO = 'encendido', 'encendido'
        APAGADO = 'apagado', 'apagado'
    tipo = models.CharField(max_length=30, choices=Tipo.choices)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    fecha = models.DateTimeField()

class RegistrosLuces(models.Model):
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    desde = models.DateTimeField()
    hasta = models.DateTimeField(null = True)
    estado = models.BooleanField()


# Create your models here.
