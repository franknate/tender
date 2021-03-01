import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentTenderId: 8
  },
  mutations: {
    switchTender(state, newTenderId) {
      state.currentTenderId = newTenderId
    }
  },
  actions: {
  },
  modules: {
  }
})
