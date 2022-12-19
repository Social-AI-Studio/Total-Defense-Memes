import Vue from 'vue'
import VueRouter from 'vue-router'

import auth from '../utils/auth'
import Login from '../views/Login.vue'

Vue.use(VueRouter)

function requireAuth(to, from, next) {
  if (!auth.loggedIn()) {
    next({
      path: '/',
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
}

const routes = [
  {
    path: '/',
    name: 'login',
    component: Login
  },
  {
    path: '/batches',
    name: 'batches',
    beforeEnter: requireAuth,
    component: () => import(/* webpackChunkName: "about" */ '../views/Batches.vue')
  },
  {
    path: '/batch/:batchId',
    name: 'batch',
    beforeEnter: requireAuth,
    component: () => import(/* webpackChunkName: "about" */ '../views/Batch.vue')
  },
  {
    path: '/logout',
    beforeEnter(to, from, next) {
      auth.logout()
      next('/')
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router