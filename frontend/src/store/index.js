import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import auth from './modules/auth';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentTender: null,
    currentRound: 1,
    BASE_URL: process.env.VUE_APP_API_URL
  },
  mutations: {
    switchTender(state, tenderId) {
      fetch(state.BASE_URL + "tenders/" + tenderId + "/", {
        method: "get",
        headers: {
          "Authorization": "Token " + state.auth.token
        }
      })
      .then((response) => {
        return response.json()
      })
      .then((jsonData) => {
        state.currentTender = jsonData
      });
    },
    switchRound(state, round) {
      state.currentRound = round;
    }
  },
  actions: {
    reloadTender(context) {
      context.commit("switchTender", context.state.currentTender.id);
    }
  },
  modules: {
    auth: auth
  },
  plugins: [createPersistedState()]
})




