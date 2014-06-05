# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Iteracion
from .forms import IteracionForm

from proyectos.models import Proyecto

#agregados import:
import re
from datetime import date
from .models import Proyecto


def iteraciones(request, id_proyecto):
    iteraciones = Iteracion.objects.filter(proyecto = id_proyecto)
    return render(request, 'iteraciones.html', {'lista_de_iteraciones':iteraciones})

class AgregarIteracion(View):
    def get(self, request):
        form = IteracionForm(usuario=request.user)
        return render(request, 'agregar-iteracion.html', {'form': form})

    def post(self, request):
        form = IteracionForm(request.POST, usuario=request.user)
        #modificacion para validaciones ----------------
        validacion=validarDatosIteracion()
        listaDeErrores=validacion.validarDatosIterac(request)

        if (form.is_valid() and len(listaDeErrores)==0):
            form.save()
            messages.success(request, u"Iteracion %s creado con exito " % request.POST['identificador'])
            return redirect(reverse('iteraciones', args=(request.POST['proyecto'],)))
        else:
            for error in listaDeErrores:
                messages.success(request, u"%s" % error)
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


#---------------------------------------------------------------------------------------------------
#Clase para validaciones de formularios de iteraciones-------------------------------------------------

class validarDatosIteracion:
    @staticmethod
    def validarDatosIterac(request):
        listaDeErrores=[] #En esta lista se almacenan los errores del formulario para despues imprimirlos
        identificador = request.POST['identificador']
        fecha_inicio_iter = request.POST['fecha_de_inicio']  # tipo unicode
        fecha_termino_iter =request.POST['fecha_de_termino']
        idproyecto=request.POST['proyecto']
        
        try:
            proyectoCorrespondiente = Proyecto.objects.filter(id=idproyecto)
            proyectoSeleccionado = 1  
            fechaInicioProyecto = proyectoCorrespondiente[0].fecha_de_inicio # tipo datetime
            anioProyecto =fechaInicioProyecto.year
            mesProyecto =fechaInicioProyecto.month
            diaProyecto =fechaInicioProyecto.day
            nombreProyecto = proyectoCorrespondiente[0].nombre
        except:
            proyectoSeleccionado = 0  
            if identificador == "":
                mensaje = "Debe seleccionar un proyecto para la iteracion."
            else:
                mensaje = "Debe seleccionar un proyecto para la iteracion << " + identificador + " >>"
            
            listaDeErrores.append(mensaje)    
        
        #Validacion de fecha_inicio_iter
        patronFecha = re.compile('(\d{4})[/-](\d{2})[/-](\d{2})')
        if ((patronFecha.match(fecha_inicio_iter) == None) or (patronFecha.match(fecha_termino_iter) == None)):
            listaDeErrores.append("Debe introducir una fecha con formato: aaaa-mm-dd")
        else: #La fecha tiene el formato corecto, ahora hay que comprobar que la persona no introduzca fechas incoherentes
            if proyectoSeleccionado ==1:
                regExpTomarAniodeIter = re.compile('\d{4}')
                anioInicioIter = regExpTomarAniodeIter.findall(fecha_inicio_iter)
                anioFinIter = regExpTomarAniodeIter.findall(fecha_termino_iter)

                rexpTomar_mes_y_dia_Iter = re.compile('\d{2}')
                
                mes_y_dia_InicioIter = rexpTomar_mes_y_dia_Iter.findall(fecha_inicio_iter)  # Si la fecha es por ejemplo, 2014-05-24 entonces llena la lista de esta forma: ['20', '14', '05', '24']
                mesInicioIter = int(mes_y_dia_InicioIter[2])
                diaInicioIter = int(mes_y_dia_InicioIter[3])
                
                mes_y_dia_FinIter = rexpTomar_mes_y_dia_Iter.findall(fecha_termino_iter)
                mesFinIter = int(mes_y_dia_FinIter[2])
                diaFinIter = int(mes_y_dia_FinIter[3])
                #Validando que la iteracion no tenga una fecha anterior al inicio del proyecto
                if ( diaInicioIter< diaProyecto or mesInicioIter< mesProyecto or anioInicioIter<anioProyecto):
                    mensaje = "El proyecto: << " + nombreProyecto + " >> fue agregado el " + fechaInicioProyecto.strftime('%d de  %b de  %Y') + ", recuerde que la iteracion no puede comenzar antes que el proyecto."
                    listaDeErrores.append(mensaje)
                
                if ( diaFinIter< diaProyecto or mesFinIter< mesProyecto or anioFinIter<anioProyecto):
                    mensaje = "El proyecto: << " + nombreProyecto + " >>  fue agregado el " + fechaInicioProyecto.strftime('%d de  %b de  %Y') + ", recuerde que la iteracion no puede terminar antes de que el proyecto inicie."
                    listaDeErrores.append(mensaje)
                #Validando que la iteracion no termine antes de que inicie
                if ( diaFinIter< diaInicioIter or mesFinIter< mesInicioIter or anioFinIter<anioInicioIter):
                    if identificador == "":
                        mensaje = "La fecha de terimno de la iteracion no puede ser menor a su fecha de inicio."
                    else:
                        mensaje = "La fecha de terimno de la iteracion << " + identificador + " >> no puede ser menor a su fecha de inicio."
                    listaDeErrores.append(mensaje)


        return listaDeErrores