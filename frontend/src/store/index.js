import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import auth from './modules/auth';
import tender from './modules/tender';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    BASE_URL:
      process.env.VUE_APP_IN_CONTAINER == true
        ? "http://api/"
        : "http://localhost:8000/api/"
  },
  modules: {
    auth: auth,
    tender: tender
  },
  plugins: [
    createPersistedState()
  ]
})
