from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CitaViewSet,
    DerivacionesViewSet,
    FacturasViewSet,
    HistoriaClinicaViewSet,
    MedicoViewSet,
    PacienteViewSet,
    TratamientoViewSet,
    UsuariosViewSet,
    index_view,
)

router = DefaultRouter()
router.register(r"paciente", PacienteViewSet, basename="paciente")
router.register(r"medico", MedicoViewSet, basename="medico")
router.register(r"cita", CitaViewSet, basename="cita")
router.register(r"tratamiento", TratamientoViewSet, basename="tratamiento")
router.register(
    r"historia_clinica", HistoriaClinicaViewSet, basename="historia_clinica"
)
router.register(r"derivaciones", DerivacionesViewSet, basename="derivaciones")
router.register(r"facturas", FacturasViewSet, basename="facturas")
router.register(r"usuarios", UsuariosViewSet, basename="usuarios")

# Aquí cargamos las URLs que vayamos a usar para las pruebas.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path(
        "", index_view, name="opciones"
    ),  # Página principal con las opciones a elegir.
]
