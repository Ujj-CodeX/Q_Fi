<template>
      <!-- Background for entire page -->
      <nav class="navbar navbar-expand-lg" style="background-color: rgba(245, 245, 245, 0.9); padding: 10px;">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">
            <img src="@/assets/logo.png" alt="Q-Fi Logo" width="110" height="60">
          </a>
          <div class="dropdown ms-auto">
            <img 
              src="@/assets/5.jpg" 
              alt="Profile" 
              class="rounded-circle" 
              width="40" 
              height="40" 
              data-bs-toggle="dropdown" 
              style="cursor: pointer;">
            <ul class="dropdown-menu dropdown-menu-end">
              
              <li><router-link class="dropdown-item" to="/leaderboard">Leaderboard</router-link></li>
              
              
              <li><router-link class="dropdown-item" to="/">Logout</router-link></li>
            </ul>
          </div>
        </div>
      </nav>
      <div class="background-container">
  
      <div class="card">
        <h3>Leaderboard</h3>
        <p>Please Choose Your Attempted Quiz</p>
        <select v-model="selectedQuiz" @change="fetchQuizDetails">
  <option value="" disabled>Select a Quiz</option>
  <option v-for="quiz in quizzes" :key="quiz.id" :value="quiz.id">
    {{ quiz.quiz_name }}
  </option>
</select>
  
        <div v-if="quizDetails">
          <p><b>Score:</b> {{ quizDetails.score }}</p>
          <p><b>Time Duration:</b> {{ quizDetails.duration }}</p>
          <p><b>Questions Attempted:</b> {{ quizDetails.questions_attempted }}</p>
        </div>

        <button class="btn btn-primary mt-3 " style="margin-top: 50%;" @click="downloadReport">
          Download Report
        </button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return { 
        quizzes: [],
        selectedQuiz: null,
        quizDetails: null
      };
    },
    mounted() {
      fetch('http://localhost:5000/user-quizzes', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
})
  .then(res => res.json())
  .then(data => {
    console.log("📋 Quiz Data:", data);
    
    // ✅ Store both id and quiz_name
    this.quizzes = data.user_quizzes.map(quiz => ({
      id: quiz.id, 
      quiz_name: quiz.quiz_name 
    }));
  })
  .catch(err => console.error('❌ Error:', err));
    },
    methods: {
      fetchQuizDetails() {
  console.log("🟣 Selected Quiz ID:", this.selectedQuiz);

  if (!this.selectedQuiz) {
    alert("Please select a quiz first.");
    return;
  }

  fetch(`http://localhost:5000/quiz-details/${this.selectedQuiz}`, {  // ✅ Now using quiz ID
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  })
    .then(res => {
      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }
      return res.json();
    })
    .then(data => {
      console.log("📋 Quiz Details:", data);
      this.quizDetails = data;
    })
    .catch(err => {
      console.error('❌ Fetch Error:', err);
      alert("Failed to load quiz details. Please try again.");
    });
},

      downloadReport() {
      fetch('http://localhost:5000/download-report',{headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
        .then(response => response.blob()) // Get CSV file as blob
        .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'report.csv'); // Set filename
          document.body.appendChild(link);
          link.click();
          link.remove();
        })
        .catch(err => console.error('❌ Error downloading report:', err));
    }
    }
  };
  </script>
  
  <style scoped>
  .background-container {
    background-color: #3E5966; /* Background image */
    background-size: cover;
    background-position: center;
    height: 100vh; /* Full viewport height */
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 20px;
  }
  
  .navbar {
    width: 100%;
    background-color: rgba(245, 245, 245, 0.9); /* Slight transparency for blending */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Soft shadow effect */
    margin-top: 0px;
  }
  
  .card {
    background-color: white;
    color: black;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 50%;
    margin-top: 20px;
    margin-bottom: 10%;

  }
  </style>
  