import { createRouter, createWebHashHistory } from "vue-router";
import Main from "./views/Main.vue";
import Home from "./views/private/Home.vue";
import Info from "./views/private/Info.vue";
import Login from "./views/public/Login.vue";
import ResetPassword from "./views/public/ResetPassword.vue";
import AuthService from "./services/AuthService";
import Services from "./views/private/Services.vue";
import Videos from "./views/private/Videos.vue";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      name: "main",
      component: Main,
      children: [
        { path: "/home", name: "home", component: Home },
        {
          path: "/purchase_orders",
          name: "purchaseOrders",
          component: () => import("./views/private/PurchaseOrders.vue"),
        },
        {
          path: "/purchase_invoices",
          name: "purchaseInvoices",
          component: () => import("./views/private/PurchaseInvoices.vue"),
        },
        {
          path: "/products",
          name: "products",
          component: () => import("./views/private/Products.vue"),
        },
        {
          path: "/parts_conference",
          name: "parts_conference",
          component: () => import("./views/private/PartsConference.vue"),
        },
        {
          path: "/purchases",
          name: "purchases",
          component: () => import("./views/private/Purchases.vue"),
        },
        {
          path: "/services",
          name: "services",
          component: Services,
        },
        {
          path: "/importation",
          name: "importation",
          component: () => import("./views/private/Importation.vue"),
        },
        {
          path: "/settings/general",
          name: "settings_general",
          component: () => import("./views/private/settings/General.vue"),
        },
        {
          path: "/settings/user",
          name: "settings_user",
          component: () => import("./views/private/settings/User.vue"),
        },
        {
          path: "/settings/users",
          name: "settings_users",
          component: () => import("./views/private/settings/Users.vue"),
        },
        { path: "/info", name: "info", component: Info },
        {
          path: "/videos",
          name: "videos",
          component: Videos,
        },
      ],
    },
    { path: "/login", name: "login", component: Login },
    {
      path: "/reset_password",
      name: "reset_password",
      component: ResetPassword,
    },
  ],
});

router.beforeEach(async (to, from, next) => {
  let currentUser = null;
  if (from.name == undefined) currentUser = await AuthService.getCurrentUser();
  if (
    !AuthService.isAuthenticated() &&
    to.path != "/login" &&
    to.path != "/reset_password"
  )
    next({ path: "/login" });
  else next();
});

export default router;
