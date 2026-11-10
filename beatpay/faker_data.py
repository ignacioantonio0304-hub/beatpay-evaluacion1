import os
import sys
import django
from decimal import Decimal
from faker import Faker

# Añadir el directorio raíz del proyecto al path para reconocer 'musicpro_project'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicpro_project.settings')
django.setup()

from beatpay.models import Cliente, Tarjeta, InstrumentoFinanciero, Movimiento

fake = Faker('es_CL')

def calcular_dv(rut_num):
    """Calcula el dígito verificador oficial de un RUT chileno."""
    s = 0
    m = 2
    for d in reversed(str(rut_num)):
        s += int(d) * m
        m = m + 1 if m < 7 else 2
    res = 11 - (s % 11)
    if res == 11:
        return '0'
    elif res == 10:
        return 'K'
    return str(res)

def generar_rut_unico(i):
    """Genera un RUT único secuencial basado en el índice i."""
    rut_num = 5000000 + i
    dv = calcular_dv(rut_num)
    # Formatear con puntos y guion (ej: 5.000.001-K)
    rut_str = f"{rut_num:,}".replace(",", ".")
    return f"{rut_str}-{dv}"

def poblar_base_datos(cantidad=10000):
    print(f"🚀 Generando {cantidad} usuarios falsos para BeatPay...")

    for i in range(1, cantidad + 1):
        nombre = fake.name()
        email = f"usuario_{i}_{fake.word()}@musicpro.cl"
        rut = generar_rut_unico(i)
        
        cliente = Cliente.objects.create(
            nombre=nombre,
            email=email,
            rut=rut,
            activo=True
        )

        # 2. Crear Tarjeta y Saldo Inicial
        saldo_inicial = Decimal(str(fake.random_int(min=10000, max=150000)))
        
        tarjeta = Tarjeta.objects.create(
            cliente=cliente,
            saldo=saldo_inicial
        )

        # Obtener la instancia de InstrumentoFinanciero vinculada
        inst_financiero = InstrumentoFinanciero.objects.filter(id=tarjeta.id).first()
        if not inst_financiero:
            inst_financiero = InstrumentoFinanciero.objects.last()

        # 3. Crear Movimientos de Prueba
        if inst_financiero:
            for _ in range(fake.random_int(min=1, max=2)):
                monto_mov = Decimal(str(fake.random_int(min=5000, max=25000)))
                Movimiento.objects.create(
                    tarjeta_uuid_origen=inst_financiero,
                    tarjeta_uuid_destino=inst_financiero,
                    monto=monto_mov,
                    estado='Completado',
                    referencia_operacion=f'REF-TEST-{fake.random_int(min=100, max=999)}'
                )

        # Mensaje de progreso cada 1000 registros
        if i % 1000 == 0:
            print(f"-> Generados {i} de {cantidad} usuarios...")

    print(f"¡Éxito! Se han generado {cantidad} clientes con sus respectivas tarjetas y movimientos.")

if __name__ == '__main__':
    poblar_base_datos(10000)