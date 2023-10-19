from django.db import models

class Usuarios(models.Model):
    ADMIN = 'admin'
    USUARIO = 'usuario'
    ROL_CHOICES = (
        (ADMIN, 'Admin'),
        (USUARIO, 'Usuario'),
    )
    nombre_usuario = models.CharField(max_length=30)
    clave = models.CharField(max_length=250)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default=USUARIO)

class Aulas(models.Model):
    numero = models.IntegerField()

class TipoSensores(models.Model):
    nombre = models.CharField(max_length=30)

class Sensores(models.Model):
    ip_aula = models.ForeignKey(Aulas, on_delete=models.CASCADE)
    last_signal_late = models.IntegerField()
    tipo = models.ForeignKey(TipoSensores, on_delete=models.CASCADE)

class Interacciones(models.Model):
    ENCENDIDO = 'encendido'
    APAGADO = 'apagado'
    TIPO_CHOICES = (
        (ENCENDIDO, 'encendido'),
        (APAGADO, 'apagado'),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    id_sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    fecha = models.DateTimeField()

class RegistrosLuces(models.Model):
    id_sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    desde = models.DateTimeField()
    hasta = models.DateTimeField()
    estado = models.BooleanField()


# Create your models here.
