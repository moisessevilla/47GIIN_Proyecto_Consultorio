<template>
  <div class="seguridad-auditoria">
    <h1>Seguridad y Auditoría</h1>

    <div class="auditoria-seccion">
      <div class="graficos-container">
        <div class="grafico">
          <h2>Distribución de Roles</h2>
          <apexchart type="pie" :options="rolesChartOptions" :series="rolesChartData" />
        </div>
        <div class="grafico">
          <h2>Actividades por Usuario</h2>
          <apexchart type="bar" :options="actividadesChartOptions" :series="actividadesChartData" />
        </div>
      </div>

      <div class="tabla-auditoria">
        <h2>Registros de Auditoría</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Usuario</th>
              <th>Acción</th>
              <th>Fecha</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="registro in auditoria" :key="registro.id">
              <td>{{ registro.id }}</td>
              <td>{{ registro.usuario }}</td>
              <td>{{ registro.accion }}</td>
              <td>{{ registro.fecha }}</td>
              <td>{{ registro.estado }}</td>
            </tr>
          </tbody>
        </table>
      </div>
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
      auditoria: [], // Datos de auditoría obtenidos desde el backend
      rolesChartOptions: {
        chart: {
          type: "pie",
        },
        labels: ["Administradores", "Médicos", "Pacientes", "Usuarios de Clínica"],
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {
                width: 300,
              },
              legend: {
                position: "bottom",
              },
            },
          },
        ],
      },
      rolesChartData: [5, 15, 70, 10], // Datos ficticios para el gráfico de roles
      actividadesChartOptions: {
        chart: {
          type: "bar",
        },
        xaxis: {
          categories: ["Admin", "Médico", "Paciente", "Usuario de Clínica"],
        },
      },
      actividadesChartData: [
        {
          name: "Acciones",
          data: [50, 120, 200, 80], // Datos ficticios para actividades
        },
      ],
    };
  },
  methods: {
    async fetchAuditoria() {
      try {
        const response = await axios.get("/auditoria/");
        this.auditoria = response.data;
      } catch (error) {
        console.error("Error al cargar los datos de auditoría:", error);
      }
    },
  },
  mounted() {
    this.fetchAuditoria();
  },
};
</script>

<style scoped>
.seguridad-auditoria {
  padding: 20px;
}

.auditoria-seccion {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.graficos-container {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 20px;
}

.grafico {
  flex: 1;
  min-width: 300px;
}

.tabla-auditoria {
  margin-top: 20px;
}

.tabla-auditoria table {
  width: 100%;
  border-collapse: collapse;
}

.tabla-auditoria th,
.tabla-auditoria td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.tabla-auditoria th {
  background-color: #f4f4f4;
  font-weight: bold;
}
</style>
