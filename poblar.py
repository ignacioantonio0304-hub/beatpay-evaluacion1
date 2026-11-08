import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicpro_project.settings')
django.setup()

from beatpay.models import Cliente, Banco, Tarjeta, InstrumentoFinanciero, Movimiento

print("Cargando datos de prueba...")

# 1. Bancos
banco_bch, _ = Banco.objects.get_or_create(nombre="Banco de Chile", codigo="BCH")
banco_tenpo, _ = Banco.objects.get_or_create(nombre="Tenpo Prepago", codigo="TENPO")
banco_mach, _ = Banco.objects.get_or_create(nombre="MACH Bci", codigo="MACH")

# 2. Clientes
cli1, _ = Cliente.objects.get_or_create(rut="19.876.543-2", nombre="Ignacio Hidalgo", email="ignacio.hidalgo@musicpro.cl")
cli2, _ = Cliente.objects.get_or_create(rut="20.123.456-7", nombre="Almendra González", email="almendra@ejemplo.cl")

# 3. Tarjetas
t1, _ = Tarjeta.objects.get_or_create(cliente=cli1, numero_enmascarado="**** **** **** 1726", saldo=55500.00, estado="Activa")
t2, _ = Tarjeta.objects.get_or_create(cliente=cli2, numero_enmascarado="**** **** **** 9012", saldo=120000.00, estado="Activa")

# 4. Instrumentos Financieros
inst_origen, _ = InstrumentoFinanciero.objects.get_or_create(banco=banco_mach, tarjeta=t1, tipo="Tarjeta Virtual", es_interno=True)
inst_destino, _ = InstrumentoFinanciero.objects.get_or_create(banco=banco_tenpo, tarjeta=t2, tipo="Cuenta Prepago", es_interno=False)

# 5. Movimientos
Movimiento.objects.get_or_create(tarjeta_uuid_origen=inst_origen, tarjeta_uuid_destino=inst_destino, monto=15000.00, estado="Completado", referencia_operacion="REF-001")
Movimiento.objects.get_or_create(tarjeta_uuid_origen=inst_origen, tarjeta_uuid_destino=inst_destino, monto=22000.00, estado="Completado", referencia_operacion="REF-002")

print("¡Datos cargados exitosamente!")