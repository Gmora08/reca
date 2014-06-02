# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import AuthenticationForm, RegistrationForm, RegistrationFormAnalista
from .models import User

import re
from datetime import date

class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            django_login(request, user)
            return redirect(reverse('proyectos'))
                
        else:
            messages.error(request, u'Usuario/Password incorrectos')
            return redirect(reverse('login'))

class Registro(View):
    def get(self, request):
       
        form = RegistrationForm()
        return render(request, 'registro.html', {'form':form})
    def post(self, request):
        form = RegistrationForm(request.POST)
        validacion=ValidarDatosRegistroUsuarios()
        listaDeErrores=validacion.validarRegistro(request)
        if (form.is_valid() and len(listaDeErrores)==0):
            messages.success(request, u"%s ,se ha registrado con exito, ahora puede iniciar sesión " % request.POST['nombre'])
            form.save()
            return redirect(reverse('login'))
        else:
            for error in listaDeErrores:
                messages.success(request, u"%s" % error)
            return render(request, 'registro.html', {'form':form})
@method_decorator(login_required)
def analistas(request):
    if not request.user.jefe:
        analistas = User.objects.filter(jefe = request.user.id)
        return render(request, 'analistas.html', {'lista_de_analistas':analistas}) 
    else:
        return redirect(reverse('requerimientos-analista'))

class AgregarAnalista(View):
    @method_decorator(login_required)
    def get(self, request):
        form = RegistrationFormAnalista()
        return render(request, 'agregar-analista.html', {'form':form})

    @method_decorator(login_required)
    def post(self, request):
        form = RegistrationFormAnalista(request.POST)
        validacion = ValidarDatosRegistroUsuarios()
        listaDeErrores = validacion.validarRegistro(request)
 
        if (form.is_valid() and len(listaDeErrores)==0):
            form.save(jefe=request.user)
            messages.success(request, u"Analista %s creado con exito " % request.POST['nombre'])
            return redirect(reverse('proyectos'))
        else:
            for error in listaDeErrores:
                messages.success(request, u"%s" % error)
            return render(request, 'agregar-analista.html', {'form':form})


class EditarAnalista(View):
    @method_decorator(login_required)
    def get(self, request, id_analista):
        analista = get_object_or_404(User, pk=id_analista, jefe = request.user)
        form = RegistrationFormAnalista(instance=analista)
        return render(request, 'editar-analista.html', {'form':form})

    @method_decorator(login_required)
    def post(self, request, id_analista):
        analista = get_object_or_404(User, pk=id_analista, jefe = request.user)
        form = RegistrationFormAnalista(request.POST, instance=analista)

        validacion=ValidarDatosRegistroUsuarios()
        listaDeErrores=validacion.validarRegistro(request)

        if (form.is_valid() and len(listaDeErrores)==0):

            form.save(jefe = analista.jefe)
            messages.success(request, u"Analista %s editado" % analista.nombre)
            return redirect(reverse('analistas'))
        else:
            for error in listaDeErrores:
                messages.success(request, u"%s" % error)
            return render(request, 'editar-analista.html', {'form':form})
@method_decorator(login_required)
def borrarAnalista(request, id_analista):
    analista = get_object_or_404(User, pk=id_analista, jefe = request.user)
    analista.delete()
    messages.success(request, u"Analista eliminado")
    return redirect(reverse('analistas'))


def logout(request):
    """
    Log out view
    """
    django_logout(request)
    return redirect(reverse('home'))

def home(request):
    return redirect(reverse('login'))

# -------------------------------------------------------------------------------------------
# Clase en la que se definen los metodos para las validaciones de formularios: ---------------

class ValidarDatosRegistroUsuarios:
    
    #Validaciones para clase: Registro
    @staticmethod
    def validarRegistro(request):
        nombre=request.POST['nombre']
        apellidoP=request.POST['apellido_paterno']
        apellidoM=request.POST['apellido_materno']
        pass1=request.POST['password1']
        pass2=request.POST['password2']
        fechaNac=request.POST['fecha_de_nacimiento']
        #print fechaNac
        listaDeErrores=[] #En esta lista se almacenan los errores del formulario para despues imprimirlos
        
    #NOMBRE Y APELLIDOS  (Verificar tamaño>2 y sin numeros)
        patron = re.compile('([a-zA-Z]*)\d+([a-zA-Z]*)') # Patron para buscar numeros en las cadenas
        if (patron.match(nombre) or patron.match(apellidoP) or patron.match(apellidoM) or len(nombre)<3 or len(apellidoP)<3 or len(apellidoM)<3):
            listaDeErrores.append("Nombre, Apellido paterno y Apellido materno no admiten numeros y deben contener almenos 3 caracteres")
    #CONTRASEÑA
        if (pass1 != pass2):
            listaDeErrores.append("Su password no coincide, intente nuevamente.")
        if (len(pass1)<5):
            listaDeErrores.append("Su password debe contener al menos 4 numeros o caracteres")
    #FECHA DE NACIMIENTO
        patronFecha = re.compile('(\d{4})[/-](\d{2})[/-](\d{2})')
        if (patronFecha.match(fechaNac) == None):
            listaDeErrores.append("Debe introducir una fecha con formato: aaaa-mm-dd")
        
        #Si no se cumple el if anterior entonces la fecha tiene el formato corecto, ahora hay que comprobar que la persona no introduzca fechas incoherentes
        else:  
            tomarAnio=re.compile('\d{4}')
            anio=tomarAnio.findall(fechaNac)
            fechaHoy = date.today()
            print fechaHoy
            anioMaximo=fechaHoy.year-40
            print anioMaximo
            anioMinimo=fechaHoy.year-20
            print anioMinimo

            if (int(anio[0])>anioMinimo or int(anio[0])<anioMaximo):
                listaDeErrores.append("Para poder trabajar en esta empresa debe tener entre 20 y 40 anios")

        return listaDeErrores
