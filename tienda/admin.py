from django.contrib import admin
from .models import Categoria, Talla, Producto, Cliente, Pedido, DetallePedido 

admin.site.register(Categoria)
admin.site.register(Talla)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
