import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store'; // Import your router file
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

const app = createApp(App);

app.use(router);
app.use(store); // Add this line to enable routing
app.mount('#app');
