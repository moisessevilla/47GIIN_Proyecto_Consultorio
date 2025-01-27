<template>
  <div class="contenido">
    <h1>Gestión de Usuarios</h1>

    <!-- Formulario para crear o editar un usuario -->
    <div class="formulario">
      <h2>{{ isEditing ? "Editar Usuario" : "Nuevo Usuario" }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="nombre">Nombre:</label>
          <input type="text" v-model="form.nombre" id="nombre" placeholder="Ingrese el nombre" required />
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" v-model="form.email" id="email" placeholder="Ingrese el email" required />
        </div>
        <div class="form-group">
          <label for="contrasena">Contraseña:*</label>
          <input id="contrasena" v-model="form.contrasena" minlength="6" maxlenght="100"
            placeholder="Ingrese un contraseña 6 cáracteres o más" :type="showPassword ? 'text' : 'password'"
            :required="!form.id_paciente" />
        </div>
        <div class="form-group">
          <label for="rol">Rol:</label>
          <select v-model="form.rol" id="rol" required>
            <option value="admin">Admin</option>
            <option value="medico">Médico</option>
            <option value="paciente">Paciente</option>
            <option value="recepcionista">Recepcionista</option>
            <option value="usuario">Usuario</option>
          </select>
        </div>
        <div class="form-group">
          <label for="estado">Estado:</label>
          <select v-model="form.estado" id="estado" required>
            <option value="activo">Activo</option>
            <option value="inactivo">Inactivo</option>
          </select>
        </div>
        <button type="submit">{{ isEditing ? "Actualizar" : "Registrar" }}</button>
        <button type="button" @click="resetForm">Cancelar</button>
      </form>
    </div>

    <!-- Contenedor para mostrar usuarios -->
    <div class="tabla-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="usuario in usuarios" :key="usuario.id_usuario">
            <td>{{ usuario.id_usuario }}</td>
            <td>{{ usuario.nombre }}</td>
            <td>{{ usuario.email }}</td>
            <td>{{ usuario.rol }}</td>
            <td>{{ usuario.estado === true ? 'Inactivo' : 'Activo' }}</td>
            <td>
              <button @click="editUsuario(usuario)">Editar</button>
              <button @click="deleteUsuario(usuario.id_usuario)">Eliminar</button>
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
      usuarios: [],
      form: {
        id_usuario: null,
        nombre: "",
        apellido: "",
        email: "",
        rol: "medico",
        estado: "activo",
      },
      isEditing: false,
    };
  },
  methods: {
    async fetchUsuarios() {
      try {
        const response = await axios.get("/usuarios/");
        this.usuarios = response.data;
      } catch (error) {
        console.error("Error al obtener los usuarios:", error);
      }
    },
    handleSubmit() {
      if (this.isEditing) {
        this.updateUsuario();
      } else {
        this.createUsuario();
      }
    },
    async createUsuario() {
      try {
        await axios.post("/usuarios/", this.form);
        this.fetchUsuarios();
        this.resetForm();
      } catch (error) {
        console.error("Error al crear el usuario:", error);
      }
    },
    async updateUsuario() {
      try {
        await axios.put(`/usuarios/${this.form.id_usuario}/`, this.form);
        this.fetchUsuarios();
        this.resetForm();
      } catch (error) {
        console.error("Error al actualizar el usuario:", error);
      }
    },
    async deleteUsuario(id) {
      try {
        await axios.delete(`/usuarios/${id}/`);
        this.fetchUsuarios();
      } catch (error) {
        console.error("Error al eliminar el usuario:", error);
      }
    },
    editUsuario(usuario) {
      this.form = { ...usuario };
      this.isEditing = true;
    },
    resetForm() {
      this.form = {
        id_usuario: null,
        nombre: "",
        apellido: "",
        email: "",
        rol: "medico",
        estado: "activo",
      };
      this.isEditing = false;
    },
  },
  mounted() {
    this.fetchUsuarios();
  },
};
</script>