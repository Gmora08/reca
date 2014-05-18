from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib import messages

from .forms import ProyectoForm
from .models import Proyecto

def proyectos(request):
    print request.user.is_authenticated()
    print request.user.nombre
    print request.user.id
    proyectos = Proyecto.objects.filter(encargado = request.user.id)
    return render(request, 'proyectos.html', {'lista_de_proyectos':proyectos})  

class AgregarProyecto(View):
    def get(self, request):
        form = ProyectoForm()
        return render(request, 'agregar-proyecto.html', {'form':form})
    def post(self, request):
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save(usuario=request.user)
            messages.success(request, u"Proyecto %s creado con exito " % request.POST['nombre'])
            return redirect(reverse('proyectos'))
        else:
            messages.error(request, u"Verifica los datos ingresados")
            return render(request, 'agregar-proyecto.html', {'form':form})

class EditarProyecto(View):
    def get(self, request, id_proyecto):
        proyecto = get_object_or_404(Proyecto, pk=id_proyecto, encargado = request.user)
        form = ProyectoForm(instance=proyecto)
        return render(request, 'editar-proyecto.html', {'form':form})
    def post(self, request, id_proyecto):
        proyecto = get_object_or_404(Proyecto, pk=id_proyecto, encargado = request.user)
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save(usuario = proyecto.encargado)
            messages.success(request, u"Proyecto %s editado" % proyecto.nombre)
            return redirect(reverse('proyectos'))
        else:
            return render(request, 'editar-proyecto.html', {'form':form})


def borrarProyecto(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, pk=id_proyecto, encargado = request.user)
    proyecto.delete()
    messages.success(request, u"Proyecto eliminado")
    return redirect(reverse('proyectos'))   