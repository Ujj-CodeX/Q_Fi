import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from '@/components/HelloWorld.vue';
import QuizUser from '@/components/QuizUser.vue';
import QuizPreferences from '@/components/QuizPreferences.vue';
import AdminDash from '@/components/AdminDash.vue';
import QuizManage from '@/components/QuizManage.vue';
import SignUp from '@/components/SignUp.vue';
import AdminLogin from '@/components/AdminLogin.vue';
import ChangePassword from '@/components/ChangePassword.vue';
import TestPage from '@/components/TestPage.vue'; 
import LeaderBoard from '@/components/LeaderBoard.vue';
import AdminSummary from '@/components/AdminSummary.vue'; 



const routes = [
  { path: '/', component: HelloWorld },
  { path: '/user', component: QuizUser },
  { 
    path: '/quiz-preferences/:quizName', 
    name: 'QuizPreferences', 
    component: QuizPreferences 
  },
  { 
    path: '/admin-dashboard', 
    name: 'AdminDash', 
    component: AdminDash
  },
  { 
    path: '/quiz-management', 
    name: 'QuizManage', 
    component: QuizManage
  },
  { 
    path: '/signup', 
    name: 'SignUp', 
    component: SignUp  // Added SignUp route
  },
  { path: '/admin-login', component: AdminLogin },
  {
    path: '/change-password',   // Add Change Password route
    name: 'ChangePassword',
    component: ChangePassword
  },
  {
    path: '/test_page',
    name: 'TestPage',
    component: TestPage,
    props: (route) => ({
        quizName: route.query.quizName,
        duration: route.query.duration,
        questions: route.query.questions
    })
},
{
  path: '/leaderBoard',
  name: 'LeaderBoard',
  component: LeaderBoard
},
{
  path: '/admin-summary',   // The route path for the Admin Summary page
  name: 'AdminSummary',     // The name of this route
  component: AdminSummary,  // The component to render when this route is accessed
}

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
