import requests
from rest_framework import serializers
from .models import Producto, HistorialPrecio, Inventario, Message, Conversation, Mensaje
from django.contrib.auth.models import User

class ProductoSerializer(serializers.ModelSerializer):
    precio_convertido = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'precio', 'descripcion', 'en_promocion', 'lanzamiento_reciente', 'precio_convertido']

    def get_precio_convertido(self, obj):
        # Aquí deberías implementar la lógica para convertir el precio a la moneda deseada
        # Puedes utilizar la API de conversión de divisas que prefieras
        # Aquí un ejemplo de cómo podrías hacerlo con CurrencyStack

        # Reemplaza 'YOUR_API_KEY' con tu clave de API real proporcionada por CurrencyStack
        api_key = 'vd71sghc3jd7h597kmc2agmtjt'

        # Moneda de origen (USD en este ejemplo)
        moneda_origen = 'USD'
        # Moneda de destino (la moneda a la que deseas convertir el precio)
        moneda_destino = 'EUR'  # Por ejemplo, EUR para Euros

        # Obtener el precio del producto
        precio = obj.precio

        # Realizar la solicitud a la API de conversión de divisas
        url = f'https://api.currency.com/convert?access_key={api_key}&from={moneda_origen}&to={moneda_destino}&amount={precio}'
        response = requests.get(url)
        data = response.json()

        # Verificar si la solicitud fue exitosa y obtener el precio convertido
        if response.status_code == 200:
            precio_convertido = data['result']
            return precio_convertido
        else:
            # En caso de error, devolver el precio original sin realizar ninguna conversión
            return precio

class CrearProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'descripcion', 'en_promocion', 'lanzamiento_reciente']
        extra_kwargs = {
            'descripcion': {'required': False},
            'en_promocion': {'required': False},
            'lanzamiento_reciente': {'required': False}
        }

class ActualizarProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'descripcion', 'en_promocion', 'lanzamiento_reciente']
        extra_kwargs = {
            'descripcion': {'required': False},
            'en_promocion': {'required': False},
            'lanzamiento_reciente': {'required': False}
        }

class HistorialPrecioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPrecio
        fields = ['id', 'producto', 'precio', 'fecha']


class InventarioProductoSerializer(serializers.ModelSerializer):
    producto_id = serializers.IntegerField(source='producto.id')
    sucursal_id = serializers.IntegerField(source='sucursal.id')
    producto_nombre = serializers.CharField(source='producto.nombre')
    sucursal_nombre = serializers.CharField(source='sucursal.nombre')
    
    class Meta:
        model = Inventario
        fields = ['producto_id', 'producto_nombre', 'sucursal_id', 'sucursal_nombre', 'cantidad']
        

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'user']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'timestamp', 'conversation']
        

class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = ['id', 'remitente', 'destinatario', 'contenido', 'fecha_envio', 'leido']
        read_only_fields = ['id', 'remitente', 'fecha_envio', 'leido']
        
        

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user