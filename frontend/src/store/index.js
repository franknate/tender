import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentTender: null,
    currentRound: 1
  },
  mutations: {
    switchTender(state, tenderId) {
      fetch("http://127.0.0.1:8000/api/tenders/" + tenderId, {
        method: "get"
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
  }
})




