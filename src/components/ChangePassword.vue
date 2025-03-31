<template>
    <div class="change-password-container">
      <div class="card">
        <h2 class="card-heading">Change Password</h2>
  
        <form @submit.prevent="handleChangePassword">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input v-model="formData.username" type="text" class="form-control" id="username" required>
          </div>
  
          <div class="mb-3">
            <label for="new_password" class="form-label">New Password</label>
            <input v-model="formData.new_password" type="password" class="form-control" id="new_password" required>
          </div>
  
          <div class="mb-3">
            <label for="confirm_password" class="form-label">Confirm New Password</label>
            <input v-model="formData.confirm_password" type="password" class="form-control" id="confirm_password" required>
          </div>
  
          <button type="submit" class="btn btn-primary w-100">Change Password</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        formData: {
          username: '',
          new_password: '',
          confirm_password: ''
        }
      };
    },
    methods: {
      async handleChangePassword() {
        if (this.formData.new_password !== this.formData.confirm_password) {
          alert('Passwords do not match!');
          return;
        }
  
        try {
          const payload = {
            username: this.formData.username,
            new_password: this.formData.new_password
          };
  
          const response = await axios.post('http://localhost:5000/change-password', payload);
  
          if (response.data.success) {
            alert('Password changed successfully!');
            this.$router.push('/');
          } else {
            alert(response.data.error || 'Failed to change password.');
          }
        } catch (error) {
          console.error('Change password error:', error);
          alert('Error changing password. Please try again.');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .change-password-container {
    background-image: url('@/assets/7.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;
  }
  
  .card {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    width: 100%;
    max-width: 400px;
  }
  
  .card-heading {
    text-align: center;
    margin-bottom: 20px;
    font-weight: bold;
  }
  </style>
  