export default {
  state: {
    username: null,
    token: null,
  },
  getters: {
    IsAuthenticated: (state) => !!state.username,
    UserName: (state) => state.username,
    Token: (state) => state.token,
  },
  actions: {
    LogIn({ commit, rootState }, User) {
      return new Promise((resolve, reject) => {
        fetch(rootState.BASE_URL + "login/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(User),
        })
          .then((response) => {
            if (response.ok) {
              return response.json();
            } else {
              throw new Error("Invalid credidentals");
            }
          })
          .then(
            (data) => {
              commit({
                type: "login",
                username: User.username,
                token: data.token,
              });
              resolve();
            },
            (error) => {
              reject(error);
            }
          );
      });
    },
    LogOut({ commit }) {
      let user = null;
      commit("logout", user);
    },
  },
  mutations: {
    login(state, payload) {
      state.username = payload.username;
      state.token = payload.token;
    },
    logout(state) {
      state.username = null;
      state.token = null;
    },
  },
};
