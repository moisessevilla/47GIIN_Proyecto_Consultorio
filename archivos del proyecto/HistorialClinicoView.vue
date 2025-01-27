<template>
  <div class="contenido">
    <h1>Gestión del Historial Clínico</h1>

    <!-- Formulario para crear o editar historial clínico -->
    <div class="formulario">
      <h2>{{ isEditing ? "Editar Registro Clínico" : "Nuevo Registro Clínico" }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="id_paciente">Paciente:</label>
          <select v-model="form.id_paciente" id="id_paciente" required>
            <option value="" disabled>Seleccione un paciente</option>
            <option v-for="paciente in pacientes" :key="paciente.id_paciente" :value="paciente.id_paciente">
              {{ paciente.nombre }} {{ paciente.apellido }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="descripcion">Descripción:</label>
          <textarea v-model="form.descripcion" id="descripcion" required></textarea>
        </div>
        <div class="form-group">
          <label for="observaciones">Observaciones:</label>
          <textarea v-model="form.observaciones" id="observaciones"></textarea>
        </div>
        <div class="form-group">
          <label for="fecha_apertura">Fecha de Apertura:</label>
          <input type="date" v-model="form.fecha_apertura" id="fecha_apertura" required />
        </div>
        <button type="submit">{{ isEditing ? "Actualizar" : "Registrar" }}</button>
        <button type="button" @click="resetForm">Cancelar</button>
      </form>
    </div>

    <!-- Campo de búsqueda -->
    <div class="busqueda-container">
      <label for="searchKey" class="busqueda-label">Filtro:</label>
      <select id="searchKey" v-model="searchKey" class="busqueda-select">
        <option value="id_historia">ID Historia</option>
        <option value="paciente">Paciente</option>
        <option value="descripción">Observaciones</option>
        <option value="fecha_apertura">Fecha de Apertura</option>
      </select>
      <input type="text" v-model="searchValue" class="busqueda-input" placeholder="Ingrese criterio de búsqueda" />
    </div>

    <!-- Contenedor para mostrar registros del historial clínico -->
    <div class="tabla-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Paciente</th>
            <th>Descripción</th>
            <th>Observaciones</th>
            <th>Fecha de Apertura</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="historial in historialClinico" :key="historial.id_historia">
            <td>{{ historial.id_historia }}</td>
            <td>{{ getPaciente(historial.id_paciente) }}</td>
            <td>{{ historial.descripcion }}</td>
            <td>{{ historial.observaciones || "N/A" }}</td>
            <td>{{ historial.fecha_apertura }}</td>
            <td>
              <button @click="editHistorial(historial)">Editar</button>
              <button @click="deleteHistorial(historial.id_historia)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      historialClinico: [],
      pacientes: [],
      form: {
        id_historia: null,
        id_paciente: "",
        descripcion: "",
        observaciones: "",
        fecha_apertura: "",
      },
      isEditing: false,
    };
  },
  methods: {
    async fetchHistorialClinico() {
      try {
        const response = await axios.get("/historia_clinica/");
        this.historialClinico = response.data;
      } catch (error) {
        console.error("Error al obtener el historial clínico:", error);
      }
    },
    async fetchPacientes() {
      try {
        const response = await axios.get("/paciente/");
        this.pacientes = response.data;
      } catch (error) {
        console.error("Error al obtener los pacientes:", error);
      }
    },
    handleSubmit() {
      if (this.isEditing) {
        this.updateHistorial();
      } else {
        this.createHistorial();
      }
    },
    async createHistorial() {
      try {
        await axios.post("/historia_clinica/", this.form);
        this.fetchHistorialClinico();
        this.resetForm();
      } catch (error) {
        console.error("Error al crear el registro clínico:", error);
      }
    },
    async updateHistorial() {
      try {
        await axios.put(`/historia_clinica/${this.form.id_historia}/`, this.form);
        this.fetchHistorialClinico();
        this.resetForm();
      } catch (error) {
        console.error("Error al actualizar el registro clínico:", error);
      }
    },
    async deleteHistorial(id) {
      try {
        await axios.delete(`/historia_clinica/${id}/`);
        this.fetchHistorialClinico();
      } catch (error) {
        console.error("Error al eliminar el registro clínico:", error);
      }
    },
    editHistorial(historial) {
      this.form = { ...historial };
      this.isEditing = true;
    },
    resetForm() {
      this.form = {
        id_historia: null,
        id_paciente: "",
        descripcion: "",
        observaciones: "",
        fecha_apertura: "",
      };
      this.isEditing = false;
    },
    getPaciente(id) {
      const paciente = this.pacientes.find((p) => p.id_paciente === id);
      return paciente ? `${paciente.nombre} ${paciente.apellido}` : "N/A";
    },
  },
  mounted() {
    this.fetchHistorialClinico();
    this.fetchPacientes();
  },
};
</script>
