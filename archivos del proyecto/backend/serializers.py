from datetime import date

from rest_framework import serializers

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


# Serializer para el modelo Paciente
class PacienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paciente  # Modelo asociado al serializer
        fields = "__all__"  # Incluye todos los campos del modelo

    def validate_dni(self, value):
        if self.instance:
            # Validación al actualizar
            if (
                Paciente.objects.filter(dni=value)
                .exclude(id_paciente=self.instance.id_paciente)
                .exists()
            ):
                raise serializers.ValidationError(
                    "El DNI ya está registrado en otro paciente."
                )
        else:
            # Validación al crear
            if Paciente.objects.filter(dni=value).exists():
                raise serializers.ValidationError("El DNI ya está registrado.")
        return value

    def validate_email(self, value):
        if self.instance:
            # Validación al actualizar
            if (
                Paciente.objects.filter(email=value)
                .exclude(id_paciente=self.instance.id_paciente)
                .exists()
            ):
                raise serializers.ValidationError(
                    "El email ya está registrado en otro paciente."
                )
        else:
            # Validación al crear
            if Paciente.objects.filter(email=value).exists():
                raise serializers.ValidationError("El email ya está registrado.")
        return value


# Serializer para el modelo Medico
class MedicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medico  # Modelo asociado al serializer
        fields = "__all__"  # Incluye todos los campos del modelo

    def validate_ncolegiado(self, value):
        if self.instance:
            # Validación al actualizar
            if (
                Medico.objects.filter(ncolegiado=value)
                .exclude(id_medico=self.instance.id_medico)
                .exists()
            ):
                raise serializers.ValidationError(
                    "El Nº colegiado ya está registrado en otro especialista."
                )
        else:
            # Validación al crear
            if Medico.objects.filter(ncolegiado=value).exists():
                raise serializers.ValidationError("El Nº colegiado ya está registrado.")
        return value

    def validate_email(self, value):
        if self.instance:
            # Validación al actualizar
            if (
                Medico.objects.filter(email=value)
                .exclude(id_medico=self.instance.id_medico)
                .exists()
            ):
                raise serializers.ValidationError(
                    "El email ya está registrado en otro especialista."
                )
        else:
            # Validación al crear
            if Medico.objects.filter(email=value).exists():
                raise serializers.ValidationError("El email ya está registrado.")
        return value


# Serializer para el modelo Cita
class CitaSerializer(serializers.ModelSerializer):

    fecha = serializers.DateField(
        format="%Y-%m-%d", input_formats=["%Y-%m-%d", "%d-%m-%Y"]
    )

    class Meta:
        model = Cita  # Modelo asociado al serializer
        fields = "__all__"  # Incluye todos los campos del modelo
        read_only_fields = ["refcita"]  # Hace que refcita sea solo lectura

    # Representa las relaciones ForeignKey con información detallada
    id_paciente = PacienteSerializer(
        read_only=True
    )  # Serializa el objeto completo del paciente

    id_paciente_id = serializers.PrimaryKeyRelatedField(
        source="id_paciente", queryset=Paciente.objects.all(), write_only=True
    )  # Para recibir solo el ID al crear o actualizar

    id_medico = MedicoSerializer(
        read_only=True
    )  # Serializa el objeto completo del médico
    id_medico_id = serializers.PrimaryKeyRelatedField(
        source="id_medico", queryset=Medico.objects.all(), write_only=True
    )  # Para recibir solo el ID al crear o actualizar


# Serializador para Tratatmiento
class TratamientoSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True, source="id_paciente")
    medico = MedicoSerializer(read_only=True, source="id_medico")

    class Meta:
        model = Tratamiento
        fields = "__all__"


# Serializador para Historia Clinica
class HistoriaClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriaClinica
        fields = "__all__"


# Serializador para Derivaciones
class DerivacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Derivaciones
        fields = "__all__"


# Serializador para Facturas
class FacturasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facturas
        fields = "__all__"


# Serializador para Usuarios/Roles
class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = "__all__"

    """

    class FacturasSerializer(serializers.ModelSerializer):
    # Incluyendo campos relacionados (opcional)
    ref_cita = serializers.CharField(source='id_cita.refcita', read_only=True)  # Campo derivado de la cita
    nombre_paciente = serializers.CharField(
        source='id_cita.id_paciente.nombre', read_only=True
    )  # Nombre del paciente relacionado con la cita
    apellido_paciente = serializers.CharField(
        source='id_cita.id_paciente.apellido', read_only=True
    )  # Apellido del paciente relacionado con la cita
    costo_tratamiento = serializers.DecimalField(
        source='id_tratamiento.costo', max_digits=10, decimal_places=2, read_only=True
    )  # Costo derivado del tratamiento

    class Meta:
        model = Facturas
        fields = [
            'id',
            'ref_factura',
            'id_cita',
            'id_tratamiento',
            'concepto',
            'fecha_emision',
            'fecha_cobro',
            'estado',
            'ref_cita',          # Campo derivado de id_cita
            'nombre_paciente',   # Campo derivado del paciente
            'apellido_paciente', # Campo derivado del paciente
            'costo_tratamiento', # Campo derivado del tratamiento
        ]
        read_only_fields = ['ref_cita', 'nombre_paciente', 'apellido_paciente', 'costo_tratamiento']

    def validate(self, data):
        
        Validación personalizada para asegurar consistencia de datos.
        
        if data.get('fecha_cobro') and data.get('fecha_cobro') < data.get('fecha_emision'):
            raise serializers.ValidationError("La fecha de cobro no puede ser anterior a la fecha de emisión.")
        return data


    """

    """
        # Validar que la referencia de cita sea única
        if Cita.objects.filter(refcita=refcita).exists():
            raise serializers.ValidationError({
                "duplicado_refcita": "La referencia de cita ya está registrada."
            })

        return data
        """

    """
        def validate_fecha(self, value):
        """

    """
        Validación personalizada para el campo `fecha`.
        Se asegura de que la fecha no sea anterior a la fecha actual.
        """

    """
        if value < date.today():  # Verifica si la fecha es pasada
            raise serializers.ValidationError("La fecha no puede ser en el pasado.")
        return value  # Retorna la fecha si es válida
        """


def validate_hora(self, value):
    """
    Validación personalizada para el campo `hora`.
    Se asegura de que la hora esté dentro del horario laboral (9:00 a 17:00).
    """
    import datetime

    # Verifica si la hora está fuera del rango permitido
    if value < datetime.time(9, 0) or value > datetime.time(17, 0):
        raise serializers.ValidationError(
            "La hora debe estar entre las 09:00 y las 17:00."
        )
    return value  # Retorna la hora si es válida


"""
# Serializer para el modelo Cita
class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita  # Modelo asociado al serializer
        fields = '__all__'  # Incluye todos los campos del modelo
"""
"""
    def validate_(self, value):
        if self.instance:
            # Validación al actualizar
            if Medico.objects.filter(ncolegiado=value).exclude(id_medico=self.instance.id_medico).exists():
                raise serializers.ValidationError("El Nº colegiado ya está registrado en otro especialista.")
        else:
            # Validación al crear
            if Medico.objects.filter(ncolegiado=value).exists():
                raise serializers.ValidationError("El Nº colegiado ya está registrado.")
        return value

    def validate_email(self, value):
        if self.instance:
            # Validación al actualizar
            if Medico.objects.filter(email=value).exclude(id_medico=self.instance.id_medico).exists():
                raise serializers.ValidationError("El email ya está registrado en otro especialista.")
        else:
            # Validación al crear
            if Medico.objects.filter(email=value).exists():
                raise serializers.ValidationError("El email ya está registrado.")
        return value
"""


def validate(self, data):
    paciente = data.get("id_paciente")
    medico = data.get("id_medico")
    fecha = data.get("fecha")
    hora = data.get("hora")

    # Validar que todos los campos necesarios estén presentes
    missing_fields = []
    if not paciente:
        missing_fields.append("id_paciente")
    if not medico:
        missing_fields.append("id_medico")
    if not fecha:
        missing_fields.append("fecha")
    if not hora:
        missing_fields.append("hora")

    if missing_fields:
        raise serializers.ValidationError(
            {
                "campos_faltantes": f"Los siguientes campos son obligatorios: {', '.join(missing_fields)}"
            }
        )

    # Validar que el médico no tenga otra cita en la misma fecha y hora
    if Cita.objects.filter(fecha=fecha, hora=hora, id_medico=medico).exists():
        raise serializers.ValidationError(
            {
                "conflicto_horario": "El médico ya tiene una cita programada en este horario."
            }
        )

    return data  # ✅ IMPORTANTE: Retornar los datos validados
