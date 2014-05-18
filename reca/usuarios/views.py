# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth import login as django_login, authenticate, logout as django_logout

from .forms import AuthenticationForm, RegistrationForm, RegistrationFormAnalista
from .models import User

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
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
        else:
            return render(request, 'registro.html', {'form':form})

def analistas(request):
    print request.user.jefe
    if not request.user.jefe:
        analistas = User.objects.filter(jefe = request.user.id)
        return render(request, 'analistas.html', {'lista_de_analistas':analistas}) 
    else:
        return HttpResponse('No tienes permisos para ver esta zona')

class AgregarAnalista(View):
    def get(self, request):
        form = RegistrationFormAnalista()
        return render(request, 'agregar-analista.html', {'form':form})
    def post(self, request):
        form = RegistrationFormAnalista(request.POST)
        if form.is_valid():
            form.save(jefe=request.user)
            messages.success(request, u"Analista %s creado con exito " % request.POST['nombre'])
            return redirect(reverse('proyectos'))
        else:
            messages.error(request, u"Verifica los datos ingresados")
            return render(request, 'agregar-analista.html', {'form':form})

class EditarAnalista(View):
    def get(self, request, id_analista):
        analista = get_object_or_404(User, pk=id_analista, jefe = request.user)
        form = RegistrationFormAnalista(instance=analista)
        return render(request, 'editar-analista.html', {'form':form})
    def post(self, request, id_analista):
        analista = get_object_or_404(User, pk=id_analista, jefe = request.user)
        form = RegistrationFormAnalista(request.POST, instance=analista)
        if form.is_valid():
            form.save(jefe = analista.jefe)
            messages.success(request, u"Analista %s editado" % analista.nombre)
            return redirect(reverse('analistas'))
        else:
            return render(request, 'editar-analista.html', {'form':form})


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
