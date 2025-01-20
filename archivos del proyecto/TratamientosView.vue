<template>
  <div class="contenido">
    <h1>Gestión de Tratamientos</h1>

    <!-- Formulario para agregar o editar tratamientos -->
    <form @submit.prevent="handleSubmit" class="formulario">
      <div class="form-group">
        <label for="id_paciente">Paciente:</label>
        <select id="id_paciente" v-model="form.id_paciente" required>
          <option v-for="paciente in pacientes" :key="paciente.id_paciente" :value="paciente.id_paciente">
            {{ paciente.nombre }} {{ paciente.apellido }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="id_medico">Médico:</label>
        <select id="id_medico" v-model="form.id_medico" required>
          <option v-for="medico in medicos" :key="medico.id_medico" :value="medico.id_medico">
            {{ medico.nombre }} ({{ medico.especialidad }})
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="descripcion">Descripción:</label>
        <textarea id="descripcion" v-model="form.descripcion" required></textarea>
      </div>

      <div class="form-group">
        <label for="fecha_inicio">Fecha de Inicio:</label>
        <input type="date" id="fecha_inicio" v-model="form.fecha_inicio" @change="formatFecha" required />
      </div>

      <div class="form-group">
        <label for="fecha_fin">Fecha de Fin:</label>
        <input type="date" id="fecha_fin" v-model="form.fecha_fin" @change="formatFecha" />
      </div>

      <div class="form-group">
        <label for="costo">Costo:</label>
        <input type="number" id="costo" v-model="form.costo" />
      </div>

      <div class="form-buttons">
        <button type="submit">{{ form.id_tratamiento ? 'Actualizar' : 'Agregar' }} Tratamiento</button>
        <button type="button" v-if="form.id_tratamiento" @click="resetForm">Cancelar</button>
      </div>
    </form>

    <!-- Campo de búsqueda -->
    <div class="busqueda-container">
      <label for="searchKey" class="busqueda-label">Filtro:</label>
      <select id="searchKey" v-model="searchKey" class="busqueda-select">
        <option value="id_paciente">ID Paciente</option>
        <option value="paciente">Paciente</option>
        <option value="especialidad">Especialidad</option>
        <option value="descripción">Descripción</option>
        <option value="fecha_inicio">Fecha Inicio</option>
        <option value="fecha_fin">Fecha Fin</option>
      </select>
      <input type="text" v-model="searchValue" class="busqueda-input" placeholder="Ingrese criterio de búsqueda" />
    </div>

    <!-- Tabla de tratamientos -->
    <div class="tabla-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Paciente</th>
            <th>Médico</th>
            <th>Descripción</th>
            <th>Fecha Inicio</th>
            <th>Fecha Fin</th>
            <th>Costo</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tratamiento in tratamientos" :key="tratamiento.id_tratamiento">
            <td>{{ tratamiento.id_tratamiento }}</td>
            <td>{{ tratamiento.paciente.nombre }} {{ tratamiento.paciente.apellido }}</td>
            <td>{{ tratamiento.medico.especialidad }}</td>
            <td>{{ tratamiento.descripcion }}</td>
            <td>{{ formatFecha(tratamiento.fecha_inicio) }}</td>
            <td>{{ formatFecha(tratamiento.fecha_fin) || 'N/A' }}</td>
            <td>{{ tratamiento.costo }} €</td>
            <td>
              <button @click="editTratamiento(tratamiento)">Editar</button>
              <button @click="deleteTratamiento(tratamiento.id_tratamiento)">Eliminar</button>
            </td>
          </tr>


        </tbody>
      </table>
    </div>
  </div>
</template>

<script>

import axios from "axios";
import moment from 'moment';

export default {
  data() {
    return {
      tratamientos: [],
      pacientes: [],
      medicos: [],
      form: {
        id_tratamiento: null,
        id_paciente: "",
        id_medico: "",
        descripcion: "",
        fecha_inicio: "",
        fecha_fin: "",
        costo: "",
      },
    };
  },

  methods: {
    async fetchTratamientos() {
      try {
        const tratamientosResponse = await axios.get("/tratamiento/");
        const pacientesResponse = await axios.get("/paciente/");
        const medicosResponse = await axios.get("/medico/");

        const pacientes = pacientesResponse.data;
        const medicos = medicosResponse.data;

        this.tratamientos = tratamientosResponse.data.map(tratamiento => {
          const paciente = pacientes.find(p => p.id_paciente === tratamiento.id_paciente);
          const medico = medicos.find(m => m.id_medico === tratamiento.id_medico);

          return {
            ...tratamiento,
            paciente: paciente || { nombre: "Desconocido", apellido: "" },
            medico: medico || { especialidad: "Desconocida" }
          };
        });
      } catch (error) {
        console.error("Error al obtener los tratamientos:", error);
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

    async fetchMedicos() {
      try {
        const response = await axios.get("/medico/");
        this.medicos = response.data;
      } catch (error) {
        console.error("Error al obtener los médicos:", error);
      }
    },

    formatFecha(fecha) {
      if (!fecha) return 'Baja indefinida';
      return moment(fecha, ["YYYY-MM-DD", "DD-MM-YYYY"]).format("DD-MM-YYYY");
    },

    async handleSubmit() {
      try {
        if (this.form.id_tratamiento) {
          await axios.put(`/tratamiento/${this.form.id_tratamiento}/`, this.form);
          alert("Tratamiento actualizado correctamente.");
        } else {
          await axios.post("/tratamiento/", this.form);
          alert("Tratamiento agregado correctamente.");
        }
        this.fetchTratamientos();
        this.resetForm();
      } catch (error) {
        console.error("Error al guardar el tratamiento:", error);
      }
    },

    editTratamiento(tratamiento) {
      this.form = { ...tratamiento };
    },

    async deleteTratamiento(id_tratamiento) {
      if (confirm("¿Estás seguro de eliminar este tratamiento?")) {
        try {
          await axios.delete(`/tratamiento/${id_tratamiento}/`);
          alert("Tratamiento eliminado correctamente.");
          this.fetchTratamientos();
        } catch (error) {
          console.error("Error al eliminar el tratamiento:", error);
        }
      }
    },

    resetForm() {
      this.form = {
        id_tratamiento: null,
        id_paciente: "",
        id_medico: "",
        descripcion: "",
        fecha_inicio: "",
        fecha_fin: "",
        costo: "",
      };
    },
  },

  mounted() {
    this.fetchTratamientos();
    this.fetchPacientes();
    this.fetchMedicos();
  },
};
</script>

<style>
textarea#descripcion {
  width: 66%;
  /* Igual de ancho que los demás campos */
  height: 4em;
  /* El doble de altura (puedes ajustar el valor según prefieras) */
  padding: 5px;
  /* Asegura que el texto tenga espacio interno */
  border: 1px solid #ccc;
  /* Estilo consistente */
  border-radius: 4px;
  /* Opcional: esquinas redondeadas */
  resize: vertical;
  /* Opcional: desactiva el redimensionamiento manual */
  box-sizing: border-box;
  /* Considera el padding en el ancho total */
}

.contenido {
  padding: 20px;
}

.formulario {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-buttons button {
  margin-right: 10px;
}

.tabla-container {
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

th {
  background-color: #f2f2f2;
}
</style>
