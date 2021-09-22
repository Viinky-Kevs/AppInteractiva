from django.db import models

class Nombre(models.Model):
	nombre = models.CharField(max_length = 20)

	def __str__(self):
		return self.nombre

class archivo(models.Model):
	nombre = models.CharField(max_length = 50)
	tipo = models.CharField(max_length = 10)
	cantidad = models.IntegerField()
	pregunta = models.BooleanField()
	eliminar = models.ForeignKey(Nombre, on_delete = models.PROTECT)
	media = models.FileField(upload_to = 'myfolder/', blank = True, null = True)

	def __str__(self):
		return self.nombre