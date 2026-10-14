from django.contrib import admin
from .models import TarjetaVirtual, Transaccion

@admin.register(TarjetaVirtual)
class TarjetaVirtualAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'numero_tarjeta', 'saldo', 'activa')
    search_fields = ('numero_tarjeta', 'usuario__username', 'usuario__email')
    list_filter = ('activa',)

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tarjeta', 'tipo', 'monto', 'comercio_destino', 'fecha')
    search_fields = ('comercio_destino', 'tarjeta__numero_tarjeta')
    list_filter = ('tipo', 'fecha')