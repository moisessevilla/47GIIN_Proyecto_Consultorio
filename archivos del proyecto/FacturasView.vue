<template>
  <div class="contenido">
    <h1>Gestión de Facturas</h1>

    <!-- Formulario para crear o editar una factura -->
    <div class="formulario">
      <h2>{{ isEditing ? "Editar Factura" : "Nueva Factura" }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="id_cita">Cita:</label>
          <select v-model="form.id_cita" id="id_cita" required>
            <option v-for="cita in citas" :key="cita.id_cita" :value="cita.id_cita">
              Ref: {{ cita.refcita }} - Paciente: {{ getPacienteName(cita.id_paciente) }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="id_tratamiento">Tratamiento:</label>
          <select v-model="form.id_tratamiento" id="id_tratamiento" required>
            <option v-for="tratamiento in tratamientos" :key="tratamiento.id_tratamiento"
              :value="tratamiento.id_tratamiento">
              Costo: €{{ tratamiento.costo }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="concepto">Concepto:</label>
          <textarea v-model="form.concepto" id="concepto" required></textarea>
        </div>
        <div class="form-group">
          <label for="fecha_emision">Fecha de Emisión:</label>
          <input type="date" v-model="form.fecha_emision" id="fecha_emision" required />
        </div>
        <div class="form-group">
          <label for="fecha_cobro">Fecha de Cobro:</label>
          <input type="date" v-model="form.fecha_cobro" id="fecha_cobro" />
        </div>
        <div class="form-group">
          <label for="estado">Estado:</label>
          <select v-model="form.estado" id="estado" required>
            <option value="Pendiente">Pendiente</option>
            <option value="Pagada">Pagada</option>
            <option value="Cancelada">Cancelada</option>
          </select>
        </div>
        <button type="submit">{{ isEditing ? "Actualizar" : "Registrar" }}</button>
        <button type="button" @click="resetForm">Cancelar</button>
      </form>
    </div>

    <!-- Campo de búsqueda -->
    <div class="busqueda-container">
      <label for="searchKey" class="busqueda-label">Filtro:</label>
      <select id="searchKey" v-model="searchKey" class="busqueda-select">
        <option value="id_factura">ID Factura</option>
        <option value="ref_factura">Ref. Factura</option>
        <option value="refcita">Ref. Cita</option>
        <option value="costo">Costo</option>
        <option value="c_concepto">Concepto</option>
        <option value="fecha_emision">Fecha Emisión</option>
        <option value="fecha_cobro">Fecha Cobro</option>
        <option value="estado">Estado</option>
      </select>
      <input type="text" v-model="searchValue" class="busqueda-input" placeholder="Ingrese criterio de búsqueda" />
    </div>



    <!-- Contenedor para mostrar facturas -->
    <div class="tabla-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Ref. Factura</th>
            <th>Cita</th>
            <th>Costo</th>
            <th>Concepto</th>
            <th>Fecha Emisión</th>
            <th>Fecha Cobro</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="factura in facturas" :key="factura.id_factura">
            <td>{{ factura.id_factura }}</td>
            <td>{{ factura.ref_factura }}</td>
            <td>{{ getCitaInfo(factura.id_cita) }}</td>
            <td>€{{ getTratamientoCosto(factura.id_tratamiento) }}</td>
            <td>{{ factura.concepto }}</td>
            <td>{{ factura.fecha_emision }}</td>
            <td>{{ factura.fecha_cobro || "N/A" }}</td>
            <td>{{ factura.estado }}</td>
            <td>
              <button @click="generarPDF(factura)">PDF</button>
              <button @click="editFactura(factura)">Editar</button>
              <button @click="deleteFactura(factura.id_factura)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import logo from "@/assets/imagenes/salud_v3.png";
import axios from "axios";
import autoTable from "jspdf-autotable"; // Sin cambios aquí
import jsPDF from "jspdf/dist/jspdf.umd"; // Corrige para usar la versión UMD


export default {
  data() {
    return {
      facturas: [
        {
          id_factura: 1,
          ref_factura: "FAC20250001",
          ref_cita: "CIT20250045",
          paciente: "Juan Pérez",
          tratamiento: 200,
          concepto: "Consulta médica y tratamiento adicional",
          fecha_emision: "2025-01-20",
          fecha_cobro: null,
          estado: "Pendiente"
        }
        // Agrega más facturas simuladas o carga desde el backend
      ],
      citas: [],
      tratamientos: [],
      pacientes: [],
      form: {
        id_factura: null,
        ref_factura: "",
        id_cita: "",
        id_tratamiento: "",
        concepto: "",
        fecha_emision: "",
        fecha_cobro: "",
        estado: "Pendiente",
      },
      isEditing: false,
    };
  },
  methods: {
    generarPDF(factura) {
      const doc = new jsPDF();

      // Validar datos clave
      const tratamientoCosto = factura.tratamiento || 0; // Si es undefined, usa 0
      const concepto = factura.concepto || "Sin concepto"; // Predeterminado si no existe

      // Calcular IVA y total con IVA
      const ivaPorcentaje = 21; // IVA del 21%
      const ivaMonto = (tratamientoCosto * ivaPorcentaje) / 100;
      const totalConIva = tratamientoCosto + ivaMonto;

      // Logo y encabezado
      const img = new Image();
      img.src = logo;
      doc.addImage(img, "PNG", 140, 5, 20, 20);
      doc.setFontSize(16);
      doc.text("Clínica Rehabilita tu alma", 70, 20);
      doc.setFontSize(12);
      doc.text("Factura Detallada", 10, 40);

      // Información general de la factura
      doc.setFontSize(10);
      doc.text(`Referencia Factura: ${factura.ref_factura}`, 10, 50);
      doc.text(`Referencia Cita: ${factura.ref_cita}`, 10, 60);
      doc.text(`Paciente: ${factura.paciente}`, 10, 70);
      doc.text(`Fecha Emisión: ${factura.fecha_emision}`, 10, 80);
      doc.text(`Fecha Cobro: ${factura.fecha_cobro || "N/A"}`, 10, 90);
      doc.text(`Estado: ${factura.estado}`, 10, 100);

      // Detalles del tratamiento
      autoTable(doc, {
        startY: 110,
        head: [["Concepto", "Precio sin IVA", "IVA (21%)", "Total con IVA"]],
        body: [[
          concepto,
          `${tratamientoCosto.toFixed(2)} €`,
          `${ivaMonto.toFixed(2)} €`,
          `${totalConIva.toFixed(2)} €`
        ]]
      });

      // Total final
      const startY = doc.lastAutoTable.finalY + 10;
      doc.text(`Total sin IVA: ${tratamientoCosto.toFixed(2)} €`, 10, startY);
      doc.text(`IVA (21%): ${ivaMonto.toFixed(2)} €`, 10, startY + 10);
      doc.text(`Total con IVA: ${totalConIva.toFixed(2)} €`, 10, startY + 20);

      // Guardar el PDF
      doc.save(`Factura_${factura.ref_factura}.pdf`);
    },

    async fetchFacturas() {
      try {
        const response = await axios.get("/facturas/");
        this.facturas = response.data;
      } catch (error) {
        console.error("Error al obtener las facturas:", error);
      }
    },

    async fetchCitas() {
      try {
        const response = await axios.get("/cita/");
        this.citas = response.data;
      } catch (error) {
        console.error("Error al obtener las citas:", error);
      }
    },

    async fetchTratamientos() {
      try {
        const response = await axios.get("/tratamiento/");
        this.tratamientos = response.data;
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

    handleSubmit() {
      if (this.isEditing) {
        this.updateFactura();
      } else {
        this.createFactura();
      }
    },

    async createFactura() {
      try {
        await axios.post("/facturas/", this.form);
        this.fetchFacturas();
        this.resetForm();
      } catch (error) {
        console.error("Error al crear la factura:", error);
      }
    },

    async updateFactura() {
      try {
        await axios.put(`/facturas/${this.form.id_factura}/`, this.form);
        this.fetchFacturas();
        this.resetForm();
      } catch (error) {
        console.error("Error al actualizar la factura:", error);
      }
    },

    async deleteFactura(id) {
      try {
        await axios.delete(`/facturas/${id}/`);
        this.fetchFacturas();
      } catch (error) {
        console.error("Error al eliminar la factura:", error);
      }
    },

    editFactura(factura) {
      this.form = { ...factura };
      this.isEditing = true;
    },

    resetForm() {
      this.form = {
        id_factura: null,
        ref_factura: "",
        id_cita: "",
        id_tratamiento: "",
        concepto: "",
        fecha_emision: "",
        fecha_cobro: "",
        estado: "Pendiente",
      };
      this.isEditing = false;
    },

    getPacienteName(id) {
      const paciente = this.pacientes.find((p) => p.id_paciente === id);
      return paciente ? `${paciente.nombre} ${paciente.apellido}` : "N/A";
    },

    getCitaInfo(id) {
      const cita = this.citas.find((c) => c.id_cita === id);
      if (!cita) return "N/A";
      const paciente = this.getPacienteName(cita.id_paciente);
      return `Ref: ${cita.refcita} - Paciente: ${paciente}`;
    },

    getTratamientoCosto(id) {
      const tratamiento = this.tratamientos.find((t) => t.id_tratamiento === id);
      return tratamiento ? tratamiento.costo : "N/A";
    },
  },

  mounted() {
    this.fetchFacturas();
    this.fetchCitas();
    this.fetchTratamientos();
    this.fetchPacientes();
  },
};
</script>

<style>
.contenido {
  padding: 20px;
}

.formulario {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

textarea {
  width: 55%;
  height: 80px;
}

textarea#concepto {
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


.tabla-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
}
</style>
