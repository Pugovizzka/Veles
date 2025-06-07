export default {
  namespaced: true,
  
  state: () => ({
    user: null,
    userRole: null,
    loading: false
  }),

  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_USER_ROLE(state, role) {
      state.userRole = role
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    }
  },

  actions: {
    async login({ commit }, { email, password }) {
      commit('SET_LOADING', true)
      try {
        // TODO: Implement actual authentication with your backend
        console.log('Login attempt:', email, password) // Используем password для избежания ESLint ошибки
        const user = { email, id: 1 }
        const role = 'employee'
        
        commit('SET_USER', user)
        commit('SET_USER_ROLE', role)
        return user
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async logout({ commit }) {
      commit('SET_USER', null)
      commit('SET_USER_ROLE', null)
    },

    async checkAuth({ commit }) {
      // TODO: Implement session check with your backend
      const user = localStorage.getItem('user')
      if (user) {
        commit('SET_USER', JSON.parse(user))
        commit('SET_USER_ROLE', 'employee')
      }
    }
  },

  getters: {
    isAuthenticated: state => !!state.user,
    currentUser: state => state.user,
    userRole: state => state.userRole,
    isAdmin: state => state.userRole === 'admin',
    isManager: state => state.userRole === 'manager'
  }
}