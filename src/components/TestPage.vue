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
    <div>
      <div v-if="isLoading">Loading questions...</div>
      <div v-else>
        <div class="timer">Time Left: {{ formatTime(remainingTime) }}</div>

      
        <div v-if="currentQuestionIndex < questionsCopy.length" class="question-card">
    <p>{{ questionsCopy[currentQuestionIndex].text }}</p>

    <div v-for="(option, i) in questionsCopy[currentQuestionIndex].options" :key="i">
    <input 
        type="radio" 
        :name="'question-' + questionsCopy[currentQuestionIndex].id" 
        :value="typeof option === 'object' ? option.text : option"
        :checked="userAnswers[questionsCopy[currentQuestionIndex].id] === (typeof option === 'object' ? option.text : option)"
        @change="handleSelection(questionsCopy[currentQuestionIndex].id, typeof option === 'object' ? option.text : option)"
    />
    {{ typeof option === 'object' ? option.text : option }}
</div>
</div>

<div v-else>
    <p>All questions completed!</p>
</div>

  
        <div class="nav-buttons">
          <button @click="prevQuestion" :disabled="currentQuestionIndex === 0">Previous</button>
          <button @click="currentQuestionIndex < questionsCopy.length - 1 ? nextQuestion() : submitQuiz()">
  {{ currentQuestionIndex < questionsCopy.length - 1 ? 'Next' : 'Submit' }}
</button>

        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
   
  
  export default {
    props: {
        quizName: {
            type: String,
            required: true
        },
        duration: {
            type: String,
            default: '5 minutes' // Fallback if not provided
        },
        questions: {
            type: String,
            required: true
        }
    },
    data() {
      return {
        questionsCopy: JSON.parse(this.questions),
        userAnswers: {},
        currentQuestionIndex: 0,
        isLoading: false,
        remainingTime: parseInt(this.duration) * 60 || 300, // Fallback 5 mins
        timer: null
      };
    },
    created() {
    this.fetchQuestions();   
    this.remainingTime = (parseInt(this.$route.query.duration) || 5) * 60;  // Default 5 mins
    this.startTimer();       
},


  beforeUnmount() {
    clearInterval(this.timer);  // Clear timer when leaving the page
  },
  
    
  
    methods: {
      async fetchQuestions() {
        this.isLoading = true;
    try {
        const response = await axios.get(`http://localhost:5000/get-questions`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
            params: {
                quizName: this.quizName,  // Use prop value
                courseName: this.$route.query.courseName,
                userID: this.userID,
                questions: this.questions
            }
        });

        console.log("API Response:", response.data);
        this.questionsCopy = response.data || [];
        this.userAnswers = Array(this.questionsCopy.length).fill(null);
    } catch (error) {
        console.error("Error fetching questions:", error);
        alert("Failed to load questions. Please try again.");
    } finally {
        this.isLoading = false;
    }
},
  
      nextQuestion() {
        if (this.currentQuestionIndex < this.questionsCopy.length - 1) {
          this.currentQuestionIndex++;
        } else {
          localStorage.setItem('userAnswers', JSON.stringify(this.userAnswers));
          alert("Answers saved successfully!");
        }
      },
  
      prevQuestion() {
        if (this.currentQuestionIndex > 0) {
          this.currentQuestionIndex--;
        }
      },
      startTimer() {
      this.timer = setInterval(() => {
        if (this.remainingTime > 0) {
          this.remainingTime--;
        } else {
          clearInterval(this.timer);
          this.submitQuiz();
          this.$router.push('/times-up');

        }
      }, 1000);  // Decrease every second
    },

    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
    },
    handleSelection(questionId, selectedOption) {
    this.userAnswers = { ...this.userAnswers, [String(questionId)]: selectedOption };
    console.log(` Question ID: ${questionId}, Selected Option: ${selectedOption}`);



},
async submitQuiz() {
    const userAnswersObject = {};

    this.questionsCopy.forEach((question) => {
        const questionId = String(question.id);  // Ensure consistent key type
        console.log(`Mapping ID: ${question.id} -> Answer: ${this.userAnswers[questionId] || 'N/A'}`);

        if (this.userAnswers[questionId]) {
            userAnswersObject[questionId] = this.userAnswers[questionId];
        } else {
            console.warn(`No answer provided for question ID: ${question.id}`);
            userAnswersObject[questionId] = null;
        }
    });

    const payload = {
        quizName: this.quizName,
        userAnswers: this.userAnswers,
        duration: this.remainingTime
    };

    console.log("Payload being sent:", payload);

    try {
        const response = await axios.post('http://localhost:5000/submit-quiz', payload, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });

        if (response.data.message) {
            alert(`Quiz submitted successfully! Your score is: ${response.data.score}`);
            this.$router.push('/Leaderboard');  
        } else {
            alert('Submission failed. Please try again.');
        }

    } catch (error) {
        console.error("Error submitting quiz:", error);
        alert("Failed to submit quiz. Please try again.");
    }
}



  }
};

  
  </script>
  
  <style scoped>
  .question-card {
    border: 1px solid #ddd;
    width: 50%;
    margin-left: 25%;
    padding: 15px;
    margin-bottom: 15px;
    margin-top: 20px;
    border-radius: 8px;
    background-color: #f9f9f9;
  }
  
  .nav-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
    margin-left: 25%;
    margin-right: 25%;
  }
  
  button {
    background-color: #9c27b0;
    color: #fff;
    border: none;
    padding: 8px 20px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  .timer {
  font-size: 1.5rem;
  font-weight: bold;
  color: #d9534f;  /* Red color for urgency */
  margin-bottom: 20px;
}
  </style>
  
