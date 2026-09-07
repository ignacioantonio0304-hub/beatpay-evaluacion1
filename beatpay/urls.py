from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('tarjeta/', views.detalle_tarjeta_view, name='detalle_tarjeta'),
    path('recargar/', views.cargar_fondos_view, name='cargar_fondos'),
    path('cartelera/', views.cartelera_view, name='cartelera'),
    path('pagar/<int:evento_id>/', views.simular_pago_view, name='simular_pago'),
    path('historial/', views.historial_view, name='historial'),
]