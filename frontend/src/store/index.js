import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import auth from './modules/auth';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    tenders: [],
    currentTender: null,
    BASE_URL: process.env.VUE_APP_IN_CONTAINER == true ? "http://api/" : "http://localhost:8000/api/"
  },
  mutations: {
    getTenders(state) {
      fetch(state.BASE_URL + "tenders/", {
        method: "get",
        headers: {
          "Authorization": "Token " + state.auth.token
        }
      })
      .then((response) => {
        return response.json()
      })
      .then((jsonData) => {
        state.tenders = jsonData
      })
    },
    switchTender(state, tenderId) {
      fetch(state.BASE_URL + "tenders/" + tenderId + "/", {
        method: "get",
        headers: {
          "Authorization": "Token " + state.auth.token
        }
      })
      .then(response => response.json().then(data => ({status: response.status, body: data})))
      .then(response => {
        if (response.status == "200") {
          state.currentTender = response.body
        } else {
          console.log("Error in switchTender", response)
        }
      });
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
  plugins: [createPersistedState({
    paths: ["auth"]
  }
  )]
})




