from django.contrib.auth.hashers import make_password
from rest_framework import routers, serializers, viewsets, status
from GestionLuces.models import Aulas, Sensores, RegistrosLuces, Interacciones
from rest_framework.response import Response
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from requests import post, get


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


# ViewSets
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


class RegistroDatosArduino(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        ip = request.META.get('REMOTE_ADDR')  # obtiene la ip del cliente cuando llama a la ruta

        estado = request.data.get('estado')

        last_signal = Aulas.objects.filter(ip = ip).first() #obtiene el aula con su ultima señal
        last_signal.last_signal_date = datetime.now() #actualiza la ultima señal del aula
        last_signal.save()

        ultimo_registro = RegistrosLuces.objects.filter(sensor__aula__ip=ip).last() #obtiene el ultimo registro del sensor con la ip del sensor

        if not ultimo_registro:
            sensor = Sensores.objects.get(aula__ip=ip, tipo=Sensores.Tipo.FOTOSENSIBLE) #obtiene el sensor fotosensible con la ip del aula

            nuevo_registro = RegistrosLuces.objects.create( #se crea un nuevo campo con el nuevo estado
                sensor = sensor,
                desde = datetime.now(),
                estado = estado
            )
        elif int(ultimo_registro.estado) != int(estado): #si el estado no es el mismo
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
        if request.method != 'POST':
            return

        id_aula = request.data.get('id_aula')
        try:
            estado = 0
            aula = Aulas.objects.get(id=id_aula)
            sensor_rele = Sensores.objects.get(aula=id_aula, tipo=Sensores.Tipo.RELE)
            sensor_fotosensible = Sensores.objects.get(aula=id_aula, tipo=Sensores.Tipo.FOTOSENSIBLE)
            id_sensor = sensor_rele.id
            ultimoRegistro = RegistrosLuces.objects.filter(sensor=sensor_fotosensible.id).last()
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
                fecha=datetime.now(),
                tipo=tipo,
                sensor=sensor_rele
            )

            response = get(f'http://{aula.ip}/hola')
            if response.status_code != 200:
                raise Exception('Error al llamar a la API del arduino.', [
                    response.status_code,
                    response.text
                ])

            arduino_status = 1 if int(response.text) == 0 else 0 # ¿porqueeee?
            # creo que porque la medición que hace el arduino se hace antes de que
            # se llegue a prender el foco, luego del cambio del relé. HAY QUE REVISARLO

            # según lo que nos dice el arduino, actualizamos el estado de la luz
            if ultimoRegistro and arduino_status == 0 and ultimoRegistro.estado == 1:
                nuevo_registro = RegistrosLuces.objects.create(
                    sensor=sensor_fotosensible,
                    desde=datetime.now(),
                    estado=0
                )
                ultimoRegistro.hasta = datetime.now()
                ultimoRegistro.save()
            elif ultimoRegistro and arduino_status == 1 and ultimoRegistro.estado == 0:
                ultimoRegistro.hasta = datetime.now()
                ultimoRegistro.save()
                nuevo_registro = RegistrosLuces.objects.create(
                    sensor=sensor_fotosensible,
                    desde=datetime.now(),
                    estado=1
                )

            return Response({
                'estado': arduino_status,
            }, status=status.HTTP_201_CREATED)
        except Aulas.DoesNotExist:
            return Response('No se encontro una aula con ese ID.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response('Error al realizar la accion.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        aulas = Aulas.objects.all()
        datos_aulas = []
        for aula in aulas:
            rele = Sensores.objects.get(aula=aula.id, tipo=Sensores.Tipo.RELE)
            sensor_fotosensible = Sensores.objects.get(aula=aula.id, tipo=Sensores.Tipo.FOTOSENSIBLE)
            ultimo_registro = RegistrosLuces.objects.filter(sensor=sensor_fotosensible.id).last()
            datos_aula = {
                'aula_id': aula.id,
                'aula_numero': aula.numero,
                'has_rele': True if rele else False,
                'estado': ultimo_registro.estado if ultimo_registro else False,
                'desde': ultimo_registro.desde if ultimo_registro else False,
            }

            datos_aulas.append(datos_aula)
        return Response(datos_aulas)


# Routers
router = routers.DefaultRouter()
router.register(r'aulas', AulasViewSet)
router.register(r'sensores', SensoresViewSet)
router.register(r'registro_sensores', RegistroDatosArduino, basename='sensores')
router.register(r'usuarios', UsuariosViewSet)
router.register(r'user', GetAuthenticatedUser, basename='user')
router.register(r'interacciones', InteraccionesView, basename='interacciones')
router.register(r'estadistica_semanal', EstadisticasSemanales, basename='estadisticas')
