from django import forms
from .models import Iteracion
from proyectos.models import Proyecto

class IteracionForm(forms.ModelForm):
    class Meta :
        model = Iteracion

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')
        super(IteracionForm, self).__init__(*args, **kwargs)

        self.fields['proyecto'].queryset = Proyecto.objects.filter(encargado=usuario)

