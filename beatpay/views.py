from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Count, Avg
from .models import Cliente, Tarjeta, Movimiento, InstrumentoFinanciero, Banco

# ==========================================
# Datos simulados (Mock Data) para la app
# ==========================================
usuario_actual = {
    "nombre": "Ignacio Hidalgo",
    "email": "ignacio.hidalgo@musicpro.cl",
}

tarjeta_virtual = {
    "numero": "**** **** **** 1726",
    "tipo": "Visa Digital - BeatPay",
    "estado": "Activa",
    "saldo": 45500,
}

cartelera_eventos = [
    {"id": 1, "nombre": "Gira Music Pro Tour 2026 - Concierto Santiago", "precio": 15000, "fecha": "15-09-2026"},
    {"id": 2, "nombre": "Music Pro Festival - Edición Providencia", "precio": 22000, "fecha": "28-09-2026"},
    {"id": 3, "nombre": "Show Acústico Íntimo Sello ALR", "precio": 10000, "fecha": "10-10-2026"},
]

historial_transacciones = [
    {"tipo": "Recarga de Fondos", "detalle": "Abono inicial en moneda local", "monto": 30000, "fecha": "05/09/2026", "estado": "Acreditado"},
    {"tipo": "Pago de Entrada", "detalle": "Entrada Gira Music Pro Tour", "monto": -15000, "fecha": "06/09/2026", "estado": "Exitoso"},
]

# ==========================================
# Autenticación y Seguridad
# ==========================================
def login_view(request):
    error = None
    if request.method == "POST":
        email_ingresado = request.POST.get("email")
        password_ingresada = request.POST.get("password")
        
        user = authenticate(request, username=email_ingresado, password=password_ingresada)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            if email_ingresado == "ignacio.hidalgo@musicpro.cl" and password_ingresada == "123456":
                return redirect('dashboard')
            error = "Correo o contraseña incorrectos."
            
    return render(request, 'beatpay/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


# ==========================================
# Vistas del Sistema (Protegidas)
# ==========================================
@login_required(login_url='login')
def dashboard_view(request):
    context = {
        "usuario": usuario_actual,
        "tarjeta": tarjeta_virtual,
    }
    return render(request, 'beatpay/dashboard.html', context)


@login_required(login_url='login')
def detalle_tarjeta_view(request):
    context = {"tarjeta": tarjeta_virtual}
    return render(request, 'beatpay/detalle_tarjeta.html', context)


@login_required(login_url='login')
def cargar_fondos_view(request):
    global tarjeta_virtual
    mensaje = None
    if request.method == "POST":
        monto = int(request.POST.get("monto", 0))
        if monto > 0:
            tarjeta_virtual["saldo"] += monto
            historial_transacciones.insert(0, {
                "tipo": "Recarga de Fondos",
                "detalle": "Recarga mediante pasarela local",
                "monto": monto,
                "fecha": "06/09/2026",
                "estado": "Acreditado"
            })
            mensaje = f"¡Recarga exitosa de ${monto} CLP!"
            
    context = {"tarjeta": tarjeta_virtual, "mensaje": mensaje}
    return render(request, 'beatpay/cargar_fondos.html', context)


@login_required(login_url='login')
def cartelera_view(request):
    context = {"eventos": cartelera_eventos}
    return render(request, 'beatpay/cartelera.html', context)


@login_required(login_url='login')
def simular_pago_view(request, evento_id):
    global tarjeta_virtual
    evento = next((e for e in cartelera_eventos if e["id"] == evento_id), None)
    error = None
    exito = None

    if evento:
        if tarjeta_virtual["saldo"] >= evento["precio"]:
            tarjeta_virtual["saldo"] -= evento["precio"]
            historial_transacciones.insert(0, {
                "tipo": "Compra Entradas",
                "detalle": evento["nombre"],
                "monto": -evento["precio"],
                "fecha": "06/09/2026",
                "estado": "Exitoso"
            })
            exito = f"¡Pago exitoso para {evento['nombre']}!"
        else:
            error = "Fondos insuficientes en la tarjeta virtual. Por favor, cargue fondos."
            
    context = {"evento": evento, "tarjeta": tarjeta_virtual, "error": error, "exito": exito}
    return render(request, 'beatpay/resultado_pago.html', context)


@login_required(login_url='login')
def historial_view(request):
    context = {"transacciones": historial_transacciones}
    return render(request, 'beatpay/historial.html', context)


# ==========================================
# PARTE 2: Consultas Django ORM y Reportes
# ==========================================
@login_required(login_url='login')
def reportes_view(request):
    # 1. Básico: Todos los clientes registrados
    q1_clientes = Cliente.objects.all()

    # 2. Básico: Tarjetas activas vs inactivas/bloqueadas
    q2_tarjetas_activas = Tarjeta.objects.filter(estado='Activa').count()

    # 3. Básico: Últimos 10 movimientos registrados
    q3_ultimos_movimientos = Movimiento.objects.select_related(
        'tarjeta_uuid_origen', 'tarjeta_uuid_destino'
    ).order_by('-fecha')[:10]

    # 4. Intermedio: Transferencias enviadas hacia instrumentos de Tenpo
    q4_movimientos_tenpo = Movimiento.objects.filter(
        tarjeta_uuid_destino__banco__nombre__icontains='Tenpo'
    )

    # 5. Intermedio: Transferencias recibidas desde MACH
    q5_movimientos_mach = Movimiento.objects.filter(
        tarjeta_uuid_origen__banco__nombre__icontains='MACH'
    )

    # 6. Intermedio: Conteo de movimientos según su estado
    q6_estado_movimientos = Movimiento.objects.values('estado').annotate(total=Count('id'))

    # 7. Intermedio: Los 10 movimientos con mayor monto
    q7_top_movimientos = Movimiento.objects.order_by('-monto')[:10]

    # 8. Avanzado: Monto total transferido agrupado por tarjeta origen
    q8_totales_enviados = Movimiento.objects.filter(
        tarjeta_uuid_origen__es_interno=True
    ).values('tarjeta_uuid_origen__tarjeta__numero_enmascarado').annotate(monto_total=Sum('monto'))

    # 9. Análisis: Monto promedio de transferencias completadas
    q9_promedio_completadas = Movimiento.objects.filter(
        estado='Completado'
    ).aggregate(promedio=Avg('monto'))['promedio'] or 0

    # 10. Análisis: Porcentaje de operaciones internas vs externas
    total_mov = Movimiento.objects.count()
    internas = Movimiento.objects.filter(
        tarjeta_uuid_origen__es_interno=True, 
        tarjeta_uuid_destino__es_interno=True
    ).count()
    porcentaje_internas = (internas / total_mov * 100) if total_mov > 0 else 0

    context = {
        'clientes': q1_clientes,
        'tarjetas_activas_count': q2_tarjetas_activas,
        'ultimos_movimientos': q3_ultimos_movimientos,
        'movimientos_tenpo': q4_movimientos_tenpo,
        'movimientos_mach': q5_movimientos_mach,
        'estado_movimientos': q6_estado_movimientos,
        'top_movimientos': q7_top_movimientos,
        'totales_enviados': q8_totales_enviados,
        'promedio_completadas': q9_promedio_completadas,
        'porcentaje_internas': round(porcentaje_internas, 1),
    }
    return render(request, 'beatpay/reportes.html', context)