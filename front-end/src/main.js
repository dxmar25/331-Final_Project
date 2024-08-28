import './style.css'

import App from '@/App.vue';
import Admin from '@/layouts/Admin.vue';
import Login from '@/views/auth/Login.vue';
import AllTables from '@/views/manager/AllTables.vue';
import Analytics from '@/views/manager/Analytics.vue';
import Dashboard from '@/views/manager/Dashboard.vue';
import CashierMenuBoard from '@/views/menuboard/CashierMenuBoard.vue';
import CustomerMenuBoard from '@/views/menuboard/CustomerMenuBoard.vue';
import Welcome from '@/views/Welcome.vue';
import {createApp} from 'vue'
import {createRouter, createWebHistory} from 'vue-router'

import {auth, authPipeline} from './middleware/auth';
import Kitchen from './views/kitchen/Kitchen.vue';
import InventoryPage from './views/manager/InventoryPage.vue';
import MenuPage from './views/manager/MenuPage.vue';
import UserPage from './views/manager/UserPage.vue';
import GeneralMenuBoard from './views/menuboard/GeneralMenuBoard.vue';
import CreatePage from '@views/manager/CreatePage.vue'

const routes = [
  {
    path: '/menu-board',
    component: GeneralMenuBoard,
  },
  {path: '/kitchen', component: Kitchen, meta: {middleware: [auth]}},
  {
    path: '/cashier-order',
    component: CashierMenuBoard,
    meta: {middleware: [auth], 

    requiresInit: true,

    }
  },
  {
    path: '/manager',
    redirect: '/manager/dashboard',
    component: Admin,
    children: [
      {
        path: 'dashboard',
        component: Dashboard,
      },
      {
        path: 'tables',
        component: AllTables,
      },
      {
        path: 'inventory',
        component: InventoryPage,
      },
      {
        path: 'menu',
        component: MenuPage,
      },
      {
        path: 'users',
        component: UserPage,
      },
      {
        path: 'analytics',
        component: Analytics,
      },
      {
        path: 'create',
        component: CreatePage,
      },
    ],
    meta: {middleware: [auth]}
  },
  {
    path: '/customer-order',
    component: CustomerMenuBoard,
  },
  {
    name: 'auth',
    path: '/auth',
    component: Login,
  },
  {
    path: '/',
    component: Welcome,
  },
  {
    path: '',
    component: Welcome,
  },
  {path: '/:pathMatch(.*)*', redirect: '/'},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  /** Navigate to next if middleware is not applied */
  if (!to.meta.middleware) {
    return next()
  }

  const middleware = to.meta.middleware;
  const context = {
    to,
    from,
    next,
  }

  return middleware[0]({...context, next: authPipeline(context, middleware, 1)})
})

const app = createApp(App)
app.use(router);
app.mount('#app');

export const OrderStatus = {
  IN_PROGRESS: 0,
  COMPLETED: 1,   // kitchen staff
  INCOMPLETE: 2,  // for a refund, kitchen has access to this, cancelled order
                  // after payment went through
  DELETED: 3  // for deletion, mark this field if something is being deleted,
              // managed by Admin
};
export const UserRole = {
  CUSTOMER: 0,  // just a user who logged in and made an account. Can implement
                // point system if time allows.
  KITCHEN: 1,   // someone who has access to mark orders as completed or
                // cancelled and sees only the kitchen screen.
  CASHIER: 2,   // has only access to edit and make orders.
  MANAGER: 3,   // has access to analytics/manager's page.
  ADMIN: 4      // has administrative privileges.
};

export const MenuCategories = {
  SEASONAL: '8',
  COMBOS: '7',
  BURGERS: '0',
  BASKETS: '1',
  SANDWICHES: '2',
  'SHAKES N SWEETS': '3',
  BEVERAGES: '4',
  SIDES: '5',
  SAUCES: '6'
};

export const ReverseMenuCategories = {
  '0': 'BURGERS',
  '1': 'BASKETS',
  '2': 'SANDWICHES',
  '3': 'SHAKES N SWEETS',
  '4': 'BEVERAGES',
  '5': 'SIDES',
  '6': 'SAUCES',
  '7': 'COMBOS',
  '8': 'SEASONAL'
}


export const LOCAL_BASE_URL = import.meta.env.VITE_API_LOCAL_BASE_URL
export const PROD_BASE_URL = import.meta.env.VITE_API_PROD_BASE_URL
