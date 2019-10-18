import Vue from 'vue'
import App from './App.vue'

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

import VueRouter from 'vue-router'

import router from './router'

import axios from 'axios'
Vue.prototype.axios = axios

// Vue.prototype.host = "http://183.6.116.44:18080/api"
// Vue.prototype.host = "http://192.168.127.97/api"
Vue.prototype.host = window.location.origin+"/api"
Vue.prototype.host = "http://127.0.0.1:8000/api"
console.log = function () {}

Vue.use(ElementUI);
Vue.use(VueRouter)

Vue.filter('format',function(date,fmt){
var o = {
	"M+" : date.getMonth()+1,                 //月份
	"d+" : date.getDate(),                    //日
	"h+" : date.getHours(),                   //小时
	"m+" : date.getMinutes(),                 //分
	"s+" : date.getSeconds(),                 //秒
	"q+" : Math.floor((date.getMonth()+3)/3), //季度
	"S"  : date.getMilliseconds()             //毫秒
	};
if(/(y+)/.test(fmt))
	fmt=fmt.replace(RegExp.$1, (date.getFullYear()+"").substr(4 - RegExp.$1.length));
for(var k in o)
	if(new RegExp("("+ k +")").test(fmt))
fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
return fmt;
})

new Vue({
  el: '#app',
	router,
  render: h => h(App)
})
