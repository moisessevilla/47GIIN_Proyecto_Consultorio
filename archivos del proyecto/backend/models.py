import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


# Modelo para los pacientes
class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)  # Identificador único del paciente
    dni = models.CharField(unique=True, max_length=9)  # DNI del paciente
    nombre = models.CharField(max_length=100)  # Nombre del paciente
    apellido = models.CharField(max_length=100)  # Apellido del paciente
    email = models.CharField(unique=True, max_length=100)  # Correo único del paciente
    telefono = models.CharField(
        max_length=15, blank=True, null=True
    )  # Teléfono del paciente (opcional)
    contrasena = models.CharField(max_length=100)  # Contraseña del paciente

    class Meta:
        managed = False
        db_table = "paciente"


# Modelo para los médicos
class Medico(models.Model):
    id_medico = models.AutoField(primary_key=True)  # Identificador único del médico
    ncolegiado = models.CharField(
        unique=True, max_length=8
    )  # Número de colegiado del médico
    nombre = models.CharField(max_length=100)  # Nombre del médico
    especialidad = models.CharField(max_length=100)  # Especialidad del médico
    email = models.CharField(unique=True, max_length=100)  # Correo único del médico

    class Meta:
        managed = False
        db_table = "medico"


# Modelo para las citas
class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)  # Identificador único para cada cita
    id_paciente = models.ForeignKey(
        "Paciente", models.DO_NOTHING, db_column="id_paciente"
    )  # Relación con un paciente
    id_medico = models.ForeignKey(
        "Medico", models.DO_NOTHING, db_column="id_medico"
    )  # Relación con un médico
    fecha = models.DateField()  # Fecha de la cita
    hora = models.TimeField()  # Hora de la cita
    especialidad = models.CharField(max_length=100, null=True)  # Especialidad asociada
    estado = models.CharField(max_length=20, default="confirmada")
    refcita = models.CharField(max_length=12, unique=True, editable=False)

    def save(self, *args, **kwargs):
        # Generar refcita si no existe
        if not self.refcita:
            self.refcita = str(uuid.uuid4())[:12].replace("-", "").upper()
        super(Cita, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = "cita"


# Modelo para tratamiento
class Tratamiento(models.Model):
    id_tratamiento = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(
        "Paciente",
        on_delete=models.CASCADE,
        db_column="id_paciente",  # Asegúrate de especificar el nombre de la columna exacto
    )
    id_medico = models.ForeignKey(
        "Medico",
        on_delete=models.CASCADE,
        db_column="id_medico",  # Asegúrate de especificar el nombre de la columna exacto
    )
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        managed = False
        db_table = "tratamiento"  # Nombre de la tabla en la base de datos


# Modelo para Historia Clínica
class HistoriaClinica(models.Model):
    id_historia = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(
        "Paciente",
        on_delete=models.CASCADE,
        db_column="id_paciente",  # Asegúrate de que coincida con la columna en la BD
    )
    descripcion = models.TextField()
    observaciones = models.TextField(null=True, blank=True)
    fecha_apertura = models.DateField()

    class Meta:
        managed = False
        db_table = "historia_clinica"  # Nombre de la tabla en la base de datos


# Modelo para las Derivaciones
class Derivaciones(models.Model):
    id_derivacion = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(
        "Paciente", on_delete=models.CASCADE, db_column="id_paciente"
    )
    id_medico_remitente = models.ForeignKey(
        "Medico",
        on_delete=models.CASCADE,
        related_name="medico_remitente",
        db_column="id_medico_remitente",
    )
    id_medico_destino = models.ForeignKey(
        "Medico",
        on_delete=models.CASCADE,
        related_name="medico_destino",
        db_column="id_medico_destino",
    )
    motivo = models.TextField()
    fecha_derivacion = models.DateField()

    class Meta:
        managed = False
        db_table = "derivaciones"  # Nombre de la tabla en la base de datos


# Modelo paras las Facturas
class Facturas(models.Model):
    id_factura = models.AutoField(
        primary_key=True, db_column="id_factura"
    )  # Declarar explícitamente la clave primaria
    ref_factura = models.CharField(
        max_length=12,
        unique=True,
        verbose_name=_("Referencia de la factura"),
        help_text=_("Código único de referencia para la factura (máx. 12 caracteres)"),
    )
    id_cita = models.ForeignKey(
        "Cita",  # Nombre del modelo relacionado
        on_delete=models.CASCADE,
        verbose_name=_("Cita"),
        db_column="id_cita",
        help_text=_("ID de la cita asociada"),
    )
    id_tratamiento = models.ForeignKey(
        "Tratamiento",  # Nombre del modelo relacionado
        on_delete=models.CASCADE,
        verbose_name=_("Tratamiento"),
        db_column="id_tratamiento",
        help_text=_("ID del tratamiento asociado"),
    )
    concepto = models.TextField(
        verbose_name=_("Concepto"),
        help_text=_("Descripción del concepto de la factura"),
    )
    fecha_emision = models.DateField(
        verbose_name=_("Fecha de emisión"),
        help_text=_("Fecha en la que se emitió la factura"),
    )
    fecha_cobro = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Fecha de cobro"),
        help_text=_("Fecha en la que se cobró la factura (opcional)"),
    )
    estado = models.CharField(
        max_length=20,
        choices=[
            ("Pendiente", _("Pendiente")),
            ("Pagada", _("Pagada")),
            ("Cancelada", _("Cancelada")),
        ],
        default="Pendiente",
        verbose_name=_("Estado"),
        help_text=_("Estado actual de la factura"),
    )

    class Meta:
        verbose_name = _("Factura")
        verbose_name_plural = _("Facturas")
        ordering = ["-fecha_emision"]
        managed = False
        db_table = "facturas"

    def __str__(self):
        return f"Factura {self.ref_factura} - {self.get_estado_display()}"


# Modelo para usuarios y roles
class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)  # Clave primaria
    nombre = models.CharField(max_length=100)  # Nombre del usuario
    email = models.EmailField(unique=True, max_length=150)  # Correo electrónico único
    contrasena = models.CharField(max_length=255)  # Contraseña cifrada
    fecha_creacion = models.DateField(auto_now_add=True)  # Fecha de creación
    fecha_actualizacion = models.DateField(
        auto_now=True
    )  # Fecha de última actualización
    activo = models.BooleanField(default=True)  # Indica si el usuario está activo
    rol = models.CharField(max_length=100)  # Rol del usuario
    permisos = models.CharField(max_length=100)  # Permisos asociados al usuario

    class Meta:
        managed = False  # Indica que Django no gestionará la tabla
        db_table = "usuarios"  # Nombre de la tabla en la base de datos

    def __str__(self):
        return f"{self.nombre} ({self.rol})"


"""
class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)  # Identificador único para cada cita
    id_paciente = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='id_paciente')  # Relación con un paciente
    id_medico = models.ForeignKey('Medico', models.DO_NOTHING, db_column='id_medico')  # Relación con un médico
    fecha = models.DateField()  # Fecha de la cita
    hora = models.TimeField()  # Hora de la cita
    especialidad = models.CharField(max_length=100, null=True)  # Especialidad asociada
    estado = models.CharField(max_length=20, default='confirmada')
    refcita = models.CharField(max_length=12)

    def save(self, *args, **kwargs):
        if not self.refcita:
            # Generar un código único para refcita
            self.refcita = str(uuid.uuid4()).split('-')[0].upper()
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'cita'
"""


# Modelo para los administradores del sistema
class Administrador(models.Model):
    id_admin = models.AutoField(
        primary_key=True
    )  # Identificador único para cada administrador
    nombre = models.CharField(max_length=100)  # Nombre del administrador
    correo = models.CharField(
        unique=True, max_length=100
    )  # Correo único del administrador

    class Meta:
        managed = False  # Indica que Django no gestionará esta tabla
        db_table = "administrador"  # Nombre de la tabla en la base de datos


# Grupo de permisos (por defecto en Django)
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)  # Nombre único del grupo

    class Meta:
        managed = False
        db_table = "auth_group"


# Relación entre grupos y permisos
class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)  # Relación con un grupo
    permission = models.ForeignKey(
        "AuthPermission", models.DO_NOTHING
    )  # Relación con un permiso

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)  # Clave única compuesta


# Modelo de permisos (por defecto en Django)
class AuthPermission(models.Model):
    name = models.CharField(max_length=255)  # Nombre del permiso
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)  # Código único para el permiso

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)  # Clave única compuesta


# Usuarios del sistema (por defecto en Django)
class AuthUser(models.Model):
    password = models.CharField(max_length=128)  # Contraseña cifrada
    last_login = models.DateTimeField(blank=True, null=True)  # Último inicio de sesión
    is_superuser = models.BooleanField()  # Indica si es un superusuario
    username = models.CharField(unique=True, max_length=150)  # Nombre de usuario único
    first_name = models.CharField(max_length=150)  # Nombre
    last_name = models.CharField(max_length=150)  # Apellido
    email = models.CharField(max_length=254)  # Correo electrónico
    is_staff = models.BooleanField()  # Indica si es parte del personal
    is_active = models.BooleanField()  # Indica si está activo
    date_joined = models.DateTimeField()  # Fecha de creación del usuario

    class Meta:
        managed = False
        db_table = "auth_user"


# Relación entre usuarios y grupos
class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)  # Relación con un usuario
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)  # Relación con un grupo

    class Meta:
        managed = False
        db_table = "auth_user_groups"
        unique_together = (("user", "group"),)  # Clave única compuesta


# Relación entre usuarios y permisos
class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)  # Relación con un usuario
    permission = models.ForeignKey(
        AuthPermission, models.DO_NOTHING
    )  # Relación con un permiso

    class Meta:
        managed = False
        db_table = "auth_user_user_permissions"
        unique_together = (("user", "permission"),)  # Clave única compuesta


# Modelo para registrar acciones administrativas
class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()  # Hora de la acción
    object_id = models.TextField(
        blank=True, null=True
    )  # Identificador del objeto afectado
    object_repr = models.CharField(max_length=200)  # Representación del objeto
    action_flag = models.SmallIntegerField()  # Tipo de acción
    change_message = models.TextField()  # Descripción de los cambios
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey(
        AuthUser, models.DO_NOTHING
    )  # Usuario que realizó la acción

    class Meta:
        managed = False
        db_table = "django_admin_log"


# Modelo para los tipos de contenido en Django
class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)  # Nombre de la aplicación
    model = models.CharField(max_length=100)  # Nombre del modelo

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)  # Clave única compuesta


# Migraciones de Django
class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)  # Nombre de la aplicación
    name = models.CharField(max_length=255)  # Nombre de la migración
    applied = models.DateTimeField()  # Fecha de aplicación

    class Meta:
        managed = False
        db_table = "django_migrations"


# Sesiones de usuarios en Django
class DjangoSession(models.Model):
    session_key = models.CharField(
        primary_key=True, max_length=40
    )  # Clave única para la sesión
    session_data = models.TextField()  # Datos de la sesión
    expire_date = models.DateTimeField()  # Fecha de expiración

    class Meta:
        managed = False
        db_table = "django_session"


# Modelo para el historial médico de pacientes
class Historialmedico(models.Model):
    id_historial_medico = models.AutoField(
        primary_key=True
    )  # Identificador único del historial
    id_paciente = models.ForeignKey(
        "Paciente", models.DO_NOTHING, db_column="id_paciente"
    )  # Relación con un paciente
    notas = models.TextField(blank=True, null=True)  # Notas del historial (opcional)
    ultima_actualizacion = models.DateTimeField(
        blank=True, null=True
    )  # Última actualización del historial

    class Meta:
        managed = False
        db_table = "historialmedico"


# Modelo para las notificaciones
class Notificaciones(models.Model):
    id_notificacion = models.AutoField(
        primary_key=True
    )  # Identificador único de la notificación
    id_cita = models.ForeignKey(
        Cita, models.DO_NOTHING, db_column="id_cita"
    )  # Relación con una cita
    tipo = models.CharField(
        max_length=50
    )  # Tipo de notificación (ejemplo: recordatorio)
    mensaje = models.TextField()  # Mensaje de la notificación
    fecha_envio = models.DateTimeField(
        blank=True, null=True
    )  # Fecha de envío (opcional)

    class Meta:
        managed = False
        db_table = "notificaciones"


# Modelo para los roles en el sistema
class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)  # Identificador único del rol
    nombre_rol = models.CharField(max_length=50)  # Nombre del rol

    class Meta:
        managed = False
        db_table = "roles"


# Relación entre usuarios y roles
class Usuariorol(models.Model):
    id_usuario = models.OneToOneField(
        Administrador, models.DO_NOTHING, db_column="id_usuario", primary_key=True
    )  # Relación con un administrador
    id_rol = models.ForeignKey(
        Roles, models.DO_NOTHING, db_column="id_rol"
    )  # Relación con un rol

    class Meta:
        managed = False
        db_table = "usuariorol"
        unique_together = (("id_usuario", "id_rol"),)  # Clave única compuesta
