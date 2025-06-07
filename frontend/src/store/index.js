import { createStore } from 'vuex'
import auth from './modules/auth'

export default createStore({
  modules: {
    auth
  },
  state: {
    sidebarCollapsed: false
  },
  mutations: {
    TOGGLE_SIDEBAR(state) {
      state.sidebarCollapsed = !state.sidebarCollapsed
    }
  },
  getters: {
    isSidebarCollapsed: state => state.sidebarCollapsed
  }
})