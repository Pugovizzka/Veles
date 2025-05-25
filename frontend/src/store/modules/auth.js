import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
)

export default {
  namespaced: true,
  
  state: () => ({
    user: null,
    loading: false
  }),

  mutations: {
    SET_USER(state, user) {
      state.user = user
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
        
        commit('SET_USER', user)
        return user
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async logout({ commit }) {
      await supabase.auth.signOut()
      commit('SET_USER', null)
    },

    async checkAuth({ commit }) {
      const { data: { session } } = await supabase.auth.getSession()
      commit('SET_USER', session?.user ?? null)
    }
  },

  getters: {
    isAuthenticated: state => !!state.user,
    currentUser: state => state.user
  }
}