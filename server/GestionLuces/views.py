from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from django.urls import path, include
from GestionLuces.models import Aulas, Sensores, RegistrosLuces
from rest_framework.response import Response
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from django.utils import timezone

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

class RegistroDatosArduino (viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        ip = request.META.get('REMOTE_ADDR') #obtiene la ip del cliente cuando llama a la ruta 
        estado = request.data.get('estado')

        last_signal = Aulas.objects.filter(ip = ip).first() #obtiene el aula con su ultima señal
        last_signal.last_signal_date = datetime.now() #actualiza la ultima señal del aula
        last_signal.save()

        ultimo_registro = RegistrosLuces.objects.filter(sensor__aula__ip=ip).last() #obtiene el ultimo registro del sensor con la ip del sensor

        if int(ultimo_registro.estado) != estado: #si el estado no es el mismo
            nuevo_registro = RegistrosLuces.objects.create( #se crea un nuevo campo con el nuevo estado
                sensor = ultimo_registro.sensor,
                desde = datetime.now(),
                estado = estado
            )

            ultimo_registro.hasta = datetime.now() #se actualiza la fecha hasta del estado anterior
            ultimo_registro.save()
        else:
            if ultimo_registro.desde.date() < datetime.now().date():
                nuevo_registro = RegistrosLuces.objects.create(
                    sensor = ultimo_registro.sensor,
                    desde = datetime.now(),
                    estado = estado
                )

                ultimo_registro.hasta = datetime(datetime.now().year, datetime.now().month, datetime.now().day - 1, 23, 59, 59)
                ultimo_registro.save()

        return Response({})
    
class EstadisticasSemanales (viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def calcular_consumo_diario(self, fecha):
        tiempo_total = timedelta()
        registros = RegistrosLuces.objects.filter(
            desde__date=fecha,
            estado=1
        )

        for registro in registros:
            hasta = registro.hasta

            if not hasta:
                hasta = datetime.now()
            else:
                hasta = datetime.fromtimestamp(registro.hasta.timestamp())

            desde = datetime.fromtimestamp(registro.desde.timestamp())

            tiempo_total += hasta - desde
        return tiempo_total


    def list(self, request):
        fecha_domingo = request.query_params.get('fecha_domingo')
        fecha_domingo = datetime.strptime(fecha_domingo, '%Y-%m-%d').date()
        lista = []
        for i in range(7):
            nueva_fecha = fecha_domingo + timedelta(days=i)
            registro_diario = self.calcular_consumo_diario(nueva_fecha)
            lista.append(round(registro_diario.total_seconds()/3600, 4))

        return Response(lista)

#Routers
router = routers.DefaultRouter()
router.register(r'aulas', AulasViewSet)
router.register(r'sensores', SensoresViewSet)
router.register(r'registro_sensores', RegistroDatosArduino, basename='sensores')
router.register(r'usuarios', UsuariosViewSet)
router.register(r'estadistica_semanal', EstadisticasSemanales, basename='estadisticas')
