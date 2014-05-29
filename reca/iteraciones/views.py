# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib import messages

from .models import Iteracion
from .forms import IteracionForm

from proyectos.models import Proyecto

def iteraciones(request, id_proyecto):
    iteraciones = Iteracion.objects.filter(proyecto = id_proyecto)
    return render(request, 'iteraciones.html', {'lista_de_iteraciones':iteraciones})

class AgregarIteracion(View):
    def get(self, request):
        form = IteracionForm(usuario=request.user)
        return render(request, 'agregar-iteracion.html', {'form': form})
    def post(self, request):
        form = IteracionForm(request.POST, usuario=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, u"Iteracion %s creado con exito " % request.POST['identificador'])
            return redirect(reverse('iteraciones', args=(request.POST['proyecto'],)))
        else:
            return render(request, 'agregar-iteracion.html', {'form':form})

class EditarIteracion(View):
    def get(self, request, id_iteracion):
        iteracion = get_object_or_404(Iteracion, pk = id_iteracion, proyecto__encargado = request.user)
        form = IteracionForm( instance = iteracion, usuario = request.user)
        return render(request, 'editar-iteracion.html', {'form': form, 'id_iteracion': id_iteracion})
    def post(self, request, id_iteracion):
        iteracion = get_object_or_404(Iteracion, pk = id_iteracion, proyecto__encargado = request.user)
        p = request.POST
        
        form = IteracionForm(p, instance=iteracion, usuario = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, u"Iteracion %s editada" % iteracion.identificador)
            return redirect(reverse('iteraciones', args=(iteracion.proyecto.pk,)))
        else:
            return render(request, 'editar-iteracion.html', {'form':form})

def borrarIteracion(request, id_iteracion):
    iteracion = get_object_or_404(Iteracion, pk = id_iteracion, proyecto__encargado=request.user)
    proyecto = get_object_or_404(Proyecto, pk = iteracion.proyecto.pk)
    messages.success(request, u"Iteración %s eliminada." % iteracion.identificador)
    iteracion.delete()
    return redirect (reverse("iteraciones", args=(proyecto.pk,)))

