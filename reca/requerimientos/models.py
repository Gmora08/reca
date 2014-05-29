from django.db import models
from iteraciones.models import Iteracion
from usuarios.models import User


class Requerimiento(models.Model):
	identificador = models.CharField(max_length=255)
	descripcion = models.CharField(max_length=255)
	TIPO_REQUERIMIENTO = (
		('F','Funcional'),
		('NF','No Funcional'),
	)
	tipo = models.CharField(max_length=2, choices = TIPO_REQUERIMIENTO)
	ESTADO_REQUERIMIENTO = (
		('a','Atrasado'),
		('A','Asignado'),
		('I','Identificado'),
		('T', 'Terminado')
	)
	estado = models.CharField(max_length=2, choices=ESTADO_REQUERIMIENTO, default="I")
	fecha_de_inicio = models.DateField()
	fecha_de_termino = models.DateField()
	OPCIONES = (
		('A','Alta'),
		('M','Media'),
		('B','Baja'),
	)
	madurez = models.CharField(max_length=1, choices=OPCIONES)
	volatilidad = models.CharField(max_length=1, choices=OPCIONES)
	complejidad = models.CharField(max_length=1, choices=OPCIONES)
	prioridad = models.CharField(max_length=1, choices=OPCIONES)
	jefe_de_analistas = models.ForeignKey(User, editable=False, related_name="jefe_de_analistas")
	analista_asignado = models.ForeignKey(User, blank=True, null=True, related_name="analista_asignado")
	iteracion = models.ForeignKey(Iteracion, null=True, blank=True)

