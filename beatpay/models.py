import uuid
from django.db import models

class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=120)
    email = models.EmailField(max_length=150)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.rut})"

class Banco(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nombre

class Tarjeta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='tarjetas')
    numero_enmascarado = models.CharField(max_length=25)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=20, default='Activa') # Activa, Bloqueada, Inactiva

    def __str__(self):
        return f"{self.numero_enmascarado} - {self.cliente.nombre}"

class InstrumentoFinanciero(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    banco = models.ForeignKey(Banco, on_delete=models.SET_NULL, null=True, blank=True)
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.SET_NULL, null=True, blank=True)
    identificador_externo = models.CharField(max_length=150, null=True, blank=True)
    tipo = models.CharField(max_length=30)
    es_interno = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} ({'Interno' if self.es_interno else 'Externo'})"

class Movimiento(models.Model):
    tarjeta_uuid_origen = models.ForeignKey(
        InstrumentoFinanciero, 
        on_delete=models.CASCADE, 
        related_name='movimientos_origen'
    )
    tarjeta_uuid_destino = models.ForeignKey(
        InstrumentoFinanciero, 
        on_delete=models.CASCADE, 
        related_name='movimientos_destino'
    )
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='Completado') # Completado, Pendiente, Rechazado
    referencia_operacion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"${self.monto} - {self.estado}"