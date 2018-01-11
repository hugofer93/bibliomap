from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.utils.encoding import iri_to_uri
from django.contrib.auth.models import User

from django.db import models

class Categoria(models.Model):
	nombre = models.CharField(max_length=45)
	descripcion = models.CharField(max_length=45, blank=True, null=True, verbose_name='descripción')
	estado = models.BooleanField(default=True, verbose_name='disponible')
	
	estado.boolean = True
	
	def __str__(self):
		return self.nombre

	def get_absolute_url(self):
		return iri_to_uri(reverse('categoria_detalle', args = [str(self.id)]))

	class Meta:
		ordering = ["nombre"]

class Seccion(models.Model):
	nombre = models.CharField(max_length=45)
	ubicacion = models.ImageField(upload_to='ubicacion')
	estado = models.BooleanField(default=True, verbose_name='disponible')
	
	estado.boolean = True

	def __str__(self):
		return self.nombre

	def get_absolute_url(self):
		return iri_to_uri(reverse('seccion_detalle', args = [str(self.id)]))
	
	class Meta:
		ordering = ["nombre"]
		verbose_name_plural = "secciones"

class Editorial(models.Model):
	nombre = models.CharField(max_length=45)
	ciudad = models.CharField(max_length=45, blank=True, null=True)
	pais = models.CharField(max_length=45, verbose_name='país', blank=True, null=True)
	estado = models.BooleanField(default=True, verbose_name='disponible')
	
	estado.boolean = True
	
	def __str__(self):
		return self.nombre
	
	class Meta:
		ordering = ["nombre","ciudad","pais"]
		verbose_name_plural = "editoriales"

class Autor(models.Model):
	nombre = models.CharField(max_length=45)
	apellido = models.CharField(max_length=45, blank=True, null=True)
	fecha_nacimiento = models.DateField(blank=True, null=True)
	estado = models.BooleanField(default=True, verbose_name='activo')
	
	estado.boolean = True
	
	def __str__(self):
		return (self.nombre+" "+self.apellido)
	
	class Meta:
		ordering = ["nombre","apellido","fecha_nacimiento"]
		verbose_name_plural = "autores"

class Libro(models.Model):
	codigo = models.CharField(max_length=10, verbose_name='código', blank=True, null=True)
	titulo = models.CharField(max_length=45, verbose_name='título')
	editorial = models.ForeignKey(Editorial)
	isbn = models.CharField(max_length=45, verbose_name='ISBN', blank=True, null=True)
	anio = models.CharField(max_length=4, verbose_name='año', blank=True, null=True)
	autores = models.ManyToManyField(Autor)
	editorial = models.ForeignKey(Editorial)
	categoria = models.ForeignKey(Categoria, verbose_name='categoría')
	prestamos = models.ManyToManyField(User, verbose_name='préstamo', through='Prestamo', through_fields=('libro','usuario'), related_name='prestamo_libro_usuario')
	reservaciones = models.ManyToManyField(User, verbose_name='reservacion', through='Reservacion', through_fields=('libro','usuario'), related_name='reservacion_libro_usuario')
	portada = models.ImageField(upload_to='portada', blank=True, null=True)
	seccion = models.ForeignKey(Seccion)
	estado = models.BooleanField(default=True, verbose_name='activo')

	estado.boolean = True
	
	def __str__(self):
		return (self.titulo)
	
	def get_absolute_url(self):
		return iri_to_uri(reverse('libro_detalle', args = [str(self.id)]))

	#no debe estar prestado ni reservado
	#si existe captura el valor, si no existe es False
	def disponible(self):
		try:
			prestado = self.prestamo_set.filter(estado=True)[0].estado
		except Exception:
			prestado = False
		try:
			reservado = self.reservacion_set.filter(estado=True)[0].estado
		except Exception:
			reservado = False			
		return (not (prestado or reservado))

	class Meta:
		ordering = ["titulo","editorial","anio"]

class Reservacion(models.Model):
	usuario = models.ForeignKey(User)
	libro = models.ForeignKey(Libro)
	fecha = models.DateField(auto_now_add=True)
	estado = models.BooleanField(default=True, verbose_name='activo')

	estado.boolean = True

	def __str__(self):
		return (self.usuario.username + " " + self.libro.titulo)

	def get_absolute_url(self):
		return iri_to_uri(reverse('reservacion_detalle', args = [str(self.id)]))
	
	class Meta:
		ordering = ["fecha", "usuario", "libro"]
		verbose_name_plural = "reservaciones"

class Prestamo(models.Model):
	usuario = models.ForeignKey(User)
	libro = models.ForeignKey(Libro)
	fecha_salida = models.DateField()
	fecha_devolucion = models.DateField(verbose_name='fecha devolución', blank=True, null=True)
	fecha_maxima = models.DateField(verbose_name='fecha máxima')
	estado = models.BooleanField(default=True, verbose_name='activo')
	
	estado.boolean = True
	
	def __str__(self):
		return (self.usuario.username + " " + self.libro.titulo)
	
	class Meta:
		ordering = ["fecha_salida", "usuario", "libro"]

class Parametro(models.Model):
	prestamo_casa = models.CharField(max_length=2, validators=[RegexValidator(r'^\d{1,2}$')])
	prestamo_clase = models.CharField(max_length=2, validators=[RegexValidator(r'^\d{1,2}$')])