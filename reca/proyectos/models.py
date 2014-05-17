from django.db import models
from usuarios.models import User

class Proyecto(models.Model):
	nombre = models.CharField(max_length=255)
	fecha_de_inicio = models.DateField()
	fecha_de_termino = models.DateField(blank=True, null=True)
	costo = models.FloatField(blank=True, null=True)
	objetivo = models.TextField(blank=True, null=True)
	descripcion = models.CharField(max_length=255, blank=True, null=True)
	cliente = models.CharField(max_length=255, blank=True,null=True)
	porcentaje = models.FloatField(verbose_name=u'Porcentaje de avance', default=0.00, editable=False)
	encargado = models.ForeignKey(User, editable=False)
	ESTADO_CHOICES = (
		('A','Atrasado'),
		('N','Normal'),
		('AP','Alta prioridad'),		
	)
	estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)

	

	def __unicode__(self):
		return self.nombre