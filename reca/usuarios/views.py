# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth import login as django_login, authenticate, logout as django_logout

from .forms import AuthenticationForm, RegistrationForm

class Login(View):
	def get(self, request):
		form = AuthenticationForm()
		return render(request, 'login.html', {'form':form})
	def post(self, request):
		form = AuthenticationForm(request.POST)
		if form.is_valid():
			user = authenticate(email=request.POST['email'], password=request.POST['password'])
			if user is not None:
				return redirect(reverse('proyectos'))
				
			else:
				messages.error(request, u'Usuario/Password incorrectos')
				return render(request, 'login.html', {'form': form})

		else:
			messages.error(request, u'Usuario/Password incorrectos')
			return render(request, 'login.html', {'form': form})

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

def logout(request):
    """
    Log out view
    """
    django_logout(request)
    return redirect(reverse('home'))

def home(request):
	return redirect(reverse('login'))
