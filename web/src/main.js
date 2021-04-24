import Vue from 'vue'
import App from './App.vue'
import router from './router'
import http from '@/api/config'
import store from './store'
import JsonExcel from 'vue-json-excel'
// 全局配置
import '@/assets/scss/reset.scss'
import 'element-ui/lib/theme-chalk/index.css'
import Api from './router/Api' //导入全局接口

// 第三方包
import ElementUI from 'element-ui'

Vue.use(ElementUI)
Vue.prototype.bus = new Vue()
Vue.prototype.$http = http
Vue.prototype.Global_Api = Api.Global_Api
Vue.component('downloadExcel', JsonExcel)
Vue.config.productionTip = false
new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app')
