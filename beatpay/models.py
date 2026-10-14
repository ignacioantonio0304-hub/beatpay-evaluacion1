from django.db import models
from django.contrib.auth.models import User

class TarjetaVirtual(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    numero_tarjeta = models.CharField(max_length=16, unique=True, verbose_name="Número de Tarjeta")
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Saldo Actual ($)")
    cvv = models.CharField(max_length=3, verbose_name="CVV")
    fecha_expiracion = models.CharField(max_length=5, verbose_name="Fecha Expiración (MM/AA)")
    activa = models.BooleanField(default=True, verbose_name="¿Está Activa?")

    def __str__(self):
        return f"Tarjeta de {self.usuario.username} - **** {self.numero_tarjeta[-4:]}"

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('carga', 'Carga de Fondos'),
        ('pago', 'Pago en Comercio/Evento'),
    ]

    tarjeta = models.ForeignKey(TarjetaVirtual, on_delete=models.CASCADE, related_name='transacciones', verbose_name="Tarjeta")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo de Transacción")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto ($)")
    comercio_destino = models.CharField(max_length=100, blank=True, null=True, verbose_name="Comercio o Evento")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    def __str__(self):
        return f"{self.get_tipo_display()} - ${self.monto} ({self.fecha.strftime('%d/%m/%Y %H:%M')})"