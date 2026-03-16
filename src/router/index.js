import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../components/Login.vue')
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue')
  },
  {
    path: '/carousel',
    name: 'Carousel',
    component: () => import('../views/Carousel.vue')
  },
  {
    path: '/announcement',
    name: 'Announcement',
    component: () => import('../views/Announcement.vue')
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('../views/Users.vue')
  },
  {
    path: '/news',
    name: 'News',
    component: () => import('../views/News.vue')
  },
  {
    path: '/news-category',
    name: 'NewsCategory',
    component: () => import('../views/NewsCategory.vue')
  },
  {
    path: '/covid-data',
    name: 'CovidData',
    component: () => import('../views/CovidData.vue')
  },
  {
    path: '/health-report',
    name: 'HealthReport',
    component: () => import('../views/HealthReport.vue')
  },
  {
    path: '/entry-exit',
    name: 'EntryExit',
    component: () => import('../views/EntryExit.vue')
  },
  {
    path: '/dynamic-report',
    name: 'DynamicReport',
    component: () => import('../views/DynamicReport.vue')
  },
  {
    path: '/medical-office',
    name: 'MedicalOffice',
    component: () => import('../views/MedicalOffice.vue')
  },
  {
    path: '/medical-assignment',
    name: 'MedicalAssignment',
    component: () => import('../views/MedicalAssignment.vue')
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: () => import('../views/Analytics.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router