from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import Producto, Categoria, HistorialPrecio, Conversation, Message, Mensaje
from .serializers import (
    ProductoSerializer, 
    CrearProductoSerializer, 
    ActualizarProductoSerializer, 
    HistorialPrecioSerializer,
    ConversationSerializer,
    MessageSerializer, MensajeSerializer, UserSerializer
)


class ProductosPorCategoria(APIView):
    def get(self, request, id_categoria):
        categoria = get_object_or_404(Categoria, id=id_categoria)
        productos = Producto.objects.filter(categoria=categoria)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class HistorialPrecioView(APIView):
    def get(self, request, pk):
        historial_precios = HistorialPrecio.objects.filter(producto=pk)
        serializer = HistorialPrecioSerializer(historial_precios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductosEnPromocionAPIView(generics.ListAPIView):
    queryset = Producto.objects.filter(en_promocion=True)
    serializer_class = ProductoSerializer

class LanzamientosRecientesAPIView(generics.ListAPIView):
    queryset = Producto.objects.filter(lanzamiento_reciente=True)
    serializer_class = ProductoSerializer

class ListaProductos(APIView):
    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CrearProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetalleProducto(APIView):
    def get_object(self, pk):
        return get_object_or_404(Producto, pk=pk)

    def get(self, request, pk):
        producto = self.get_object(pk)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        producto = self.get_object(pk)
        serializer = ActualizarProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        producto = self.get_object(pk)
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConversationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ConversationDetailAPIView(generics.RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_id']
        conversation = Conversation.objects.get(pk=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)



class ListaMensajesUsuario(generics.ListAPIView):
    serializer_class = MensajeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        return Mensaje.objects.filter(destinatario=usuario)

class EnviarMensaje(generics.CreateAPIView):
    serializer_class = MensajeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(remitente=self.request.user)

class MarcarMensajeLeido(generics.UpdateAPIView):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(leido=True)
        

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)