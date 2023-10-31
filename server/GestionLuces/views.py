from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from django.urls import path, include
from GestionLuces.models import Aulas, Sensores
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

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

class UsuariosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        user = User(**validated_data)
        user.save()
        return user

#ViewSets
class AulasViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Aulas.objects.all()
    serializer_class = AulasSerializer

class SensoresViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer

class UsuariosViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UsuariosSerializer

#Routers
router = routers.DefaultRouter()
router.register(r'aulas', AulasViewSet)
router.register(r'sensores', SensoresViewSet)
router.register(r'usuarios', UsuariosViewSet)