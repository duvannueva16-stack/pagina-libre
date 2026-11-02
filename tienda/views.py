from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProductoForm, CategoriaForm, TallaForm
from .models import Producto, Categoria, Talla


# Funciones reutilizables 

def _editar_objeto(request, objeto, clase_form, titulo, volver):
    """Edita cualquier objeto (categoría o talla) con su formulario."""
    if request.method == 'POST':
        form = clase_form(request.POST, instance=objeto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cambios guardados correctamente')
            return redirect(volver)
    else:
        form = clase_form(instance=objeto)

    return render(request, 'tienda/formulario.html', {
        'form': form,
        'titulo': titulo,
    })


def _confirmar_eliminacion(request, objeto, tipo, volver):
    """Pide confirmación y elimina cualquier objeto."""
    if request.method == 'POST':
        try:
            objeto.delete()
            messages.success(request, f'«{objeto}» eliminado correctamente')
        except ProtectedError:
            # Pasa si hay productos que usan esa categoría o talla
            messages.error(request, f'No se puede eliminar «{objeto}» porque está siendo usado')
        return redirect(volver)

    return render(request, 'tienda/eliminar.html', {
        'objeto': objeto,
        'tipo': tipo,
        'volver': volver,
    })


#Productos 

def inicio(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    categoria_id = request.GET.get('categoria')
    seleccionar = request.GET.get('seleccionar')

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if seleccionar:
        productos = productos.filter(nombre__icontains=seleccionar)

    return render(request, 'tienda/inicio.html', {
        'productos': productos,
        'categorias': categorias,
    })


def detalle(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'tienda/detalle.html', {'producto': producto})


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente')
            return redirect('inicio')
    else:
        form = ProductoForm()

    return render(request, 'tienda/formulario.html', {
        'form': form,
        'titulo': 'Nuevo producto',
    })


def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
    else:
        form = ProductoForm(instance=producto)

    # La categoría no se puede cambiar al editar
    form.fields['categoria'].disabled = True

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto editado correctamente')
        return redirect('inicio')

    return render(request, 'tienda/editar.html', {'form': form})


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return _confirmar_eliminacion(request, producto, 'producto', 'inicio')


#  Categorías y tallas

def catalogo(request):
    return render(request, 'tienda/catalogo.html', {
        'categorias': Categoria.objects.all(),
        'tallas': Talla.objects.all(),
    })


def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente')
            return redirect('Catalogo')
    else:
        form = CategoriaForm()

    return render(request, 'tienda/formulario.html', {
        'form': form,
        'titulo': 'Nueva categoría',
    })


def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    return _editar_objeto(request, categoria, CategoriaForm, 'Editar categoría', 'Catalogo')


def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    return _confirmar_eliminacion(request, categoria, 'categoría', 'Catalogo')


def crear_talla(request):
    if request.method == 'POST':
        form = TallaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Talla creada correctamente')
            return redirect('Catalogo')
    else:
        form = TallaForm()

    return render(request, 'tienda/formulario.html', {
        'form': form,
        'titulo': 'Nueva talla',
    })


def editar_talla(request, id):
    talla = get_object_or_404(Talla, id=id)
    return _editar_objeto(request, talla, TallaForm, 'Editar talla', 'Catalogo')


def eliminar_talla(request, id):
    talla = get_object_or_404(Talla, id=id)
    return _confirmar_eliminacion(request, talla, 'talla', 'Catalogo')