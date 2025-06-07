export default {
  namespaced: true,

  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    userRole: localStorage.getItem('userRole') || null,
    loading: false,
    authError: null
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
    },
    SET_AUTH_ERROR(state, error) {
      state.authError = error
    }
  },

  actions: {
    async login({ commit }, { email, password }) {
      commit('SET_LOADING', true)
      commit('SET_AUTH_ERROR', null)

      try {
        // Простая логика определения роли
        let role = 'employee'

        if (email === 'admin@company.com' && password === 'admin123') {
          role = 'admin'
        } else if (email === 'manager@company.com' && password === 'manager123') {
          role = 'manager'
        }

        const user = {
          email,
          id: Date.now(),
          role
        }

        // Сохраняем пользователя и роль
        commit('SET_USER', user)
        commit('SET_USER_ROLE', role)
        localStorage.setItem('user', JSON.stringify(user))
        localStorage.setItem('userRole', role)

        return user
      } catch (error) {
        commit('SET_AUTH_ERROR', 'Неверные учетные данные')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async logout({ commit }) {
      localStorage.removeItem('user')
      localStorage.removeItem('userRole')
      commit('SET_USER', null)
      commit('SET_USER_ROLE', null)
    },

    async checkAuth({ commit }) {
      const userData = localStorage.getItem('user')
      const role = localStorage.getItem('userRole')
      if (userData && role) {
        const user = JSON.parse(userData)
        commit('SET_USER', user)
        commit('SET_USER_ROLE', role)
      }
    }
  },

  getters: {
    isAuthenticated: state => !!state.user,
    currentUser: state => state.user,
    userRole: state => state.userRole,
    isAdmin: state => state.userRole === 'admin',
    isManager: state => state.userRole === 'manager',
    authError: state => state.authError
  }
}
