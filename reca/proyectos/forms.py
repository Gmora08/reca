from django import forms
from .models import Proyecto
from django.forms.fields import DateField


class ProyectoForm(forms.ModelForm):
    
    def save(self, usuario=None):
        self.instance.encargado = usuario
        super(ProyectoForm,self).save()

    class Meta:
        model = Proyecto

        