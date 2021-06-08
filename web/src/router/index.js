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
      {
        path: '/script',
        name: 'script',
        component: () => import('@/views/Script/Script'),
      },
      {
        path: '/modelEdit',
        name: 'modelEdit',
        component: () => import('@/views/Model/ModelEdit'),
      },
      {
        path: '/modelInfo',
        name: 'modelInfo',
        component: () => import('@/views/Model/ModelInfo'),
      },
      {
        path: '/xmiImport',
        name: 'xmiImport',
        component: () => import('@/views/Model/XmiImport'),
      },
      {
        path: '/itemMember',
        name: 'itemMember',
        component: () => import('@/views/ItemMember/ItemMember'),
      },
      {
        path: '/boundaryValue',
        name: 'boundaryValue',
        component: () => import('@/views/TestDataGeneration/BoundaryValue'),
      },
      {
        path: '/fullMigration',
        name: 'fullMigration',
        component: () => import('@/views/TestDataGeneration/FullMigration'),
      },
      {
        path: '/fullState',
        name: 'fullState',
        component: () => import('@/views/TestDataGeneration/FullState'),
      },
      {
        path: '/interfaceProtocol',
        name: 'interfaceProtocol',
        component: () => import('@/views/TestDataGeneration/InterfaceProtocol'),
      },
      {
        path: '/randomValue',
        name: 'randomValue',
        component: () => import('@/views/TestDataGeneration/RandomValue'),
      },
      {
        path: '/increase',
        name: 'increase',
        component: () => import('@/views/TestDataGeneration/Increase'),
      },
      {
        path: '/decrease',
        name: 'decrease',
        component: () => import('@/views/TestDataGeneration/Decrease'),
      },
      {
        path: '/mcDcCoverage',
        name: 'mcDcCoverage',
        component: () => import('@/views/TestDataGeneration/McDcCoverage'),
      },
      {
        path: '/communicationProtocol',
        name: 'communicationProtocol',
        component: () => import('@/views/CommunicationProtocol/CommunicationProtocol'),
      },
      {
        path: '/dataShow',
        name: 'dataShow',
        component: () => import('@/views/TestDataGeneration/DataShow'),
      },
      {
        path: '/staticModels',
        name: 'staticModels',
        component: () => import('@/views/Model/StaticModels'),
      },
      {
        path: '/staticModelInfo',
        name: 'staticModelInfo',
        component: () => import('@/views/Model/StaticModelInfo'),
      },
      {
        path: '/testTarget',
        name: 'testTarget',
        component: () => import('@/views/TestTarget/TestTarget'),
      },
      {
        path: '/scriptDatabase',
        name: 'scriptDatabase',
        component: () => import('@/views/Script/ScriptDatabase'),
      },
      {
        path: '/conditionCoverage',
        name: 'conditionCoverage',
        component: () => import('@/views/TestDataGeneration/ConditionCoverage'),
      },
      {
        path: '/test',
        name: 'test',
        component: () => import('@/views/CommunicationProtocol/Test'),
      },
      {
        path: '/showEdit',
        name: 'showEdit',
        component: () => import('@/views/CommunicationProtocol/ShowEdit'),
      },
    ],
  },
]

const router = new VueRouter({
  routes,
})

export default router
