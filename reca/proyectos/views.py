from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib import messages

from .forms import ProyectoForm
from .models import Proyecto

def proyectos(request):
    print request.user.is_authenticated()
    # proyectos = Proyecto.objects.filter(encargado = request.user)
    return render(request, 'proyectos.html', {'lista_de_proyectos':proyectos})  

class AgregarProyecto(View):
    def get(self, request):
        form = ProyectoForm()
        return render(request, 'agregar-proyecto.html', {'form':form})
    def post(self, request):
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save(encargado=request.user.id)
            messages.success(request, u"Proyecto %s creado con exito" % request.POST['nombre'])
            return redirect(reverse('proyectos'))
        else:
            messages.error(request, u"Verifica los datos ingresados")
            return render(request, 'agregar-proyecto.html', {'form':form})



