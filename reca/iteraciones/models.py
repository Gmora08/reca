from django.db import models
from proyectos.models import Proyecto

class Iteracion(models.Model):
	identificador = models.CharField(max_length=255)
	fecha_de_inicio = models.DateField()
	fecha_de_termino = models.DateField()
	porcentaje = models.FloatField(default=0.0, editable=False)
	proyecto = models.ForeignKey(Proyecto)

	def __unicode__(self):
		return self.identificador