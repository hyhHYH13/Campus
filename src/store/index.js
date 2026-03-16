import { createStore } from 'vuex'

const store = createStore({
  state: {
    user: null,
    token: null
  },
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setToken(state, token) {
      state.token = token
    },
    logout(state) {
      state.user = null
      state.token = null
    }
  },
  actions: {
    login({ commit }, { user, token }) {
      commit('setUser', user)
      commit('setToken', token)
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('token', token)
    },
    logout({ commit }) {
      commit('logout')
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    },
    loadUser({ commit }) {
      const userStr = localStorage.getItem('user')
      const token = localStorage.getItem('token')
      if (userStr && token) {
        commit('setUser', JSON.parse(userStr))
        commit('setToken', token)
      }
    }
  },
  getters: {
    isLoggedIn: state => !!state.token,
    user: state => state.user
  }
})

export default store