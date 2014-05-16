from django.forms import ModelForm
from .models import Proyecto

class ProyectoForm(ModelForm):
	def save(self, usuario=None):
		self.instance.encargado = usuario
		super(ProyectoForm,self).save()

	class Meta:
		model = Proyecto
		fields = '__all__'
