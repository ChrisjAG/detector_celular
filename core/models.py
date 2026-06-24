from django.db import models

class Deteccion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Detección")
    objeto_detectado = models.CharField(max_length=100, verbose_name="Objeto Detectado")

    def __str__(self):
        return f"{self.objeto_detectado} detectado el {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
