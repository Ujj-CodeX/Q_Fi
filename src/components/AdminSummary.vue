<template>
  <nav class="navbar navbar-expand-lg" style="background-color: #f5f5f5; padding: 10px;">
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
  
  <li><router-link class="dropdown-item" to="/quiz-management">Quiz Management</router-link></li>
  <li><router-link class="dropdown-item" to="/admin-login">Logout</router-link></li>
</ul>

          </div>
        </div>
      </nav>
      <div class="ujju">
  <div class="admin-summary">
    <!-- Display Pie Chart -->
    <div v-if="pieChartData.labels.length" class="chart-container">
      <Pie :data="pieChartData" :options="chartOptions" />
    </div>
    <div v-else>
      <p>No data available for the chart.</p>
    </div>

    <!-- Display Quiz Summary Table -->
    <div v-if="quizSummary.length" class="table-container">
      <table class="quiz-summary-table">
        <thead>
          <tr>
            <th>Quiz Name</th>
            <th>User Attempts</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(quiz, index) in quizSummary" :key="index">
            <td>{{ quiz.quiz_name }}</td>
            <td>{{ quiz.user_attempts }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>No quiz summary available.</p>
    </div>
  </div>
  </div>

  
</template>

<script>
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale);

export default {
  name: "AdminSummary",
  components: {
    Pie,
  },
  data() {
    return {
      quizSummary: [],
      pieChartData: {
        labels: [],
        datasets: [
          {
            data: [],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4CAF50', '#E91E63'],
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
          },
        },
      },
    };
  },
  methods: {
    async fetchQuizSummary() {
      try {
        const response = await fetch('http://localhost:5000/quiz-summary');
        const data = await response.json();

        this.quizSummary = data;

        if (data.length) {
    this.pieChartData.labels = data.map(item => item.quiz_name);
    this.pieChartData.datasets[0].data = data.map(item => item.user_attempts);
}

      } catch (error) {
        console.error('Error fetching quiz summary:', error);
      }
    },
  },
  
  
  mounted() {
    this.fetchQuizSummary();
    
  },
};
</script>

<style scoped>


.admin-summary {
  margin: 0 auto;
  padding: 20px;
  max-width: 800px;
  text-align: center;
}

.chart-container {
  height: 350px; /* Increased height for better visibility */
  width: 100%;
  margin-bottom: 20px;
  border: 2px solid #ddd;
  border-radius: 12px;
  background-color: #f9f9f9;
  padding: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.table-container {
  max-height: 300px;
  overflow-y: auto;
  border: 2px solid #ddd;
  border-radius: 8px;
}

.quiz-summary-table {
  width: 100%;
  border-collapse: collapse;
}

.quiz-summary-table th,
.quiz-summary-table td {
  padding: 10px;
  border: 1px solid #ccc;
  text-align: left;
}

.quiz-summary-table th {
  background-color: #4CAF50;
  color: #fff;
}

.quiz-summary-table tr:nth-child(even) {
  background-color: #f2f2f2;
}
</style>
