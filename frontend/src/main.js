import Vue from "vue";
import App from "./App.vue";
import "./plugins/bootstrap-vue";
import store from './store'
import axios from 'axios';

axios.defaults.withCredentials = true
axios.defaults.baseURL = "http://localhost:8000/api/"

Vue.config.productionTip = false;

new Vue({
  store,
  render: h => h(App)
}).$mount("#app");
