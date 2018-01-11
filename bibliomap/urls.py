"""bibliomap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from bibliomap import views

urlpatterns = [
    url(r'^$', views.Inicio.as_view(template_name='inicio.html'), name='inicio'),
    url(r'^admin/', admin.site.urls),
    url(r'^completado/$', TemplateView.as_view(template_name='completado.html'), name='completado'),
    
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'inicio'}, name='logout'),
    
    url(r'^libro/$', views.Libro.as_view(), name='libro'),
    url(r'^libro/id/(?P<id>\d+)$', views.LibroDetalle.as_view(), name='libro_detalle'),

    url(r'^categoria/$', views.Categoria.as_view(), name='categoria'),
    url(r'^categoria/id/(?P<id>\d+)$', views.CategoriaDetalle.as_view(), name='categoria_detalle'),

    url(r'^seccion/$', views.Seccion.as_view(), name='seccion'),
    url(r'^seccion/id/(?P<id>\d+)$', views.SeccionDetalle.as_view(), name='seccion_detalle'),    

    url(r'^buscar/(?P<buscar>\w+)$', views.Buscar.as_view(), name='buscar'),
    
    url(r'^libro/id/(?P<id>\d+)/prestamo/$', views.Prestamo.as_view(), name='prestamo'),
    url(r'^prestamos/$', views.Prestamos.as_view(), name='prestamos'),

    url(r'^libro/id/(?P<id>\d+)/reservacion/$', views.Reservacion.as_view(), name='reservacion'),
    url(r'^reservacion/id/(?P<id>\d+)$', views.ReservacionDetalle.as_view(), name='reservacion_detalle'),
    url(r'^reservaciones/$', views.Reservaciones.as_view(), name='reservaciones'),

    url(r'^devolucion/pendientes/$', views.Devoluciones.as_view(), name='devoluciones'),
]


from bibliomap.settings import DEBUG

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
