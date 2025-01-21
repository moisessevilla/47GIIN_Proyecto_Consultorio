<template>
  <div class="contenido">
    <h1>Seguridad y Auditoría</h1>

    <!-- Gráficos de auditoría -->
    <div class="graficos">
      <div id="usuarios-grafico">
        <apexchart type="pie" height="300" :options="usuariosOptions" :series="usuariosData" />
      </div>
      <div id="tratamientos-grafico">
        <apexchart type="bar" height="300" :options="tratamientosOptions" :series="tratamientosData" />
      </div>
      <div id="derivaciones-grafico">
        <apexchart type="line" height="300" :options="derivacionesOptions" :series="derivacionesData" />
      </div>
      <div id="facturas-grafico">
        <apexchart type="bar" height="300" :options="facturasOptions" :series="facturasData" />
      </div>
      <div id="historial-grafico">
        <apexchart type="line" height="300" :options="historialOptions" :series="historialData" />
      </div>
      <div id="proveedores-grafico">
        <apexchart type="donut" height="300" :options="proveedoresOptions" :series="proveedoresData" />
      </div>
    </div>

    <!-- Tabla de auditoría -->
    <div class="tabla-container">
      <h2>Detalle de Auditoría</h2>
      <table>
        <thead>
          <tr>
            <th>Tabla</th>
            <th>Conteo</th>
            <th>Última Actualización</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(detalle, index) in detallesAuditoria" :key="index">
            <td>{{ detalle.tabla }}</td>
            <td>{{ detalle.conteo }}</td>
            <td>{{ detalle.ultima_actualizacion }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import VueApexCharts from "vue3-apexcharts";

export default {
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      usuariosData: [],
      tratamientosData: [],
      derivacionesData: [],
      facturasData: [],
      historialData: [],
      proveedoresData: [],
      usuariosOptions: {
        chart: {
          type: "pie",
        },
        labels: ["Activos", "Inactivos"],
        title: {
          text: "Usuarios Activos vs Inactivos",
        },
      },
      tratamientosOptions: {
        chart: {
          type: "bar",
        },
        xaxis: {
          categories: ["Enero", "Febrero", "Marzo", "Abril", "Mayo"],
        },
        title: {
          text: "Tratamientos por Mes",
        },
      },
      derivacionesOptions: {
        chart: {
          type: "line",
        },
        xaxis: {
          categories: ["Enero", "Febrero", "Marzo", "Abril", "Mayo"],
        },
        title: {
          text: "Derivaciones Mensuales",
        },
      },
      facturasOptions: {
        chart: {
          type: "bar",
        },
        xaxis: {
          categories: ["Pagadas", "Pendientes", "Anuladas"],
        },
        title: {
          text: "Estado de Facturas",
        },
      },
      historialOptions: {
        chart: {
          type: "line",
        },
        xaxis: {
          categories: ["Enero", "Febrero", "Marzo", "Abril", "Mayo"],
        },
        title: {
          text: "Historial Clínico Mensual",
        },
      },
      proveedoresOptions: {
        chart: {
          type: "donut",
        },
        labels: ["Activos", "Inactivos"],
        title: {
          text: "Proveedores Activos vs Inactivos",
        },
      },
      detallesAuditoria: [],
    };
  },
  methods: {
    async fetchData() {
      try {
        const usuariosResponse = await axios.get("/usuarios/conteo");
        const tratamientosResponse = await axios.get("/tratamientos/conteo");
        const derivacionesResponse = await axios.get("/derivaciones/conteo");
        const facturasResponse = await axios.get("/facturas/conteo");
        const historialResponse = await axios.get("/historial/conteo");
        const proveedoresResponse = await axios.get("/proveedores/conteo");

        this.usuariosData = usuariosResponse.data;
        this.tratamientosData = tratamientosResponse.data.series;
        this.derivacionesData = derivacionesResponse.data.series;
        this.facturasData = facturasResponse.data.series;
        this.historialData = historialResponse.data.series;
        this.proveedoresData = proveedoresResponse.data.series;

        this.detallesAuditoria = [
          {
            tabla: "Usuarios",
            conteo: usuariosResponse.data.reduce((a, b) => a + b, 0),
            ultima_actualizacion: "2025-01-20",
          },
          {
            tabla: "Tratamientos",
            conteo: tratamientosResponse.data.total,
            ultima_actualizacion: "2025-01-20",
          },
          {
            tabla: "Derivaciones",
            conteo: derivacionesResponse.data.total,
            ultima_actualizacion: "2025-01-20",
          },
          {
            tabla: "Facturas",
            conteo: facturasResponse.data.total,
            ultima_actualizacion: "2025-01-20",
          },
          {
            tabla: "Historial Clínico",
            conteo: historialResponse.data.total,
            ultima_actualizacion: "2025-01-20",
          },
          {
            tabla: "Proveedores",
            conteo: proveedoresResponse.data.total,
            ultima_actualizacion: "2025-01-20",
          },
        ];
      } catch (error) {
        console.error("Error al cargar los datos de auditoría:", error);
      }
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style>
.contenido {
  padding: 20px;
}

.graficos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.tabla-container table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.tabla-container th,
.tabla-container td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

.tabla-container th {
  background-color: #f9f9f9;
}
</style>
