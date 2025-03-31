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
  <li><router-link class="dropdown-item" to="/admin-summary">User Summary</router-link></li>
  <li><router-link class="dropdown-item" to="/admin-login">Logout</router-link></li>
</ul>

          </div>
        </div>
      </nav>
  
    <div class="admin-dashboard">
      <!-- Course Card -->
      <div class="card">
        <h3>Courses</h3>
        <ul>
          <li v-for="course in courses" :key="course.id">
            {{ course.name }}
            <button @click="editCourse(course)">Edit</button>
            <button @click="deleteCourse(course.id)">Delete</button>
          </li>
        </ul>
        <button @click="showAddCourseForm = true">+ Course</button>
      </div>
  
      <!-- Add Course Form -->
      <div v-if="showAddCourseForm" class="form-card">
        <h4>Add New Course</h4>
        <input v-model="newCourseName" placeholder="Course Name" />
        <button @click="addCourse">Add Course</button>
        <button @click="showAddCourseForm = false">Cancel</button>
      </div>
  
      <!-- Subject Card -->
      <div class="card">
        <h3>Subjects</h3>
        <select v-model="selectedCourse">
          <option v-for="course in courses" :key="course.id" :value="course.id">{{ course.name }}</option>
        </select>
        <ul>
          <li v-for="subject in subjects" :key="subject.id">
            {{ subject.name }}
            <button @click="editSubject(subject)">Edit</button>
            <button @click="deleteSubject(subject.id)">Delete</button>
          </li>
        </ul>
        <button @click="showAddSubjectForm = true">+ Subject</button>
      </div>
  
      <!-- Add Subject Form -->
      <div v-if="showAddSubjectForm" class="form-card">
        <h4>Add New Subject</h4>
        <input v-model="newSubjectName" placeholder="Subject Name" />
        <button @click="addSubject">Add Subject</button>
        <button @click="showAddSubjectForm = false">Cancel</button>
      </div>
  
      <!-- Chapter Card -->
      <div class="card">
        <h3>Chapters</h3>
        <select v-model="selectedChapterCourse">
          <option v-for="course in courses" :key="course.id" :value="course.id">{{ course.name }}</option>
        </select>
        <select v-model="selectedSubject">
          <option v-for="subject in subjects" :key="subject.id" :value="subject.id">{{ subject.name }}</option>
        </select>
        <ul>
          <li v-for="chapter in chapters" :key="chapter.id">
            {{ chapter.name }}
            <button @click="editChapter(chapter)">Edit</button>
            <button @click="deleteChapter(chapter.id)">Delete</button>
          </li>
        </ul>
        <button @click="showAddChapterForm = true">+ Chapter</button>
      </div>
  
      <!-- Add Chapter Form -->
      <div v-if="showAddChapterForm" class="form-card">
        <h4>Add New Chapter</h4>
        <input v-model="newChapterName" placeholder="Chapter Name" />
        <button @click="addChapter">Add Chapter</button>
        <button @click="showAddChapterForm = false">Cancel</button>
      </div>

      <div>
    <button @click="sendReminders">Send Daily Reminders</button>
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
  
        newCourseName: '',
        newSubjectName: '',
        newChapterName: '',
  
        selectedCourse: null,
        selectedChapterCourse: null,
        selectedSubject: null,
  
        showAddCourseForm: false,
        showAddSubjectForm: false,
        showAddChapterForm: false
      };
    },
  
    mounted() {
      this.fetchCourses();
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
  
      async addCourse() {
        try {
          await axios.post('http://localhost:5000/add-course', { name: this.newCourseName });
          this.fetchCourses();
          this.showAddCourseForm = false;
          this.newCourseName = '';
        } catch (error) {
          console.error('Error adding course:', error);
        }
      },
  
      async deleteCourse(courseId) {
        try {
          await axios.delete(`http://localhost:5000/delete-course/${courseId}`);
          this.fetchCourses();
        } catch (error) {
          console.error('Error deleting course:', error);
        }
      },
      async deleteSubject(subjectId) {
    try {
        await axios.delete(`http://localhost:5000/delete-subject/${subjectId}`);
        this.subjects = this.subjects.filter(subject => subject.id !== subjectId);
    } catch (error) {
        console.error('Error deleting subject:', error);
    }
}
,
async deleteChapter(chapterId) {
    try {
        await axios.delete(`http://localhost:5000/delete-chapter/${chapterId}`);
        this.chapters = this.chapters.filter(chapter => chapter.id !== chapterId);
    } catch (error) {
        console.error('Error deleting chapter:', error);
    }
},
  
      async addSubject() {
        try {
          await axios.post('http://localhost:5000/add-subject', {
            name: this.newSubjectName,
            course_id: this.selectedCourse
          });
          this.showAddSubjectForm = false;
          this.fetchSubjects();
          this.newSubjectName = '';
        } catch (error) {
          console.error('Error adding subject:', error);
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
  
      async addChapter() {
        try {
          await axios.post('http://localhost:5000/add-chapter', {
            name: this.newChapterName,
            subject_id: this.selectedSubject
          });
          this.showAddChapterForm = false;
          this.fetchChapters();
          this.newChapterName = '';
        } catch (error) {
          console.error('Error adding chapter:', error);
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

      async sendReminders() {
      try {
        const response = await fetch('http://localhost:5000/send-reminders', {
          method: 'POST',
        });

        const data = await response.json();
        console.log(data.message);
        alert('Reminders sent!');
      } catch (error) {
        console.error('Error sending reminders:', error);
      }
      },
      async editCourse(course) {
    const updatedName = prompt('Enter new course name:', course.name);
    if (updatedName && updatedName.trim()) {
      try {
        await axios.put(`http://localhost:5000/edit-course/${course.id}`, { name: updatedName.trim() });
        this.fetchCourses();
      } catch (error) {
        console.error('Error editing course:', error);
      }
    }
  },

  async editSubject(subject) {
    const updatedName = prompt('Enter new subject name:', subject.name);
    if (updatedName && updatedName.trim()) {
      try {
        await axios.put(`http://localhost:5000/edit-subject/${subject.id}`, { name: updatedName.trim() });
        this.fetchSubjects();
      } catch (error) {
        console.error('Error editing subject:', error);
      }
    }
  },

  async editChapter(chapter) {
    const updatedName = prompt('Enter new chapter name:', chapter.name);
    if (updatedName && updatedName.trim()) {
      try {
        await axios.put(`http://localhost:5000/edit-chapter/${chapter.id}`, { name: updatedName.trim() });
        this.fetchChapters();
      } catch (error) {
        console.error('Error editing chapter:', error);
      }
    }
  }


    
    }
  };
  </script>
  <style>
  
  .admin-dashboard {
    display: flex;
    gap: 20px; /* Adds space between cards */
    flex-wrap: wrap; /* Ensures responsiveness for smaller screens */
  }
  
  .card {
    
    margin-top: 80px;
    flex: 1; /* Equal width for all cards */
    min-width: 200px;
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.15); /* Softer shadow for better visual */
    border-top: 5px solid #A63DE7; /* Highlight for visual appeal */
  }
  
  .form-card {
    margin-top: 15px;
    background-color: #ffffff;
    padding: 10px 15px;
    border-radius: 8px;
    box-shadow: 1px 1px 8px rgba(0, 0, 0, 0.1);
  }
  
  h3, h4 {
    color: #A63DE7;
    text-align: center; /* Centered titles for balance */
    margin-bottom: 10px;
  }
  
  ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #eef2ff;
    padding: 5px 10px;
    border-radius: 6px;
    margin-bottom: 5px;
  }
  
  button {
    background-color: #A63DE7;
    color: #fff;
    border: none;
    padding: 5px 12px;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s ease;
  }
  
  button:hover {
    background-color: #8B2BC7;
  }
</style>