import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

//创建VueX对象
const store = new Vuex.Store({
  state: {
    //存放的键值对就是所要管理的状态
    name: 'helloVueX',
    item: '',
    user: '',
    path: '',
    scriptData: '',
    protocol: '',
  },
  getters: {
    getItem(state) {
      return state.item
    },
    getPath(state) {
      return state.path
    },
    getScriptData(state) {
      return state.scriptData
    },
    getProtocol(state) {
      return state.protocol
    },
  },
  mutations: {
    changeItem(state, newItem) {
      state.item = newItem
      // console.log('changeItem', state.item)
    },
    setUser(state, newUser) {
      state.user = newUser
    },
    setPath(state, newPath) {
      state.path = newPath
    },
    setScriptData(state, newData) {
      state.scriptData = newData
    },
    setProtocol(state, newData) {
      state.protocol = newData
    },
  },
})
export default store
