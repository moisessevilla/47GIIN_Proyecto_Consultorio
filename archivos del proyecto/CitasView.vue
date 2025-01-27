<template>
  <div class="contenido">
    <h1>Consulta de Citas</h1>

    <!-- Formulario para buscar cita -->
    <!--
    <form @submit.prevent="fetchCitaById" class="busqueda-form">
      <div class="form-group">
        <label for="id_cita">Buscar por ID de Cita:</label>
        <input type="number" id="id_cita" v-model="searchId" placeholder="Ingrese el ID de la cita" required />
        <button type="submit">Buscar</button>
      </div>
    </form>
  -->

    <!-- Contenedor de citas -->
    <div class="citas-contenedor">
      <div class="detalle-cita">
        <h2>Detalles de la Cita</h2>
        <p><strong>ID Cita:</strong><span>18</span></p>
        <p><strong>Referencia Cita:</strong><span>A085C531DAE</span></p>
        <p><strong>DNI:</strong><span>64564576D</span></p>
        <p><strong>Paciente:</strong><span>Roberto Gómez</span></p>
        <p><strong>Especialidad:</strong><span>Dermatología</span></p>
        <p><strong>Médico:</strong><span>Dra. Ana Fernández</span></p>
        <p><strong>Fecha:</strong><span>14-01-2025</span></p>
        <p><strong>Hora:</strong><span>15:00</span></p>
        <p><strong>Estado:</strong><span>confirmada</span></p>
      </div>
      <div class="detalle-cita">
        <h2>Detalles de la Cita</h2>
        <p><strong>ID Cita:</strong><span>20</span></p>
        <p><strong>Referencia Cita:</strong><span>EFCC60374AE</span></p>
        <p><strong>DNI:</strong><span>64564576D</span></p>
        <p><strong>Paciente:</strong><span>Roberto Gómez</span></p>
        <p><strong>Especialidad:</strong><span>Psiquiatría</span></p>
        <p><strong>Médico:</strong><span>Dr. Moises Sevilla</span></p>
        <p><strong>Fecha:</strong><span>13-01-2025</span></p>
        <p><strong>Hora:</strong><span>11:00</span></p>
        <p><strong>Estado:</strong><span>confirmada</span></p>
      </div>
    </div>


    <!-- Detalles de la cita -->
    <div v-if="cita" class="detalle-cita">
      <h2>Detalles de la Cita</h2>
      <p><strong>ID Cita:</strong> {{ cita.id_cita }}</p>
      <p><strong>Paciente:</strong> {{ cita.paciente_nombre }} ({{ cita.paciente_dni }})</p>
      <p><strong>Especialidad:</strong> {{ cita.medico_especialidad }}</p>
      <p><strong>Fecha:</strong> {{ cita.fecha }}</p>
      <p><strong>Hora:</strong> {{ cita.hora }}</p>
      <p><strong>Estado:</strong> {{ cita.estado }}</p>
    </div>

    <!-- Mensaje en caso de no encontrar la cita -->
    <div v-else-if="!loading && searchId && !cita" class="no-cita">
      <p>No se encontró ninguna cita con el ID proporcionado.</p>
    </div>

    <!-- Mensaje de error -->
    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      searchId: null, // ID de la cita a buscar
      cita: null, // Datos de la cita obtenida
      loading: false, // Indicador de carga
      error: null, // Mensaje de error
    };
  },
  methods: {
    async fetchCitaById() {
      // Restablecer valores previos
      this.cita = null;
      this.error = null;
      this.loading = true;

      try {
        //const response = await axios.get(`/cita/?id_cita=${this.searchId}`);
        const response = await axios.get(`/cita/?id_cita=${this.searchId}`);
        const data = response.data;

        // Reorganizar los datos para adaptarlos al frontend
        this.cita = {
          id_cita: data.id_cita,
          fecha: data.fecha,
          hora: data.hora,
          estado: data.estado || "Desconocido",
          paciente_nombre: `${data.id_paciente.nombre} ${data.id_paciente.apellido}`,
          paciente_dni: data.id_paciente.dni,
          medico_nombre: data.id_medico.nombre,
          medico_especialidad: data.id_medico.especialidad,
        };
      } catch (err) {
        console.error("Error al buscar la cita:", err);
        this.error = "Error al buscar la cita. Intente nuevamente.";
      } finally {
        this.loading = false; // Finalizar carga
      }
    },
  },
};
</script>
