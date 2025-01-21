<template>
  <div class="contenido">
    <h1>Proveedores de Material de Laboratorio</h1>

    <!-- Formulario para crear/editar proveedor -->
    <form @submit.prevent="handleSubmit" class="formulario">
      <div class="form-row">
        <div class="form-group">
          <label for="nombre">Nombre:</label>
          <input id="nombre" v-model="form.nombre" type="text" required />
        </div>
        <div class="form-group">
          <label for="razon_social">Razón Social:</label>
          <input id="razon_social" v-model="form.razon_social" type="text" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="direccion">Dirección:</label>
          <textarea id="direccion" v-model="form.direccion"></textarea>
        </div>
        <div class="form-group">
          <label for="telefono">Teléfono:</label>
          <input id="telefono" v-model="form.telefono" type="text" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="email">Email:</label>
          <input id="email" v-model="form.email" type="email" />
        </div>
        <div class="form-group">
          <label for="persona_contacto">Persona de Contacto:</label>
          <input id="persona_contacto" v-model="form.persona_contacto" type="text" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="puesto_contacto">Puesto de Contacto:</label>
          <input id="puesto_contacto" v-model="form.puesto_contacto" type="text" />
        </div>
        <div class="form-group">
          <label for="horario_atencion">Horario de Atención:</label>
          <input id="horario_atencion" v-model="form.horario_atencion" type="text" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="metodo_pago">Método de Pago:</label>
          <input id="metodo_pago" v-model="form.metodo_pago" type="text" />
        </div>
        <div class="form-group">
          <label for="moneda">Moneda:</label>
          <input id="moneda" v-model="form.moneda" type="text" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="plazo_pago">Plazo de Pago (días):</label>
          <input id="plazo_pago" v-model="form.plazo_pago" type="number" />
        </div>
        <div class="form-group">
          <label for="categorias_producto">Categorías de Producto:</label>
          <textarea id="categorias_producto" v-model="form.categorias_producto"></textarea>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="tiempo_entrega">Tiempo de Entrega (días):</label>
          <input id="tiempo_entrega" v-model="form.tiempo_entrega" type="number" />
        </div>
        <div class="form-group">
          <label for="zona_cobertura">Zona de Cobertura:</label>
          <textarea id="zona_cobertura" v-model="form.zona_cobertura"></textarea>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="calidad_proveedor">Calidad del Proveedor:</label>
          <input id="calidad_proveedor" v-model="form.calidad_proveedor" type="text" />
        </div>
        <div class="form-group">
          <label for="fecha_alta">Fecha de Alta:</label>
          <input id="fecha_alta" v-model="form.fecha_alta" type="date" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="estado">Estado:</label>
          <input id="estado" v-model="form.estado" type="text" />
        </div>
        <div class="form-group">
          <label for="notas">Notas:</label>
          <textarea id="notas" v-model="form.notas"></textarea>
        </div>
      </div>

      <div class="form-buttons">
        <button type="submit">{{ form.id_proveedor ? 'Actualizar' : 'Crear' }} Proveedor</button>
        <button type="button" v-if="form.id_proveedor" @click="resetForm">Cancelar</button>
      </div>
    </form>

    <!-- Tabla para mostrar proveedores -->
    <div class="tabla-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Razón Social</th>
            <th>Teléfono</th>
            <th>Email</th>
            <th>Persona de Contacto</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="proveedor in proveedores" :key="proveedor.id_proveedor">
            <td>{{ proveedor.id_proveedor }}</td>
            <td>{{ proveedor.nombre }}</td>
            <td>{{ proveedor.razon_social }}</td>
            <td>{{ proveedor.telefono }}</td>
            <td>{{ proveedor.email }}</td>
            <td>{{ proveedor.persona_contacto }}</td>
            <td>{{ proveedor.estado }}</td>
            <td>
              <button @click="editProveedor(proveedor)">Editar</button>
              <button @click="deleteProveedor(proveedor.id_proveedor)">Eliminar</button>
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
      proveedores: [],
      form: {
        id_proveedor: null,
        nombre: "",
        razon_social: "",
        direccion: "",
        telefono: "",
        email: "",
        persona_contacto: "",
        puesto_contacto: "",
        horario_atencion: "",
        metodo_pago: "",
        moneda: "",
        plazo_pago: null,
        categorias_producto: "",
        tiempo_entrega: null,
        zona_cobertura: "",
        calidad_proveedor: "",
        fecha_alta: "",
        estado: "",
        notas: "",
      },
    };
  },
  methods: {
    async fetchProveedores() {
      try {
        const response = await axios.get("/proveedores_material_medico/");
        this.proveedores = response.data;
      } catch (error) {
        console.error("Error al obtener los proveedores:", error);
      }
    },
    async handleSubmit() {
      try {
        if (this.form.id_proveedor) {
          await axios.put(`/proveedores_material_medico/${this.form.id_proveedor}/`, this.form);
        } else {
          await axios.post("/proveedores_material_medico/", this.form);
        }
        this.fetchProveedores();
        this.resetForm();
      } catch (error) {
        console.error("Error al guardar el proveedor:", error);
      }
    },
    async deleteProveedor(id) {
      try {
        await axios.delete(`/proveedores_material_medico/${id}/`);
        this.fetchProveedores();
      } catch (error) {
        console.error("Error al eliminar el proveedor:", error);
      }
    },
    editProveedor(proveedor) {
      this.form = { ...proveedor };
    },
    resetForm() {
      this.form = {
        id_proveedor: null,
        nombre: "",
        razon_social: "",
        direccion: "",
        telefono: "",
        email: "",
        persona_contacto: "",
        puesto_contacto: "",
        horario_atencion: "",
        metodo_pago: "",
        moneda: "",
        plazo_pago: null,
        categorias_producto: "",
        tiempo_entrega: null,
        zona_cobertura: "",
        calidad_proveedor: "",
        estado: "Activo",
      };
    },
  },
  created() {
    this.fetchProveedores();
  },
};
</script>

<style>
.contenedor {
  padding: 20px;
}

.formulario-columnas {
  display: flex;
  justify-content: space-between;
}

textarea#direccion {
  width: 66%;
}

textarea#categorias_producto {
  width: 66%;
}

textarea#zona_cobertura {
  width: 66%;
}

textarea#notas {
  width: 66%;
}

textarea {
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


.columna {
  width: 48%;
}

.form-group {
  margin-bottom: 15px;
}

.form-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.tabla {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.tabla th,
.tabla td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.tabla th {
  background-color: #f4f4f4;
}
</style>