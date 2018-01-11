from django.contrib import admin

from bibliomap import models

class AdminSite(admin.AdminSite):
    admin.AdminSite.site_header = "Administracion BiblioMap"
    admin.AdminSite.site_title = "Administracion BiblioMap"

admin.site.disable_action('delete_selected')

@admin.register(models.Categoria)
class AdminCategoria(admin.ModelAdmin):
    list_display = ["nombre","descripcion","estado"]
    list_display_link = ["nombre"]
    search_fields = ["nombre"]
    list_filter = ["estado"]

@admin.register(models.Seccion)
class AdminSeccion(admin.ModelAdmin):
    list_display = ["nombre","estado"]
    list_display_link = ["nombre"]
    search_fields = ["nombre"]
    list_filter = ["estado"]

@admin.register(models.Autor)
class AdminEscritor(admin.ModelAdmin):
    list_display = ["nombre","apellido","estado"]
    list_display_link = ["nombre"]
    search_fields = ["nombre","apellido"]
    list_filter = ["estado"]
    ordering = ["nombre","apellido"]

@admin.register(models.Editorial)
class AdminEditorial(admin.ModelAdmin):
    list_display = ["nombre","ciudad","pais"]
    list_display_link = ["nombre"]
    search_fields = ["nombre","ciudad","pais"]
    list_filter = ["estado"]
    ordering = ["nombre","ciudad","pais"]
    ordering = ["nombre"]
    
@admin.register(models.Libro)
class AdminLibro(admin.ModelAdmin):
    list_display = ["titulo","editorial","isbn","estado"]
    list_display_link = ["titulo"]
    search_fields = ["titulo","editorial","isbn"]
    list_filter = ["estado"]
    ordering = ["titulo","editorial"]

@admin.register(models.Prestamo)
class AdminPrestamo(admin.ModelAdmin):
    list_display = ["usuario","libro","fecha_salida","fecha_devolucion","estado"]
    list_display_link = ["usuario"]
    search_fields = ["usuario__username","libro__titulo","fecha_salida","fecha_devolucion"]
    list_filter = ["estado"]
    ordering = ["usuario","libro","fecha_salida"]

@admin.register(models.Reservacion)
class AdminReservacion(admin.ModelAdmin):
    list_display = ["usuario","libro","fecha","estado"]
    list_display_link = ["usuario"]
    search_fields = ["usuario__nombre","libro","fecha"]
    list_filter = ["estado"]
    ordering = ["usuario","libro","fecha"]

@admin.register(models.Parametro)
class AdminParametro(admin.ModelAdmin):
    list_display = ["prestamo_casa","prestamo_clase"]
    list_display_link = ["prestamo_casa"]