from django.urls import path
from . import views

urlpatterns = [
    # Productos
    path('', views.inicio, name='inicio'),
    path('producto/<int:id>/', views.detalle, name='detalle'),
    path('producto/nuevo/', views.crear_producto, name='CrearProducto'),
    path('producto/editar/<int:id>/', views.editar_producto, name='EditarProducto'),
    path('producto/eliminar/<int:id>/', views.eliminar_producto, name='EliminarProducto'),

    # Categorías y tallas
    path('catalogo/', views.catalogo, name='Catalogo'),
    path('categoria/nueva/', views.crear_categoria, name='CrearCategoria'),
    path('categoria/editar/<int:id>/', views.editar_categoria, name='EditarCategoria'),
    path('categoria/eliminar/<int:id>/', views.eliminar_categoria, name='EliminarCategoria'),
    path('talla/nueva/', views.crear_talla, name='CrearTalla'),
    path('talla/editar/<int:id>/', views.editar_talla, name='EditarTalla'),
    path('talla/eliminar/<int:id>/', views.eliminar_talla, name='EliminarTalla'),
]