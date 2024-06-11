from django.contrib import admin

# Register your models here.
from .models import Producto, Categoria, HistorialPrecio, Inventario, Sucursal, Mensaje, Message, Conversation



class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'categoria', 'precio', 'descripcion']
    
    
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)
admin.site.register(HistorialPrecio)
admin.site.register(Inventario)
admin.site.register(Sucursal)
admin.site.register(Mensaje)
admin.site.register(Message)
admin.site.register(Conversation)