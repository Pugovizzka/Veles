import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
)

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
        const { data: { user }, error } = await supabase.auth.signInWithPassword({
          email,
          password
        })
        
        if (error) throw error
        
        // Получаем роль пользователя
        const { data: userData, error: roleError } = await supabase
          .from('users')
          .select('role')
          .eq('id', user.id)
          .single()
        
        if (roleError) throw roleError
        
        commit('SET_USER', user)
        commit('SET_USER_ROLE', userData.role)
        return user
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async logout({ commit }) {
      await supabase.auth.signOut()
      commit('SET_USER', null)
      commit('SET_USER_ROLE', null)
    },

    async checkAuth({ commit }) {
      const { data: { session } } = await supabase.auth.getSession()
      if (session?.user) {
        const { data: userData } = await supabase
          .from('users')
          .select('role')
          .eq('id', session.user.id)
          .single()
        
        commit('SET_USER', session.user)
        commit('SET_USER_ROLE', userData?.role)
      } else {
        commit('SET_USER', null)
        commit('SET_USER_ROLE', null)
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