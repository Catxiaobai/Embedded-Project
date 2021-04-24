import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const originalPush = VueRouter.prototype.push

VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch((err) => err)
}

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login/Login'),
  },
  {
    path: '/main',
    name: 'main',
    component: () => import('@/views/Main'),
    children: [
      {
        path: '/main',
        name: 'home',
        component: () => import('@/views/Home/Home'),
      },
      {
        path: '/item',
        name: 'item',
        component: () => import('@/views/InfoManage/Item/Item'),
      },
      {
        path: '/authority',
        name: 'authority',
        component: () => import('@/views/InfoManage/System/Authority'),
      },
      {
        path: '/personnel',
        name: 'personnel',
        component: () => import('@/views/InfoManage/System/Personnel'),
      },
      {
        path: '/tools',
        name: 'tools',
        component: () => import('@/views/InfoManage/System/Tools'),
      },
    ],
  },
  {
    path: '/itemMain',
    name: 'itemMain',
    component: () => import('@/views/ItemMain'),
    children: [
      {
        path: '/itemMain',
        name: 'home',
        component: () => import('@/views/Home/Home'),
      },
    ],
  },
]

const router = new VueRouter({
  routes,
})

export default router
