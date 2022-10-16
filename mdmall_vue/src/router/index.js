import Vue from 'vue'
import VueRouter from 'vue-router'
import Cookies from "js-cookie";
import {getUser} from "@/api/user.request";
import store from '@/store'
import {canTo} from "@/router/utils";


const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location, resolve, reject) {
    if (resolve || reject) return originalPush.call(this, location, resolve, reject)
    return originalPush.call(this, location).catch((e) => {
    })
}

Vue.use(VueRouter)

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/login'),
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('@/views/register')

    },
    {
        path: '/',
        name: 'Index',
        meta: {
            normal: true
        },
        component: () => import('@/views/index')
    },
    {
        path: '/user_center',
        name: 'UserCenter',
        component: () => import('@/views/user_center/user_center'),
        redirect: '/user_center/user_info',
        children: [
            {
                name: 'user_info',
                path: 'user_info',
                meta: {
                    authentication: true
                },
                component: () => import('@/views/user_center/components/user_info'),
            },
            {
                name: 'user_order',
                path: 'user_order',
                meta: {
                    authentication: true
                },
                component: () => import('@/views/user_center/components/user_order'),

            },
            {
                name: 'user_home',
                path: 'user_home',
                meta: {
                    authentication: true
                },
                component: () => import('@/views/user_center/components/user_home'),

            },
            {
                name: 'user_changePass',
                path: 'user_changePass',
                meta: {
                    authentication: true
                },
                component: () => import('@/views/user_center/components/user_changePass'),

            },
        ]
    },
    {
        path: '/cart',
        name: 'Cart',
        meta: {
            authentication: true
        },
        component: () => import('@/views/cart')
    },
    {
        path: '/place_order',
        name: 'PlaceOrder',
        meta: {
            authentication: true
        },
        component: () => import('@/views/place_order')
    },
    {
        path: '/detail',
        name: 'Detail',
        meta: {
            normal: true
        },
        component: () => import('@/views/detail')
    },
    {
        path: '/active',
        name: 'Active',
        meta: {
            authentication: true
        },
        component: () => import('@/views/active')
    },
    {
        path: '/order_success',
        name: 'OrderSuccess',
        meta: {
            authentication: true
        },
        component: () => import('@/views/order_success')
    },
    {
        name: 'Search',
        path: '/search',
        meta:{
          normal: true
        },
        component: () => import('@/views/search')
    }
]

const router = new VueRouter({
    mode: 'history',
    routes
})

router.beforeEach((to, from, next) => {

    console.log('路由进入拦截', to);
    console.log('路由进入拦截', store);
    const token = Cookies.get('user_token')
    if (to.meta.authentication) {
        canTo({'name': 'Login'}, token, next)
    } else if (to.meta.normal) {
        canTo('', token, next)
    } else {
        next()
    }
})

router.afterEach((to, from) => {
    window.scrollTo(0, 0)
})

export default router
