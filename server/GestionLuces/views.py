from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from django.urls import path, include
from GestionLuces.models import Aulas, Sensores
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

#Routers
router = routers.DefaultRouter()
router.register(r'aulas', AulasViewSet)
router.register(r'sensores', SensoresViewSet)