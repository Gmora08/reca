from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import ProyectoForm
from .models import Proyecto

#Agregado Iteracion para consulta de numero de iteraciones y requerimientos...
from iteraciones.models import Iteracion
from requerimientos.models import Requerimiento

def proyectos(request):
    print request.user.is_authenticated()
    print request.user.id
    Count = None
    proyectos = Proyecto.objects.filter(encargado = request.user.id).annotate(nIteraciones=Count('iteracion')).annotate(nRequerimientos=Count('requerimiento'))
    return render(request, 'proyectos.html', {'lista_de_proyectos':proyectos})  

class AgregarProyecto(View):
    def get(self, request):
        form = ProyectoForm()
        return render(request, 'agregar-proyecto.html', {'form':form})
    @method_decorator(login_required)
    def post(self, request):
        form = ProyectoForm(request.POST)

        validacion = validarDatosProyecto()
        listaDeErrores = validacion.validarDatosProy(request,0)
        if (form.is_valid() and len(listaDeErrores)==0):
            form.save(usuario=request.user)
            messages.success(request, u"Proyecto %s creado con exito " % request.POST['nombre'])
            return redirect(reverse('proyectos'))
        else:
            for error in listaDeErrores:
                messages.success(request, u"%s" % error)
            return render(request, 'agregar-proyecto.html', {'form':form})

class EditarProyecto(View):
    def get(self, request, id_proyecto):
        proyecto = get_object_or_404(Proyecto, pk=id_proyecto, encargado = request.user)
        form = ProyectoForm(instance=proyecto)
        return render(request, 'editar-proyecto.html', {'form':form})
    def post(self, request, id_proyecto):
        proyecto = get_object_or_404(Proyecto, pk=id_proyecto, encargado = request.user)
        form = ProyectoForm(request.POST, instance=proyecto)
        validacion = validarDatosProyecto()
        listaDeErrores = validacion.validarDatosProy(request,1)
        if (form.is_valid() and len(listaDeErrores)==0):
        
            form.save(usuario = proyecto.encargado)
            messages.success(request, u"Proyecto %s editado" % proyecto.nombre)
            return redirect(reverse('proyectos'))
        else:
            for error in listaDeErrores:
                messages.success(request, u"%s" % error)
            return render(request, 'editar-proyecto.html', {'form':form})


def borrarProyecto(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, pk=id_proyecto, encargado = request.user)
    proyecto.delete()
    messages.success(request, u"Proyecto eliminado")
    return redirect(reverse('proyectos'))   


#---------------------------------------------------------------------------------------------------
#Clase para validaciones de formularios de proyecto-------------------------------------------------
class validarDatosProyecto:
    @staticmethod
    def validarDatosProy(request,tipo):
        nombre=request.POST['nombre']
        #if 'fecha_de_inicio' in request.POST:
        fecha_de_inicio=request.POST['fecha_de_inicio']
        costo=request.POST['costo']
        objetivo=request.POST['objetivo']
        descripcion=request.POST['descripcion']
        cliente=request.POST['cliente']
        estado=request.POST['estado']

        listaDeErrores=[] #En esta lista se almacenan los errores del formulario para despues imprimirlos
        
        if(len(nombre)<4):
            listaDeErrores.append("El nombre del proyecto es muy corto, nombralo con almenos 4 caracteres")
        if(len(objetivo)<15):
            listaDeErrores.append("El objetivo es muy corto, especifique con almenos 15 caracteres")
        if(len(cliente)<4):
            listaDeErrores.append("El nombre del cliente es muy corto, especifique con almenos 4 caracteres")
        if(len(descripcion)<15):
            listaDeErrores.append("La descripcion es muy corta, debe contener almenos 15 caracteres")
    #Validacion COSTO solo numeros
        patron = re.compile('(\d*)[A-Za-z,-,_,$]+(\d*)') # Patron para buscar caracteres en las cadenas
        if patron.match(costo):
            listaDeErrores.append("El costo solo puede especificarse con numeros, por favor corrija los datos ingresados")
    
    #Validacion fecha_de_inicio
        patronFecha = re.compile('(\d{4})[/-](\d{2})[/-](\d{2})')
        if (patronFecha.match(fecha_de_inicio) == None):
            listaDeErrores.append("Debe introducir una fecha con formato: aaaa-mm-dd")
        else: #Si no se cumple el if anterior entonces la fecha tiene el formato corecto, ahora hay que comprobar que la persona no introduzca fechas incoherentes

                tomarAnio=re.compile('\d{4}')
                anio=tomarAnio.findall(fecha_de_inicio)

                tomar_mes_y_dia=re.compile('\d{2}')
                mes_y_dia=tomar_mes_y_dia.findall(fecha_de_inicio)  # Si la fecha es por ejemplo, 2014-05-24 entonces llena la lista de esta forma: ['20', '14', '05', '24']
                mesSeleccionado=int(mes_y_dia[2])
                diaSeleccionado=int(mes_y_dia[3])
                
                fechaHoy = date.today()
                anioActual=fechaHoy.year
                mesActual=fechaHoy.month
                diaActual=fechaHoy.day

                if (anioActual>int(anio[0]) or mesActual>mesSeleccionado or (diaActual-3)>diaSeleccionado):
                    listaDeErrores.append("No puede registrar proyectos con un retraso mayor a 3 dias")
        
        return listaDeErrores