from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, status
from django.urls import path, include
from GestionLuces.models import Aulas, Sensores, RegistrosLuces, Interacciones
from rest_framework.response import Response
import datetime
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser



# Create your views here.

# Serializers
class AulasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Aulas
        fields = ['id', 'numero', 'last_signal_date', 'ip']

class SensoresSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sensores
        fields = ['id', 'aula', 'tipo']

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

class InteraccionesView(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        if request.method == 'POST':
            id_aula = request.POST.get('id_aula')
            try:
                aula = Aulas.objects.get(id=id_aula)
                sensor = Sensores.objects.get(aula=id_aula, tipo=Sensores.Tipo.RELE)
                id_sensor = sensor.id
                ultimoRegistro = RegistrosLuces.objects.filter(sensor=id_sensor).last()
                if ultimoRegistro is not None:
                    estado = ultimoRegistro.estado
                    if estado == 1:
                        tipo = Interacciones.Tipo.APAGADO
                    else:
                        tipo = Interacciones.Tipo.ENCENDIDO
                else:
                    tipo = Interacciones.Tipo.APAGADO
                interaccion = Interacciones.objects.create(
                    usuario=request.user,
                    fecha=datetime.datetime.now(),
                    tipo=tipo,
                    sensor=sensor
                )
                return Response('Accion realizada correctamente.', status=status.HTTP_201_CREATED)
            except Aulas.DoesNotExist:
                return Response('No se encontro una aula con ese ID.', status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        aulas = Aulas.objects.all()
        datos_aulas = []
        for aula in aulas:
            sensor = Sensores.objects.get(aula=aula.id, tipo=Sensores.Tipo.RELE)
            ultimoRegistro = RegistrosLuces.objects.filter(sensor=sensor.id).last()
            datos_aula = {
                'aula_id': aula.id,
                'aula_numero': aula.numero,
                'has_rele': True if sensor else False,
                'estado': ultimoRegistro.estado if ultimoRegistro else False,
                'desde': ultimoRegistro.desde if ultimoRegistro else False,
            }
            datos_aulas.append(datos_aula)
        return Response(datos_aulas)




#Routers
router = routers.DefaultRouter()
router.register(r'aulas', AulasViewSet)
router.register(r'sensores', SensoresViewSet)
router.register(r'registro_sensores', RegistroDatosArduino, basename='sensores')
router.register(r'usuarios', UsuariosViewSet)
router.register(r'user', GetAuthenticatedUser, basename='user')
router.register(r'interacciones', InteraccionesView, basename='interacciones')