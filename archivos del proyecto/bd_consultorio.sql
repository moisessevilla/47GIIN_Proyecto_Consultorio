-- Crear la base de datos para PostgreSQL
CREATE DATABASE IF NOT EXISTS consultorio;

-- Crear la tabla Paciente
CREATE TABLE Paciente (
    id_paciente SERIAL PRIMARY KEY,
    dni VARCHAR(9) UNIQUE, -- Nuevo campo DNI
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    contrasena VARCHAR(100) NOT NULL
);
