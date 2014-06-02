# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Requerimiento
from .forms import RequerimientoForm

from iteraciones.models import Iteracion
from proyectos.models import Proyecto

@method_decorator(login_required)
def requerimientos(request, id_proyecto):
    requerimientos = Requerimiento.objects.filter(iteracion__proyecto = id_proyecto)
    return render(request, 'requerimientos.html', {'lista_de_requerimientos':requerimientos})

class AgregarRequerimiento(View):
    @method_decorator(login_required)
    def get(self, request):
        form = RequerimientoForm(jefe=request.user)
        return render(request, 'agregar-requerimiento.html', {'form': form})
    @method_decorator(login_required)
    def post(self, request):
        form = RequerimientoForm(request.POST, jefe=request.user)
        
        if form.is_valid():
            form.save(jefe=request.user)
            iteracion = get_object_or_404(Iteracion, pk = request.POST['iteracion'])
            proyecto = get_object_or_404(Proyecto, pk = iteracion.proyecto.pk)            
            messages.success(request, u"Requerimiento %s creado con exito " % request.POST['identificador'])
            return redirect(reverse('requerimientos', args= (iteracion.proyecto.pk,)))
        else:
            return render(request, 'agregar-requerimiento.html', {'form':form})


class EditarRequerimiento(View):
    @method_decorator(login_required)    
    def get(self, request, id_requerimiento):
        requerimiento = get_object_or_404(Requerimiento, pk = id_requerimiento)
        form = RequerimientoForm( instance = requerimiento, jefe = request.user)
        return render(request, 'editar-requerimiento.html', {'form': form, 'id_requerimiento': id_requerimiento})

    @method_decorator(login_required)    
    def post(self, request, id_requerimiento):
        requerimiento = get_object_or_404(Requerimiento, pk = id_requerimiento)
        p = request.POST
        
        form = RequerimientoForm(p, instance=requerimiento, jefe = request.user)
        if form.is_valid():
            form.save(jefe=request.user)
            messages.success(request, u"Requerimiento %s editado" % requerimiento.identificador)
            return redirect(reverse('requerimientos', args=(requerimiento.iteracion.proyecto.pk,)))
        else:
            return render(request, 'editar-requerimiento.html', {'form':form})

@method_decorator(login_required)
def borrarRequerimiento(request, id_requerimiento):
    requerimiento = get_object_or_404(Requerimiento, pk = id_requerimiento)
    iteracion = get_object_or_404(Iteracion, pk = requerimiento.iteracion.pk)
    messages.success(request, u"Requerimiento %s eliminado." % requerimiento.identificador)
    proyecto = get_object_or_404(Proyecto, pk = iteracion.proyecto.pk)  
    requerimiento.delete()
    return redirect (reverse("requerimientos", args=(proyecto.pk,)))

