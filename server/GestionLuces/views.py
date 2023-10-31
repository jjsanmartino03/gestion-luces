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
        ultimo_registro = RegistrosLuces.objects.filter(sensor__aula__ip=ip).first()
        if int(ultimo_registro.estado) == estado:
            ultimo_registro.hasta = datetime.datetime.now() 
            ultimo_registro.save()
        else:
            nuevo_registro = RegistrosLuces.object.create(
                sensor = ultimo_registro.sensor,
                desde = datetime.datetime.now(),
                hasta = datetime.datetime.now(),
                estado = estado
            )
        return Response({})

#Routers
router = routers.DefaultRouter()
router.register(r'aulas', AulasViewSet)
router.register(r'sensores', SensoresViewSet)
router.register(r'registro_sensores', RegistroDatosArduino, basename='sensores')