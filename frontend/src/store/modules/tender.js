export default {
  state: {
    tenders: [],
    currentTender: null,
    bids: null,
    initialBids: null
  },
  getters: {
    Tenders: (state) => state.tenders,
    CurrentTender: (state) => state.currentTender,
    Bids: (state) => state.bids,
    InitialBids: (state) => state.initialBids
  },
  actions: {
    getTenders({ commit, rootState }) {
      fetch(rootState.BASE_URL + "tenders/", {
        method: "get",
        headers: {
          Authorization: "Token " + rootState.auth.token,
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          commit("setTenders", data)
        });
    },
    switchTender({ commit, dispatch, rootState}, tenderId) {
      fetch(rootState.BASE_URL + "tenders/" + tenderId + "/", {
        method: "get",
        headers: {
          Authorization: "Token " + rootState.auth.token,
        },
      })
        .then((response) => response.json().then((data) => ({ status: response.status, body: data })))
        .then((response) => {
          if (response.status == "200") {
            commit("setCurrentTender", response.body)
            dispatch("getBids", tenderId)
          } else {
            console.log("Error in switchTender", response);
          }
        });
    },
    reloadTender({ state, dispatch }) {
      dispatch("switchTender", state.currentTender.id);
    },
    deleteTender({ commit, dispatch, rootState }, tenderId) {
      fetch(rootState.BASE_URL + "tenders/" + tenderId + "/", {
        method: "delete",
        headers: {
          Authorization: "Token " + rootState.auth.token,
        },
      })
      .then((response) => {
        if (response.ok) {
          dispatch("getTenders")
        } else {
          console.log("Error in deleteTender", response)
        }
      });
    },
    getBids({ state, commit, rootState }, tenderId) {
      fetch(rootState.BASE_URL + "bid/" +tenderId + "/", {
        method: "GET",
        headers: {
          "Authorization": "Token " + rootState.auth.token,
        }
      })
      .then(response => response.json().then(data => ({status: response.status, body: data})))
      .then(response => {
        if (response.status == "200") {
          commit("setBids", response.body)
        } else {
          console.error("Error in tender.js, getBids()")
        }
      });
    },
  },
  mutations: {
    setTenders(state, tenders) {
      state.tenders = tenders
    },
    setCurrentTender(state, tender) {
      state.currentTender = tender
    },
    setBids(state, bids) {
      state.bids = bids
      state.initialBids = JSON.parse(JSON.stringify(bids))
    }
  },
};
