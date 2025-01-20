<template>
  <div class="welcome-header">
    <h1>Bienvenido a la Clínica Rehabilita tu alma</h1>
  </div>
  <div class="login-container">
    <div class="login-card">
      <h2>Iniciar Sesión</h2>
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" placeholder="Ingresa tu email" required />
        </div>
        <div class="input-group">
          <label for="password">Contraseña:</label>
          <input type="password" id="password" v-model="password" placeholder="Ingresa tu contraseña" required />
        </div>
        <div class="button-container">
          <button type="submit" class="btn-submit">Entrar</button>
        </div>
      </form>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post("http://localhost:8000/api/login/", {
          email: this.email,
          password: this.password,
        });
        this.$cookies.set("auth_token", response.data.token, "1d");
        this.$router.push("/dashboard");
      } catch (error) {
        this.errorMessage = "Correo o contraseña incorrectos. Intenta nuevamente.";
      }
    },
  },
};
</script>

<style scoped>
.welcome-header {
  position: absolute;
  top: 5cm;
  width: 100%;
  text-align: center;
}

.welcome-header h1 {
  font-size: 32px;
  font-weight: bold;
  color: #2c3e50;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #dbe7e9;
}

.login-card {
  background-color: #ffffff;
  margin-top: -200px;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
  opacity: 85%;
}

.input-group {
  margin-bottom: 20px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
}

.input-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.button-container {
  display: flex;
  justify-content: center;
}

.btn-submit {
  padding: 10px 20px;
  background-color: #007bff;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.btn-submit:hover {
  background-color: #0056b3;
}

.error-message {
  color: #e74c3c;
  margin-top: 10px;
}
</style>
