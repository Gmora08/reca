from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib import messages

from .models import Iteracion
from proyectos.models import Proyecto

def iteraciones(request):
	iteraciones = Iteracion.objects.filter(proyecto = request.user.)
    return render(request, 'proyectos.html', {'lista_de_proyectos':proyectos})
