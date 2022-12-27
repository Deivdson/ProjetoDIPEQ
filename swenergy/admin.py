from django.contrib import admin
from .models import Sensor, Fase, Consumo, Predio, Custo
# Register your models here.
admin.site.register(Sensor)
admin.site.register(Fase)
admin.site.register(Consumo)
admin.site.register(Predio)
admin.site.register(Custo)