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
                <li><router-link class="dropdown-item" to="/admin-dashboard">Admin Dashboard</router-link></li>
  
  <li><router-link class="dropdown-item" to="/quiz-management">Quiz Management</router-link></li>
  <li><router-link class="dropdown-item" to="/admin-summary">User Summary</router-link></li>
  <li><router-link class="dropdown-item" to="/admin-login">Logout</router-link></li>
</ul>

          </div>
        </div>
      </nav>
  
      <div class="page-wrapper">
  <div class="quiz-management">

    <!-- Card 1: Question Display -->
    <div class="card">
      <h3>Question Display</h3>
      
      <div class="dropdown-container">
        <select v-model="selectedCourse" @change="fetchSubjects">
          <option value="" disabled>Select Course</option>
          <option v-for="course in courses" :key="course.id" :value="course.id">{{ course.name }}</option>
        </select>

        <select v-model="selectedSubject" @change="fetchChapters">
          <option value="" disabled>Select Subject</option>
          <option v-for="subject in subjects" :key="subject.id" :value="subject.id">{{ subject.name }}</option>
        </select>

        <select v-model="selectedChapter" @change="fetchQuestions">
          <option value="" disabled>Select Chapter</option>
          <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">{{ chapter.name }}</option>
        </select>
      </div>

      <div v-for="question in questions" :key="question.id" class="question-card">
  <h4>{{ question.text }}</h4>
  <ul>
  <li v-for="option in question.options" :key="option.id">
    <span :class="{'text-success font-weight-bold': option.text === question.correctAnswer}">
      {{ option.text }} <span v-if="option.text === question.correctAnswer">(✔️ Correct)</span>
    </span>
  </li>
</ul>

  <button @click="deleteQuestion(question.id)" class="btn btn-danger btn-sm">Delete</button>
</div>
    </div>
    <!-- Card 2: Question Management -->
    <div class="card">
      <h3>Question Management</h3>
      <div class="add-question">
        <input v-model="newQuestion" placeholder="Enter new question" />
        <div v-for="(option, index) in newOptions" :key="index">
          <input v-model="newOptions[index]" placeholder="Enter option" />
        </div>
        <input v-model="correctAnswer" placeholder="Enter correct answer" />
        <button @click="addOption">+ Add Option</button>
        <button @click="submitQuestion">Submit</button>
      </div>
    </div>
  </div>
</div>

  
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        courses: [],
        subjects: [],
        chapters: [],
        questions: [],
        selectedCourse: '',
        selectedSubject: '',
        selectedChapter: '',
        newQuestion: '',
        newOptions: ['', '', '', ''],
        correctAnswer: ''
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
    async fetchSubjects() {
        try {
            const response = await axios.get(`http://localhost:5000/subjects/${this.selectedCourse}`);
            this.subjects = response.data;
        } catch (error) {
            console.error('Error fetching subjects:', error);
        }
    },
    async fetchChapters() {
        try {
            const response = await axios.get(`http://localhost:5000/chapters/${this.selectedSubject}`);
            this.chapters = response.data;
        } catch (error) {
            console.error('Error fetching chapters:', error);
        }
    },
    async fetchQuestions() {
        try {
            const response = await axios.get(`http://localhost:5000/api/get_questions/${this.selectedChapter}`);
            console.log('Fetched Questions:', response.data); // ✅ Log to verify data structure
            this.questions = Array.isArray(response.data) ? response.data : [];
        } catch (error) {
            console.error('Error fetching questions:', error);
            alert('Failed to fetch questions. Please try again.');
        }
    },
    async submitQuestion() {
        try {
            await axios.post('http://localhost:5000/api/questions', {
                question: this.newQuestion,
                options: this.newOptions,
                correctAnswer: this.correctAnswer,
                chapter: this.selectedChapter
            });
            alert('Question added successfully!');
            this.newQuestion = '';
            this.newOptions = ['', '', '', ''];
            this.correctAnswer = '';
        } catch (error) {
            console.error('Error adding question:', error);
            alert('Failed to add question. Please try again.');
        }
    },
    async editQuestion(questionId) {
        try {
            await axios.put(`http://localhost:5000/api/edit_question/${questionId}`, {
                question: this.newQuestion,
                options: this.newOptions,
                correctAnswer: this.correctAnswer
            });
            alert('Question updated successfully!');
            this.fetchQuestions();
        } catch (error) {
            console.error('Error editing question:', error);
            alert('Failed to edit question. Please try again.');
        }
    },
    async deleteQuestion(questionId) {
        if (confirm('Are you sure you want to delete this question?')) {
            try {
                await axios.delete(`http://localhost:5000/api/delete_question/${questionId}`);
                alert('Question deleted successfully!');
                this.fetchQuestions();
            } catch (error) {
                console.error('Error deleting question:', error);
                alert('Failed to delete question. Please try again.');
            }
        }
    }
},
mounted() {
    this.fetchCourses();
}
  };
  </script>
  
  <style scoped>
  .page-wrapper {
    background-color:  #3E5966; /* Light grey background */
  min-height: 100vh;         /* Full page height */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
  .quiz-management {
    display: flex;
    gap: 20px;
    margin: 20px;
    
  }
  .card {
    border: 1px solid #ccc;
    padding: 20px;
    width: auto;
    background-color: #f9f9f9;
  }
  .dropdown-container select, .add-question input {
    margin: 10px 0;
    padding: 5px;
    width: 100%;
  }
  .questions-container {
    margin-top: 20px;
  }
  .add-question button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
    margin-top: 10px;
  }
  </style>
  