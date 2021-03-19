import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import auth from './modules/auth';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    tenders: [],
    currentTender: null,
    currentRound: 1,
    lastRound: 1,
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

          // Update lastRound variable
          let bids = state.currentTender.units[0].bids
          for (let bid_round of state.currentTender.bid_rounds) {
            if (bid_round.id == bids[bids.length-1].bid_round) state.lastRound = bid_round.number
          }

        } else {
          console.log("Error in switchTender", response)
        }
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
  plugins: [createPersistedState({
    paths: ["auth"]
  }
  )]
})




