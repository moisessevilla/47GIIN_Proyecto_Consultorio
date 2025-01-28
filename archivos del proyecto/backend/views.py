from django.db import transaction
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .models import (
    Cita,
    Derivaciones,
    Facturas,
    HistoriaClinica,
    Medico,
    Paciente,
    Tratamiento,
    Usuarios,
)
from .serializers import (
    CitaSerializer,
    DerivacionesSerializer,
    FacturasSerializer,
    HistoriaClinicaSerializer,
    MedicoSerializer,
    PacienteSerializer,
    TratamientoSerializer,
    UsuariosSerializer,
)


# Vista principal
def index_view(request):

    # Renderiza la página principal con las opciones a elegir.
    try:
        return render(request, "opciones.html")
    except Exception as e:
        return Response(
            {"error": f"Error al cargar la página: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Habilitar Logs en el Backend
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Si ya existe una respuesta, se devuelve en JSON
        response.data["status_code"] = response.status_code
    else:
        # Si es un error no controlado, se devuelve este mensaje
        return Response(
            {"error": "Se ha producido un error inesperado.", "detalle": str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return response


# CRUD Paciente
class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all().order_by("id_paciente")
    serializer_class = PacienteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"Mensaje": "Paciente eliminado exitosamente."}, status=status.HTTP_200_OK
        )


# CRUD Medico
class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all().order_by("id_medico")
    serializer_class = MedicoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"Mensaje": "Medico eliminado exitosamente."}, status=status.HTTP_200_OK
        )


# CRUD Cita
class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all().order_by("id_cita")
    serializer_class = CitaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"Mensaje": "Cita eliminada exitosamente."}, status=status.HTTP_200_OK
        )


@api_view(["GET"])
def obtener_cita(request):
    id_cita = request.query_params.get("id_cita", None)
    if id_cita:
        try:
            cita = Cita.objects.get(id_cita=id_cita)
            serializer = CitaSerializer(cita)
            return Response(serializer.data)
        except Cita.DoesNotExist:
            return Response({"error": "Cita no encontrada."}, status=404)
    return Response({"error": "ID de cita no proporcionado."}, status=400)


# CRUD Tratamiento
class TratamientoViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all().order_by("id_tratamiento")
    queryset = Tratamiento.objects.select_related("id_paciente", "id_medico")
    serializer_class = TratamientoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"Mensaje": "Tratamiento eliminado exitosamente."},
            status=status.HTTP_200_OK,
        )

    def get_queryset(self):
        # Filtrar por id_tratamiento si se pasa como parámetro
        id_tratamiento = self.request.query_params.get("id_tratamiento", None)
        if id_tratamiento is not None:
            return self.queryset.filter(id_tratamiento=id_tratamiento)
        return self.queryset

    @action(detail=False, methods=["get"])
    def by_id(self, request):
        id_tratamiento = request.query_params.get("id_tratamiento", None)
        if id_tratamiento:
            tratamiento = self.queryset.filter(id_tratamiento=id_tratamiento).first()
            if tratamiento:
                serializer = self.get_serializer(tratamiento)
                return Response(serializer.data)
            return Response({"error": "Tratamiento no encontrado"}, status=404)
        return Response({"error": "ID de tratamiento no proporcionado"}, status=400)


# CRUD História Clínica
class HistoriaClinicaViewSet(viewsets.ModelViewSet):
    queryset = HistoriaClinica.objects.all().order_by("id_historia")
    serializer_class = HistoriaClinicaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"Mensaje": "Tratamiento eliminado exitosamente."},
            status=status.HTTP_200_OK,
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        id_historia = self.request.query_params.get("id_historia", None)
        if id_historia:  # Corrección del filtro
            queryset = queryset.filter(id_historia=id_historia)
        return queryset


# CRUD Derivaciones
class DerivacionesViewSet(viewsets.ModelViewSet):
    queryset = Derivaciones.objects.all().order_by("id_derivacion")
    serializer_class = DerivacionesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"Mensaje": "Tratamiento eliminado exitosamente."},
            status=status.HTTP_200_OK,
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        id_derivacion = self.request.query_params.get("id_derivacion", None)
        if id_derivacion:  # Corrección del filtro
            queryset = queryset.filter(id_derivacion=id_derivacion)
        return queryset


# CRUD Facturas
class FacturasViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para el modelo Facturas.
    """

    queryset = Facturas.objects.all().order_by(
        "id_factura"
    )  # Consulta inicial para todas las facturas
    serializer_class = FacturasSerializer  # Serializador asociado

    def get_queryset(self):
        """
        Personaliza el conjunto de consultas para permitir el filtro por `id_factura`.
        """
        queryset = super().get_queryset()
        id_factura = self.request.query_params.get("id_factura", None)

        if id_factura:
            queryset = queryset.filter(
                id_factura=id_factura
            )  # Cambia `id` por `id_factura`
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Listar todas las facturas con soporte para filtros.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Soporte para filtros opcionales (por ejemplo, estado o fecha_emision)
        estado = request.query_params.get("estado", None)
        if estado:
            queryset = queryset.filter(estado=estado)

        fecha_emision = request.query_params.get("fecha_emision", None)
        if fecha_emision:
            queryset = queryset.filter(fecha_emision=fecha_emision)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Crear una nueva factura.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Obtener los detalles de una factura específica.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Actualizar completamente una factura.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Eliminar una factura.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# CRUD Usuarios
class UsuariosViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para el modelo Usuarios.
    """

    queryset = Usuarios.objects.all().order_by("id_usuario")  # Consulta inicial
    serializer_class = UsuariosSerializer

    def list(self, request, *args, **kwargs):
        """
        Listar todos los usuarios con soporte para filtros.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Filtrar por rol si se pasa como parámetro
        rol = request.query_params.get("rol", None)
        if rol:
            queryset = queryset.filter(rol=rol)

        # Filtrar por estado activo
        activo = request.query_params.get("activo", None)
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() in ["true", "1"])

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Crear un nuevo usuario.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Obtener los detalles de un usuario específico.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Actualizar completamente un usuario.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Eliminar un usuario.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"Mensaje": "Usuario eliminado exitosamente."},
            status=status.HTTP_204_NO_CONTENT,
        )
