<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg" style="background-color: #f5f5f5;">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand">
          <img src="@/assets/logo.png" alt="Q-Fi Logo" width="110" height="60" 
               class="d-inline-block align-text-top" style="margin-left: 20px;">
        </router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" 
                aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0"></ul>

          <div class="d-flex" style="margin-right: 20px;">
            <router-link to="/signup" class="btn btn-primary">Sign Up</router-link>
          </div>
        </div>
      </div>
    </nav>

    <div class="container d-flex justify-content-center align-items-center">
      <div class="card p-4 shadow-lg" style="width: 100%; max-width: 450px;">
        <h3 class="text-center mb-4">Login</h3>

        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input v-model="username" type="text" id="username" class="form-control" required>
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input v-model="password" type="password" id="password" class="form-control" required>
          </div>

          <button 
            type="submit" 
            class="btn btn-primary w-100"
            :disabled="loading"
          >
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>

          <p v-if="errorMessage" class="text-danger text-center mt-2">{{ errorMessage }}</p>
        </form>

        <p class="text-center mt-3">Forgot Username or Password? 
          <router-link to="/change-password" class="text-primary">Click Here</router-link>
        </p>

        <p class="text-center mt-3">New Here? 
          <router-link to="/signup" class="text-primary">Register Now</router-link>
        </p>
        <p class="text-center mt-3">Admin? 
          <router-link to="/admin-login" class="text-primary">Login Here</router-link>
        </p>
      </div>

      <img src="@/assets/2.png" alt="Right Image" 
           class="img-fluid me-5" 
           style="max-width: 45%; height: auto; margin-right: auto; margin-left: auto;">
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HelloWorld',
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      loading: false
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.errorMessage = '';

      try {
        const response = await axios.post(
          'http://localhost:5000/login', 
          {
            username: this.username,
            password: this.password
          }, 
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );

        if (response.status === 200 && response.data.access_token) {
          localStorage.setItem('token', response.data.access_token);  // Store token for secure data access
          this.$router.push('/user');  // Redirect to the user page
        } else {
          this.errorMessage = 'Unexpected response from the server.';
        }
      } catch (error) {
        if (error.response) {
          this.errorMessage = error.response.data.error || 'Invalid credentials.';
        } else if (error.request) {
          this.errorMessage = 'No response from server. Please check your connection.';
        } else {
          this.errorMessage = 'Error occurred during request.';
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>


<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
