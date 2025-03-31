<template>
  <div>
    <!-- Navbar -->
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
    
    <li><router-link class="dropdown-item" to="/leaderboard">Leaderboard</router-link></li>
    <li><router-link class="dropdown-item" to="/">Logout</router-link></li>
</ul>

        </div>
      </div>
    </nav>

    <!-- Sidebar for Subjects -->
<div class="sidebar-card">
  <h5 style="color: white;">Subjects</h5>
  <hr>
  <div 
    v-for="(subject, key) in subjects" 
    :key="key" 
    class="subject-item" 
    @click="fetchChapters(subject.subject_id)">
    <span>{{ subject.name }}</span>
    <span>&gt;</span>
  </div>
</div>
</div>

<div class="quiz-container">
  <h5 style="color: black;">Available Quizzes</h5>
  <hr>
  <div v-for="(chapter, index) in chapters"
       :key="index"
       class="quiz-item"
       @click="navigateToQuiz(chapter.name)">
      
    <span>{{ chapter.name }}</span>
  </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: "QuizUser",
  data() {
    return {
      subjects: [],   
      chapters: [],   
      selectedSubjectId: null  // Track selected subject ID for dynamic loading
    };
  },
  mounted() {
    this.fetchSubjects();
  },
  methods: {
    async fetchSubjects() {
  try {
    const token = localStorage.getItem('token');  // Retrieve token from storage

    const response = await axios.get('http://localhost:5000/subjects1', {
      headers: {
        'Authorization': `Bearer ${token}`  // Include token in the request
      }
    });

    this.subjects = response.data;
  } catch (error) {
    console.error('Error fetching subjects:', error);
  }
},
async fetchChapters(subjectId) {
    this.selectedSubjectId = subjectId;
    const token = localStorage.getItem('token');

    // Token check with improved feedback
    if (!token) {
        alert('Session expired or not logged in. Redirecting to login page...');
        this.$router.push('/');
        return;
    }

    try {
        const response = await axios.get(`http://localhost:5000/chapters1/${subjectId}`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        // Check if response data is empty
        if (!response.data || response.data.length === 0) {
            alert('No chapters available for the selected subject.');
            this.chapters = [];
            return;
        }

        this.chapters = response.data;
    } catch (error) {
        // Improved error feedback for various scenarios
        if (error.response) {
            if (error.response.status === 401) {
                alert('Unauthorized access. Please log in again.');
                this.$router.push('/');
            } else if (error.response.status === 404) {
                alert('No chapters found for the selected subject.');
                this.chapters = [];
            } else {
                alert(`Error: ${error.response.status} - ${error.response.data.message || 'Unknown error occurred'}`);
            }
        } else if (error.request) {
            alert('Server is not responding. Please try again later.');
        } else {
            console.error('Error fetching chapters:', error);
            alert('An unexpected error occurred. Please try again.');
        }
    }
},
navigateToQuiz(chapterName) {
            const token = localStorage.getItem('token');

            if (!token) {
                alert('Session expired or invalid token. Please log in again.');
                this.$router.push('/');
                return;
            }

            this.$router.push({
            name: 'QuizPreferences',
            params: { quizName: chapterName }
        });
        }
    }
}


</script>

<style scoped>
.sidebar-card {
  width: 250px;
  border-radius: 15px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  background-color: #A63DE7;
  padding: 15px;
  position: fixed;
  top: 80px;
  left: 20px;
  height: 80vh;
  overflow-y: auto;
  margin-top: 50px;
}

.subject-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
  color: white;
}

.subject-item:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.quiz-container {
  margin-left: 300px;
  padding: 20px;
}

.quiz-item {
  background: #f8f9fa;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: background 0.3s;
}

.quiz-item:hover {
  background: #e0e0e0;
}
</style>