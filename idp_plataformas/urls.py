"""
URL configuration for idp_plataformas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from idp_p.views import ListaProductos, DetalleProducto, ProductosPorCategoria, HistorialPrecioView,ProductosEnPromocionAPIView, LanzamientosRecientesAPIView, ConversationDetailAPIView, MessageListCreateAPIView, ConversationListCreateAPIView, ListaMensajesUsuario, MarcarMensajeLeido, EnviarMensaje, UserRegistrationAPIView

urlpatterns = [

    
    path('productos/', ListaProductos.as_view(), name='lista_productos'),
    path('productos/<int:pk>/', DetalleProducto.as_view(), name='detalle_producto'),
    path('productos/categoria/<int:id_categoria>/', ProductosPorCategoria.as_view(), name='productos_por_categoria'),
    path('historial-precio/<int:pk>/', HistorialPrecioView.as_view(), name='historial_precio'),
    path('productos/promocion/', ProductosEnPromocionAPIView.as_view(), name='productos_en_promocion'),
    path('productos/lanzamientos-recientes/', LanzamientosRecientesAPIView.as_view(), name='lanzamientos_recientes'),
    path('conversations/', ConversationListCreateAPIView.as_view(), name='conversation_list_create'),
    path('conversations/<int:pk>/', ConversationDetailAPIView.as_view(), name='conversation_detail'),
    path('conversations/<int:conversation_id>/messages/', MessageListCreateAPIView.as_view(), name='message_list_create'),
    path('messages/', ListaMensajesUsuario.as_view(), name='lista_mensajes_usuario'),
    path('messages/send/', EnviarMensaje.as_view(), name='enviar_mensaje'),
    path('messages/<int:pk>/mark-as-read/', MarcarMensajeLeido.as_view(), name='marcar_mensaje_leido'),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('admin/', admin.site.urls),  # Esta línea agrega la URL para el panel de administración
    
]


