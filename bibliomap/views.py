from datetime import date

from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.utils.encoding import iri_to_uri
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from bibliomap import models
from bibliomap import suma_dias

class Inicio(TemplateView):
	template_name = 'inicio.html'

	def get_context_data(self, **kwargs):
		context = super(Inicio, self).get_context_data(**kwargs)
		try:
			context['libro'] = models.Libro.objects.all().filter(estado=True)
		except Exception:
			pass

		try:
			context['categoria'] = models.Categoria.objects.all().filter(estado=True)
		except Exception:
			pass

		try:
			context['seccion'] = models.Seccion.objects.all().filter(estado=True)
		except Exception:
			pass

		if self.request.user.is_authenticated():
			try:
				context['reservacion'] = models.Reservacion.objects.all().filter(usuario=self.request.user).exclude(estado=False)
			except Exception:
				pass

			try:
				prestamo = models.Prestamo.objects.all().filter(usuario=self.request.user)
				context['devolucion_pendiente'] = prestamo.filter(estado=True)
				context['prestamo'] = prestamo.filter(estado=False)
			except Exception:
				pass
		return context

class Libro(ListView):
	model = models.Libro
	template_name = 'libro.html'
	queryset = model.objects.all().filter(estado=True)

class LibroDetalle(DetailView):
	model = models.Libro
	template_name = 'libro_detalle.html'
	pk_url_kwarg = 'id'

class Categoria(ListView):
	model = models.Categoria
	template_name = 'categoria.html'
	queryset = model.objects.all().filter(estado=True)

class CategoriaDetalle(DetailView):
	model = models.Categoria
	template_name = 'categoria_detalle.html'
	pk_url_kwarg = 'id'

	def get_context_data(self, **kwargs):
		context = super(CategoriaDetalle, self).get_context_data(**kwargs)
		categoria = context['object']
		context['object_list'] = categoria.libro_set.all().filter(estado=True)
		return context

class Seccion(ListView):
	model = models.Seccion
	template_name = 'seccion.html'
	queryset = model.objects.all().filter(estado=True)

class SeccionDetalle(DetailView):
	model = models.Seccion
	template_name = 'seccion_detalle.html'
	pk_url_kwarg = 'id'

	def get_context_data(self, **kwargs):
		context = super(SeccionDetalle, self).get_context_data(**kwargs)
		seccion = context['object']
		context['object_list'] = seccion.libro_set.all().filter(estado=True)
		return context

class Buscar(ListView):
	model = models.Libro
	template_name = 'buscar.html'
	queryset = None

	def get_queryset(self):
		parametro = self.kwargs['buscar']
		if parametro:
			qset = (
				Q(titulo__icontains=parametro) |
				Q(autores__nombre__icontains=parametro) |
				Q(autores__apellido__icontains=parametro)
			)
			queryset = self.model.objects.filter(qset).distinct().exclude(estado=False)
			return queryset
		else:
			return HttpResponseRedirect('/')

class Prestamo(LoginRequiredMixin, DetailView):
	model = models.Libro
	template_name = 'prestamo.html'
	pk_url_kwarg = 'id'

	def get_context_data(self, **kwargs):
		context = super(Prestamo, self).get_context_data(**kwargs)
		context['parametro'] = models.Parametro.objects.all()[0]
		return context

	def post(self, request, *args, **kwargs):
		try:
			libro = self.model.objects.get(id=self.request.POST['libro'])
		except Exception:
			libro = None
		if libro and self.request.user.is_authenticated()==True:
			user = self.request.user
			dias_prestamo = int(self.request.POST['prestamo'])
			fecha_salida = date.today()
			fecha_maxima = suma_dias.addworkdays(fecha_salida,dias_prestamo)
			prestamo = models.Prestamo(usuario=user,
										libro=libro,
										fecha_salida=fecha_salida,
										fecha_maxima=fecha_maxima,
										estado=True)
			prestamo.save()
			return HttpResponseRedirect(iri_to_uri(reverse('completado')))
		else:
			return HttpResponseRedirect(iri_to_uri(reverse('inicio')))

class Prestamos(LoginRequiredMixin, ListView):
	model = models.Prestamo
	template_name = 'prestamos.html'
	queryset = None

	def get_queryset(self):
		queryset = self.model.objects.filter(usuario=self.request.user).exclude(estado=True)
		return queryset

class PrestamoDetalle(LoginRequiredMixin, DetailView):
	model = models.Prestamo
	template_name = 'prestamo_detalle.html'
	pk_url_kwarg = 'id'

class Reservacion(LoginRequiredMixin, DetailView):
	model = models.Libro
	template_name = 'reservacion.html'
	pk_url_kwarg = 'id'

	def post(self, request, *args, **kwargs):
		try:
			libro = self.model.objects.get(id=self.request.POST['libro'])
		except Exception:
			libro = None
		if libro and self.request.user.is_authenticated()==True:
			user = self.request.user
			reservacion = models.Reservacion(usuario=user,
											libro=libro,
											estado=True)
			reservacion.save()
			return HttpResponseRedirect(iri_to_uri(reverse('completado')))
		else:
			return HttpResponseRedirect('')

class Reservaciones(LoginRequiredMixin, ListView):
	model = models.Reservacion
	template_name = 'reservaciones.html'
	queryset = None

	def get_queryset(self):
		queryset = self.model.objects.filter(usuario=self.request.user).exclude(estado=False)
		return queryset

class ReservacionDetalle(LoginRequiredMixin, DetailView):
	model = models.Reservacion
	template_name = 'reservacion_detalle.html'
	pk_url_kwarg = 'id'

	def post(self, request, *args, **kwargs):
		try:
			if self.kwargs['id']==self.request.POST['reservacion']:
				id = self.kwargs['id']
				reservacion = self.model.objects.get(id=id)
		except Exception:
			reservacion = None
		if reservacion and reservacion.estado and self.request.user.is_authenticated():
			reservacion.estado = False
			reservacion.save()
			return HttpResponseRedirect(iri_to_uri(reverse('completado')))
		else:
			return HttpResponseRedirect(iri_to_uri(reverse('inicio')))

class Devoluciones(LoginRequiredMixin, ListView):
	model = models.Prestamo
	template_name = 'devoluciones.html'
	queryset = None

	def get_queryset(self):
		queryset = self.model.objects.filter(usuario=self.request.user).exclude(estado=False)
		return queryset
