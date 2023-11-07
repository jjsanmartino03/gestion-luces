import datetime

from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, status
from django.urls import path, include
from GestionLuces.models import Aulas, Sensores
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


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

class GetAuthenticatedUser(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        data = {
            'username': user.username,
            'is_staff': user.is_staff,
        }
        return Response(data)

class Interacciones(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        id_usuario = request.user.id
        fecha = datetime.datetime.now()
        if request.method == 'POST':
            id_aula = request.POST.get('id_aula')
            try:
                aula = Aulas.objects.get(id_aula)
                sensor = Sensores.objects.filter(aula=id_aula).filter(tipo='RELE')
            except Aulas.DoesNotExist:
                return Response('No se encontro una aula con ese ID.', status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        pass




#Routers
router = routers.DefaultRouter()
router.register(r'aulas', AulasViewSet)
router.register(r'sensores', SensoresViewSet)
router.register(r'usuarios', UsuariosViewSet)
router.register(r'user', GetAuthenticatedUser, basename='user')