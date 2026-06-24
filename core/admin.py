from django.contrib import admin
from .models import Deteccion

@admin.register(Deteccion)
class DeteccionAdmin(admin.ModelAdmin):
    list_display = ('objeto_detectado', 'fecha')
    search_fields = ('objeto_detectado',)
    list_filter = ('fecha',)
