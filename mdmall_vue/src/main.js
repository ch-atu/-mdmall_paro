import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import 'default-passive-events'

// 引入element ui组件
import '@/utils/elementUI'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
