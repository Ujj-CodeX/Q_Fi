<template>
    <div class="container mt-4">
        <h3 class="text-center">Quiz Name : {{ quizName }}</h3>

        <div class="quiz-settings">
            

            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                    Choose Duration
                </button>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" @click="setOption('duration', '2 minutes')">2 minutes</a></li>
                    <li><a class="dropdown-item" @click="setOption('duration', '5 minutes')">5 minutes</a></li>
                    <li><a class="dropdown-item" @click="setOption('duration', '10 minutes')">10 minutes</a></li>
                </ul>
            </div>

            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                    Choose No. of Questions
                </button>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" @click="setOption('questions', '2')">2</a></li>
                    <li><a class="dropdown-item" @click="setOption('questions', '5')">5</a></li>
                    <li><a class="dropdown-item" @click="setOption('questions', '10')">10</a></li>
                </ul>
            </div>
        </div>

        <div class="start-quiz-btn">
            <button class="btn btn-success" @click="startQuiz">Start Quiz</button>
        </div>

        <div class="selected-quiz">
            Selected Quiz: {{ quizSettings.difficulty }}, {{ quizSettings.duration }}, {{ quizSettings.questions }} questions
        </div>

        <div class="quiz-image">
            <img src="@/assets/6.jpg" style="height: 40%; width: 40%;" alt="Quiz Illustration">
        </div>
    </div>
</template>

<script>
import { jwtDecode } from 'jwt-decode';

export default {
    data() {
        return {
            userID: '',
            quizName: this.$route.params.quizName || "Quiz",
            quizSettings: {
                duration: "Not Selected",
                questions: "Not Selected"
            }
        };
    },
    created() {
    const token = localStorage.getItem('token');
    if (token) {
      const decoded = jwtDecode(token);
      this.userID = decoded.user_id;  // Extract securely
    } else {
      console.error('No token found!');
    }
  },
    methods: {
        setOption(type, value) {
            this.quizSettings[type] = value;
        },
        startQuiz() {
            const { duration, questions } = this.quizSettings;

            if (duration === "Not Selected" || questions === "Not Selected") {
                alert('Please select both duration and number of questions before starting the quiz.');
                return;
            }

            this.$router.push({
                path: '/test_page',
                query: {
                    quizName: this.quizName,
                    duration,
                    questions
                }
            });
        }
    }
};
</script>


<style scoped>
.quiz-settings {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
}

.purple-bg {
    background-color: #A63DE7;
    color: white;
    border-radius: 8px;
    padding: 10px;
    text-align: center;
}

.start-quiz-btn {
    margin-top: 20px;
    display: flex;
    justify-content: center;
}

.selected-quiz {
    margin-top: 20px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
}
</style>
