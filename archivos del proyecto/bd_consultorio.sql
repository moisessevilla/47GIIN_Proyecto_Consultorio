-- Crear la base de datos para PostgreSQL
CREATE DATABASE IF NOT EXISTS consultorio;

-- Crear la tabla Paciente
CREATE TABLE Paciente (
    id_paciente SERIAL PRIMARY KEY,
    dni VARCHAR(9) UNIQUE,              -- Campo DNI
    nombre VARCHAR(100) NOT NULL,       -- Nombre (máx. 9 carácteres)
    apellido VARCHAR(100) NOT NULL,     -- Apellido
    email VARCHAR(100) UNIQUE NOT NULL, -- Email único
    telefono VARCHAR(9),                -- Teléfono (máx. 9 carácteres)
    contrasena VARCHAR(100) NOT NULL    -- Contraseña
);

-- Crear la tabla Médico
CREATE TABLE Medico (
    id_medico SERIAL PRIMARY KEY,           -- Identificador único
    ncolegiado VARCHAR(8) UNIQUE NOT NULL,  -- Número de colegiado (máx. 8 carácteres)
    nombre VARCHAR(100) NOT NULL,           -- Nombre completo
    especialidad VARCHAR(50) NOT NULL,      -- Especialidad médica
    email VARCHAR(100) UNIQUE NOT NULL      -- Email único
);

-- Crear la tabla Cita
CREATE TABLE Cita (
    id_cita SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'confirmada',
    refcita VARCHAR(12) UNIQUE NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES Medico(id_medico) ON DELETE CASCADE
);

-- Crear la tabla de Tratamientos
CREATE TABLE tratamiento (
    id_tratamiento SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    costo NUMERIC (10, 2),
    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES medico(id_medico) ON DELETE CASCADE
);

-- Crear la tabla de Historia Clínica
CREATE TABLE historia_clinica (
    id_historia SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL,
    descripcion TEXT NOT NULL,
    observaciones TEXT, 
    fecha_apertura DATE NOT NULL, 
    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente) ON DELETE CASCADE
);

-- Crear la tabla de Derivaciones a Especialistas
CREATE TABLE derivaciones (
    id_derivacion SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico_remitente INT NOT NULL,
    id_medico_destino INT NOT NULL,
    motivo TEXT NOT NULL,
    fecha_derivacion DATE NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    FOREIGN KEY (id_medico_remitente) REFERENCES medico(id_medico) ON DELETE CASCADE,
    FOREIGN KEY (id_medico_destino) REFERENCES medico(id_medico) ON DELETE CASCADE
);

-- Crear la tabla de Facturas
CREATE TABLE facturas (
    id_factura SERIAL PRIMARY KEY,
    ref_factura VARCHAR(12) UNIQUE NOT NULL, -- Se genera en backend automáticamente
    id_cita INT NOT NULL, -- A partir de id_cita mostrar en VUE refcita de la tabla Cita, el nombre y apellido del paciente de la tabla Paciente
    id_tratamiento INT NOT NULL, -- Mostrar el costo de la tabla de tratamiento
    concepto TEXT NOT NULL,
    fecha_emision DATE NOT NULL,
    fecha_cobro DATE,
    estado VARCHAR(20) DEFAULT 'Pendiente',
    FOREIGN KEY (id_cita) REFERENCES cita(id_cita) ON DELETE CASCADE,
    FOREIGN KEY (id_tratamiento) REFERENCES tratamiento(id_tratamiento) ON DELETE CASCADE
);


-- Crear la tabla de Usuarios
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL, -- Contraseña encriptada
    fecha_creacion DATE,
    fecha_actualizacion DATE,
    activo BOOLEAN DEFAULT TRUE, -- Indica si el usuario está activo
    rol VARCHAR(100) NOT NULL,
    permisos VARCHAR(100) NOT NULL,
);






--********* Se han aplicado de aquí hacía arriba **********

--**** Temporal, de aquí hacía abajo no se han usado ******







-- Tabla de Usuarios
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL, -- Contraseña encriptada
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE -- Indica si el usuario está activo
);

-- Tabla de Roles
CREATE TABLE roles (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE, -- Ejemplo: Admin, Médico, Recepcionista
    descripcion TEXT
);

-- Tabla de Permisos
CREATE TABLE permisos (
    id_permiso SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE, -- Ejemplo: Crear, Editar, Eliminar
    descripcion TEXT
);

-- Relación entre Usuarios y Roles
CREATE TABLE usuario_roles (
    id_usuario INT NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol) ON DELETE CASCADE,
    PRIMARY KEY (id_usuario, id_rol)
);

-- Relación entre Roles y Permisos
CREATE TABLE rol_permisos (
    id_rol INT NOT NULL,
    id_permiso INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol) ON DELETE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES permisos(id_permiso) ON DELETE CASCADE,
    PRIMARY KEY (id_rol, id_permiso)
);

-- Tabla de Usuarios
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    contrasena VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    FOREIGN KEY (rol_id) REFERENCES roles(id_rol)
);

-- Tabla de Roles
CREATE TABLE roles (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- Tabla de Facturas
CREATE TABLE facturas (
    id_factura SERIAL PRIMARY KEY,
    id_cita INT NOT NULL,
    fecha_emision DATE NOT NULL,
    monto NUMERIC(10, 2) NOT NULL,
    estado VARCHAR(20) DEFAULT 'Pendiente',
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita)
);

-- Tabla de Proveedores de Material Médico
CREATE TABLE proveedores_material_medico (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(15),
    email VARCHAR(100)
);

-- Tabla de Proveedores de Laboratorio
CREATE TABLE proveedores_laboratorio (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(15),
    email VARCHAR(100)
);

-- Tabla de Derivaciones a Especialistas
CREATE TABLE derivaciones (
    id_derivacion SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico_remitente INT NOT NULL,
    id_medico_destino INT NOT NULL,
    motivo TEXT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_medico_remitente) REFERENCES medicos(id_medico),
    FOREIGN KEY (id_medico_destino) REFERENCES medicos(id_medico)
);

-- Tabla de Tratamientos
CREATE TABLE tratamientos (
    id_tratamiento SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
);

-- Tabla de Historia Clínica
CREATE TABLE historia_clinica (
    id_historia SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL,
    descripcion TEXT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente)
);

-- Ajustes adicionales a tablas existentes
ALTER TABLE citas
ADD COLUMN ref_factura INT,
ADD FOREIGN KEY (ref_factura) REFERENCES facturas(id_factura);
