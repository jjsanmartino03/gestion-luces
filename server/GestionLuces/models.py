from django.db import models
from django.contrib.auth.models import User

class Aulas(models.Model):
    numero = models.IntegerField()

class TipoSensores(models.Model):
    nombre = models.CharField(max_length=30)

class Sensores(models.Model):
    aula = models.ForeignKey(Aulas, on_delete=models.CASCADE)
    last_signal_late = models.DateTimeField()
    tipo = models.ForeignKey(TipoSensores, on_delete=models.CASCADE)
    ip = models.CharField(max_length=30, unique=True)

class Interacciones(models.Model):
    ENCENDIDO = 'encendido'
    APAGADO = 'apagado'
    TIPO_CHOICES = (
        (ENCENDIDO, 'encendido'),
        (APAGADO, 'apagado'),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    fecha = models.DateTimeField()

class RegistrosLuces(models.Model):
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    desde = models.DateTimeField()
    hasta = models.DateTimeField()
    estado = models.BooleanField()


# Create your models here.
