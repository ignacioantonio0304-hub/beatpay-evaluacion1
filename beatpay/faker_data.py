import os
import sys
import django

# Agregamos la carpeta raíz del proyecto (ev1) al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuramos el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicpro_project.settings')
django.setup()

from faker import Faker
from django.contrib.auth.models import User
import random
from beatpay.models import TarjetaVirtual, Transaccion

fake = Faker('es_CL') # Datos adaptados a Chile

def ejecutar_carga(cantidad=100):
    print(f"Generando {cantidad} registros de prueba para BeatPay...")
    
    for _ in range(cantidad):
        # Crear un usuario ficticio
        username = fake.user_name() + str(random.randint(1000, 9999))
        email = fake.email()
        user = User.objects.create_user(username=username, email=email, password='password123')
        
        # Crear su tarjeta virtual asociada
        num_tarjeta = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        cvv = str(random.randint(100, 999))
        saldo = round(random.uniform(5000.0, 500000.0), 2)
        
        tarjeta = TarjetaVirtual.objects.create(
            usuario=user,
            numero_tarjeta=num_tarjeta,
            saldo=saldo,
            cvv=cvv,
            fecha_expiracion="12/28",
            activa=True
        )
        
        # Crear algunas transacciones para esta tarjeta
        for _ in range(random.randint(1, 3)):
            tipo_trx = random.choice(['carga', 'pago'])
            monto_trx = round(random.uniform(1000.0, 50000.0), 2)
            comercio = "Concierto Gira 2026" if tipo_trx == 'pago' else "Carga de Fondos BeatPay"
            
            Transaccion.objects.create(
                tarjeta=tarjeta,
                tipo=tipo_trx,
                monto=monto_trx,
                comercio_destino=comercio
            )
            
    print(f"¡Carga de {cantidad} datos completada con éxito!")

if __name__ == '__main__':
    ejecutar_carga(100)