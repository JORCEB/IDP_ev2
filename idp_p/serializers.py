import requests
from rest_framework import serializers
from .models import Producto, HistorialPrecio, Inventario, Message, Conversation, Mensaje
from django.contrib.auth.models import User

class ProductoSerializer(serializers.ModelSerializer):
 

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'precio', 'descripcion', 'en_promocion', 'lanzamiento_reciente']


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