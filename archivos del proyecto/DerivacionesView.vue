<template>
  <div class="contenido">
    <h1>Gestión de Derivaciones</h1>

    <!-- Formulario para crear o editar derivaciones -->
    <div class="formulario">
      <h2>{{ isEditing ? "Editar Derivación" : "Nueva Derivación" }}</h2>
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
          <label for="id_medico_remitente">Médico Remitente:</label>
          <select v-model="form.id_medico_remitente" id="id_medico_remitente" required>
            <option value="" disabled>Seleccione el Médico Remitente</option>
            <option v-for="medico in medicos" :key="medico.id_medico" :value="medico.id_medico">
              {{ medico.nombre }} ({{ medico.especialidad }})
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="id_medico_destino">Médico Destino:</label>
          <select v-model="form.id_medico_destino" id="id_medico_destino" required>
            <option value="" disabled>Seleccione el Médico Destino</option>
            <option v-for="medico in medicos" :key="medico.id_medico" :value="medico.id_medico">
              {{ medico.nombre }} ({{ medico.especialidad }})
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="motivo">Motivo:</label>
          <textarea v-model="form.motivo" id="motivo" required></textarea>
        </div>
        <div class="form-group">
          <label for="fecha_derivacion">Fecha de Derivación:</label>
          <input type="date" v-model="form.fecha_derivacion" id="fecha_derivacion" required />
        </div>
        <button type="submit">{{ isEditing ? "Actualizar" : "Registrar" }}</button>
        <button type="button" @click="resetForm">Cancelar</button>
      </form>
    </div>

    <!-- Campo de búsqueda -->
    <div class="busqueda-container">
      <label for="searchKey" class="busqueda-label">Filtro:</label>
      <select id="searchKey" v-model="searchKey" class="busqueda-select">
        <option value="id_derivacion">ID Derivación</option>
        <option value="paciente">Paciente</option>
        <option value="medico_remitente">Médico Remitente</option>
        <option value="medico_destino">Médico Destino</option>
        <option value="motivo">Motivo</option>
        <option value="fecha_derivacion">Fecha Derivacion</option>
      </select>
      <input type="text" v-model="searchValue" class="busqueda-input" placeholder="Ingrese criterio de búsqueda" />
    </div>

    <!-- Contenedor para mostrar derivaciones -->
    <div class="tabla-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Paciente</th>
            <th>Médico Remitente</th>
            <th>Médico Destino</th>
            <th>Motivo</th>
            <th>Fecha de Derivación</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="derivacion in derivaciones" :key="derivacion.id_derivacion">
            <td>{{ derivacion.id_derivacion }}</td>
            <td>{{ getPaciente(derivacion.id_paciente) }}</td>
            <td>{{ getMedico(derivacion.id_medico_remitente) }}</td>
            <td>{{ getMedico(derivacion.id_medico_destino) }}</td>
            <td>{{ derivacion.motivo }}</td>
            <td>{{ derivacion.fecha_derivacion }}</td>
            <td>
              <button @click="editDerivacion(derivacion)">Editar</button>
              <button @click="deleteDerivacion(derivacion.id_derivacion)">Eliminar</button>
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
      derivaciones: [],
      pacientes: [],
      medicos: [],
      form: {
        id_derivacion: null,
        id_paciente: "",
        id_medico_remitente: "",
        id_medico_destino: "",
        motivo: "",
        fecha_derivacion: "",
      },
      isEditing: false,
    };
  },
  methods: {
    async fetchDerivaciones() {
      try {
        const response = await axios.get("/derivaciones/");
        this.derivaciones = response.data;
      } catch (error) {
        console.error("Error al obtener derivaciones:", error);
      }
    },
    async fetchPacientes() {
      try {
        const response = await axios.get("/paciente/");
        this.pacientes = response.data;
      } catch (error) {
        console.error("Error al obtener pacientes:", error);
      }
    },
    async fetchMedicos() {
      try {
        const response = await axios.get("/medico/");
        this.medicos = response.data;
      } catch (error) {
        console.error("Error al obtener médicos:", error);
      }
    },
    handleSubmit() {
      if (this.isEditing) {
        this.updateDerivacion();
      } else {
        this.createDerivacion();
      }
    },
    async createDerivacion() {
      try {
        await axios.post("/derivaciones/", this.form);
        this.fetchDerivaciones();
        this.resetForm();
      } catch (error) {
        console.error("Error al crear derivación:", error);
      }
    },
    async updateDerivacion() {
      try {
        await axios.put(`/derivaciones/${this.form.id_derivacion}/`, this.form);
        this.fetchDerivaciones();
        this.resetForm();
      } catch (error) {
        console.error("Error al actualizar derivación:", error);
      }
    },
    async deleteDerivacion(id) {
      try {
        await axios.delete(`/derivaciones/${id}/`);
        this.fetchDerivaciones();
      } catch (error) {
        console.error("Error al eliminar derivación:", error);
      }
    },
    editDerivacion(derivacion) {
      this.form = { ...derivacion };
      this.isEditing = true;
    },
    resetForm() {
      this.form = {
        id_derivacion: null,
        id_paciente: "",
        id_medico_remitente: "",
        id_medico_destino: "",
        motivo: "",
        fecha_derivacion: "",
      };
      this.isEditing = false;
    },
    getPaciente(id) {
      const paciente = this.pacientes.find((p) => p.id_paciente === id);
      return paciente ? `${paciente.nombre} ${paciente.apellido}` : "N/A";
    },
    getMedico(id) {
      const medico = this.medicos.find((m) => m.id_medico === id);
      return medico ? `${medico.nombre} (${medico.especialidad})` : "N/A";
    },
  },
  mounted() {
    this.fetchDerivaciones();
    this.fetchPacientes();
    this.fetchMedicos();
  },
};
</script>
