// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'bootstrap/dist/css/bootstrap.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import Vuetify from 'vuetify'
import App from './App';
import router from './router';

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(Vuetify, {
 iconfont: 'mdi'
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
