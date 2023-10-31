from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from django.urls import path, include
from GestionLuces.models import Aulas, Sensores, RegistrosLuces
from rest_framework.response import Response
import datetime
# Create your views here.

# Serializers
class AulasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Aulas
        fields = ['id', 'numero']

class SensoresSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sensores
        fields = ['id', 'aula', 'last_signal_late', 'tipo', 'ip']

#ViewSets
class AulasViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []

    queryset = Aulas.objects.all()
    serializer_class = AulasSerializer

class SensoresViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []

    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer

class RegistroDatosArduino (viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        ip = request.META.get('REMOTE_ADDR') #obtiene la ip del cliente cuando llama a la ruta 
        estado = request.data.get('estado')

        last_signal = Aulas.objects.filter(ip = ip).first() #obtiene el aula con su ultima señal
        last_signal.last_signal_date = datetime.datetime.now() #actualiza la ultima señal del aula
        last_signal.save()

        ultimo_registro = RegistrosLuces.objects.filter(sensor__aula__ip=ip, hasta=None).first() #obtiene el ultimo registro del sensor con la ip del sensor

        if int(ultimo_registro.estado) != estado: #si el estado no es el mismo
            nuevo_registro = RegistrosLuces.objects.create( #se crea un nuevo campo con el nuevo estado
                sensor = ultimo_registro.sensor,
                desde = datetime.datetime.now(),
                estado = estado
            )

            ultimo_registro.hasta = datetime.datetime.now() #se actualiza la fecha hasta del estado anterior
            ultimo_registro.save()
        
        return Response({})

#Routers
router = routers.DefaultRouter()
router.register(r'aulas', AulasViewSet)
router.register(r'sensores', SensoresViewSet)
router.register(r'registro_sensores', RegistroDatosArduino, basename='sensores')