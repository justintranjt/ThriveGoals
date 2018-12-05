import Vue from 'vue';
import Router from 'vue-router';
import Goals from '@/components/Goals';
import Splash from '@/components/Splash';
import NotFound from '@/components/NotFound';

Vue.use(Router);

export default new Router({
    routes: [{
            path: '/',
            name: 'Splash',
            component: Splash,
        },
        {
            path: '/goals',
            name: 'Goals',
            component: Goals,
        },
        { path: '/404', component: NotFound},
        { path: '*', component: NotFound},
    ],
    mode: 'history',
});