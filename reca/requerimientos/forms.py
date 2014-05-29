from django import forms
from .models import Requerimiento
from iteraciones.models import Iteracion
from proyectos.models import Proyecto
from usuarios.models import User

class RequerimientoForm(forms.ModelForm):
    
    def save(self, jefe=None):
        self.instance.jefe_de_analistas = jefe
        super(RequerimientoForm,self).save()

    class Meta:
        model = Requerimiento

    def __init__(self, *args, **kwargs):
        jefe = kwargs.pop('jefe')
        super(RequerimientoForm, self).__init__(*args, **kwargs)

        self.fields['iteracion'].queryset = Iteracion.objects.filter(proyecto__encargado=jefe)
        self.fields['analista_asignado'].queryset = User.objects.filter(jefe=jefe)

        

