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


