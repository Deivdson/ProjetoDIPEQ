from django.contrib import admin
from .models import Sensor, Fase, Consumo
# Register your models here.
admin.site.register(Sensor)
admin.site.register(Fase)
admin.site.register(Consumo)