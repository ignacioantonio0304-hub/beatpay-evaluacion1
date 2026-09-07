from django.shortcuts import render, redirect

# Datos simulados (Mock Data) para la Evaluación 1
usuario_actual = {
    "nombre": "Ignacio Hidalgo",
    "email": "ignacio.hidalgo@musicpro.cl",
}

tarjeta_virtual = {
    "numero": "**** **** **** 1726",
    "tipo": "Visa Digital - BeatPay",
    "estado": "Activa",
    "saldo": 45500, # en CLP
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

def login_view(request):
    return render(request, 'beatpay/login.html')

def dashboard_view(request):
    context = {
        "usuario": usuario_actual,
        "tarjeta": tarjeta_virtual,
    }
    return render(request, 'beatpay/dashboard.html', context)

def detalle_tarjeta_view(request):
    context = {"tarjeta": tarjeta_virtual}
    return render(request, 'beatpay/detalle_tarjeta.html', context)

def cargar_fondos_view(request):
    global tarjeta_virtual
    mensaje = None
    if request.method == "POST":
        monto = int(request.POST.get("monto", 0))
        if monto > 0:
            tarjeta_virtual["saldo"] += monto
            # Registrar en historial
            historial_transacciones.insert(0, {
                "tipo": "Recarga de Fondos",
                "detalle": f"Recarga mediante pasarela local",
                "monto": monto,
                "fecha": "06/09/2026",
                "estado": "Acreditado"
            })
            mensaje = f"¡Recarga exitosa de ${monto} CLP!"
    
    context = {"tarjeta": tarjeta_virtual, "mensaje": mensaje}
    return render(request, 'beatpay/cargar_fondos.html', context)

def cartelera_view(request):
    context = {"eventos": cartelera_eventos}
    return render(request, 'beatpay/cartelera.html', context)

def simular_pago_view(request, evento_id):
    global tarjeta_virtual
    # Buscar el evento seleccionado
    evento = next((e for e in cartelera_eventos if e["id"] == evento_id), None)
    error = None
    exito = None

    if evento:
        if tarjeta_virtual["saldo"] >= evento["precio"]:
            # Descontar saldo
            tarjeta_virtual["saldo"] -= evento["precio"]
            # Agregar al historial
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

def historial_view(request):
    context = {"transacciones": historial_transacciones}
    return render(request, 'beatpay/historial.html', context)