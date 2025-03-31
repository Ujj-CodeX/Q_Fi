<template>
    <nav class="navbar navbar-expand-lg" style="background-color: #f5f5f5;">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand">
          <img src="@/assets/logo.png" alt="Q-Fi Logo" width="110" height="60" class="d-inline-block align-text-top" style="margin-left: 20px;">
        </router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            
          </ul>

          
        </div>
      </div>
    </nav>

    <div class="signup-wrapper">
    <div class="signup-container">
      <h2 class="signup-heading">Signup as New User</h2>
  
      <form @submit.prevent="handleSignup">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="formData.username" type="text" class="form-control" id="username" required>
        </div>
  
        <div class="mb-3">
          <label for="email" class="form-label">Email Address</label>
          <input v-model="formData.email" type="email" class="form-control" id="email" required>
        </div>
  
        <div class="mb-3">
          <label for="birthdate" class="form-label">Date of Birth</label>
          <input v-model="formData.birthdate" type="date" class="form-control" id="birthdate" required>
        </div>
  
        <div class="mb-3">
          <label for="gender" class="form-label">Gender</label>
          <select v-model="formData.gender" class="form-select" id="gender" required>
            <option value="" disabled selected>Select Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>
  
        <div class="mb-3">
          <label for="course" class="form-label">Course</label>
          <select v-model="formData.course" class="form-select" id="course" required>
            <option value="" disabled selected>Select Course</option>
            <option v-for="course in courses" :key="course.id" :value="course.name">
              {{ course.name }}
            </option>
          </select>
        </div>
  
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="formData.password" type="password" class="form-control" id="password" required>
        </div>
  
        <div class="mb-3">
          <label for="confirm_password" class="form-label">Confirm Password</label>
          <input v-model="formData.confirm_password" type="password" class="form-control" id="confirm_password" required>
        </div>
  
        <button type="submit" class="btn btn-primary w-100">Signup</button>
      </form>
  
      <p class="text-center mt-3">
        Already have an account? <router-link to="/">Login here</router-link>
      </p>
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
          email: '',
          birthdate: '',
          gender: '',
          course: '',
          password: '',
          confirm_password: ''
        },
        courses: [] // To store available courses
      };
    },
    methods: {
        async fetchCourses() {
        try {
          const response = await axios.get('http://localhost:5000/courses');
          this.courses = response.data;
        } catch (error) {
          console.error('Error fetching courses:', error);
        }
      },
      async handleSignup() {
        if (this.formData.password !== this.formData.confirm_password) {
          alert('Passwords do not match!');
          return;
        }
  
        try {
          const payload = {
            username: this.formData.username,
            email: this.formData.email,
            dob: this.formData.birthdate,
            gender: this.formData.gender,
            course: this.formData.course,
            password: this.formData.password
          };
  
          const response = await axios.post('http://localhost:5000/signup', payload);
  
          if (response.data.success) {
            alert(response.data.message || 'Signup successful!');
            this.$router.push('/');
          } else {
            alert(response.data.error || 'Signup failed. Please try again.');
          }
        } catch (error) {
          console.error('Signup error:', error);
          alert('Error during signup. Please try again.');
        }
      }
    },
    mounted() {
      this.fetchCourses(); // Load courses when component is mounted
    }
  };
  </script>
  
  <style scoped>
  .signup-wrapper {
    height: 100%;
    background-color:  #3E5966;
    background-size: cover;
    display: flex;
    justify-content: center;
    align-items: center;
}

.signup-container {
    background-color: rgba(255, 255, 255, 0.9);  /* Slight white overlay for better readability */
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
    margin-top: 5%;
    margin-bottom: 40px;
}
.signup-heading {
    text-align: center;
    margin-bottom: 20px;
    font-weight: bold;
}

  </style>
  