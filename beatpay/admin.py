from django.contrib import admin
from .models import Cliente, Banco, Tarjeta, InstrumentoFinanciero, Movimiento

admin.site.register(Cliente)
admin.site.register(Banco)
admin.site.register(Tarjeta)
admin.site.register(InstrumentoFinanciero)
admin.site.register(Movimiento)