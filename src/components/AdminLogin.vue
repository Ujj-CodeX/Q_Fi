<template>
    
  
    <div class="admin-login-wrapper">
      <div class="admin-login-container">
        <h2 class="admin-login-heading">Admin Login</h2>
  
        <form @submit.prevent="handleAdminLogin">
          <div class="mb-3">
            <label for="username" class="form-label">Admin Username</label>
            <input v-model="adminData.username" type="text" class="form-control" id="username" required>
          </div>
  
          <div class="mb-3">
            <label for="password" class="form-label">Admin Password</label>
            <input v-model="adminData.password" type="password" class="form-control" id="password" required>
          </div>
  
          <button type="submit" class="btn btn-primary w-100">Login as Admin</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        adminData: {
          username: '',
          password: ''
        }
      };
    },
    methods: {
  async handleAdminLogin() {
    try {
      const response = await axios.post('http://localhost:5000/admin-login', this.adminData);

      if (response.data.success) {
        alert('Admin login successful!');
        this.$router.push('/admin-dashboard');  // Redirect via Vue Router
      } else {
        alert(response.data.error || 'Invalid admin credentials!');
      }
    } catch (error) {
      console.error('Admin login error:', error);
      alert('Error during admin login. Please try again.');
    }
  }
}

  };
  </script>
  
  <style scoped>
  .admin-login-wrapper {
    height: 100vh;
    background: url('@/assets/7.jpg') no-repeat center center/cover;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .admin-login-container {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    width: 100%;
    max-width: 350px;
  }
  
  .admin-login-heading {
    text-align: center;
    margin-bottom: 20px;
    font-weight: bold;
    color: #343a40;
  }
  
  .form-label {
    font-weight: 500;
  }
  
  button {
    background-color: #007bff;
    border: none;
  }
  </style>
  