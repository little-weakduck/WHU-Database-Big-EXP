import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('../login/Login.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('../login/Login.vue')
    },
    {
      path: '/course',
      name: 'Course',
      component: () => import('../Home.vue')
    },
    {
      path: '/my',
      name: 'My',
      component: () => import('../Home.vue')
    },
    {
      path: '/course/detail',
      name: 'CourseDetail',
      component: () => import('../course/CourseDetail.vue'),
      props: true
    }
  ]
});

export default router;
