import Vue from 'vue'
import VueRouter from 'vue-router'

import register from '../components/register.vue'
import login from '../components/login.vue'
import forgot from '../components/forgot.vue'
import info from '../components/info.vue'
import account from '../components/account.vue'

import userinfo from '../components/userinfo.vue'
import reservation from '../components/reservation.vue'
import myreservation from '../components/myreservation.vue'
import interview from '../components/interview.vue'

Vue.use(VueRouter)

export default new VueRouter({
	// mode:'history',
	routes:[
    {
      path: '/',
      redirect: '/account',
    },
    {
      path:'/account',
      name:'account',
      component:account,
      redirect: '/account/login',
      children:[
        { path:'login', component: login },
        { path:'register', component: register },
        { path:'forgot' , component: forgot}
      ]
    },
		{
			path:"/info",
			name:"info",
			component:info,
      redirect: '/info/userinfo',
			children:[
				{ path: 'userinfo', component: userinfo },
				{ path: 'reservation', component: reservation },
				{ path: 'myreservation', component: myreservation },
        { path: 'interview', component:interview }
          ]
		},
	]
})
