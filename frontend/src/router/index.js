import Vue from "vue";
import VueRouter from "vue-router";

import AppHeader from "@/components/AppHeader.vue";
import TenderSelector from "@/components/TenderSelector.vue";

Vue.use(VueRouter);

const routes = [
  { path: "/", component: AppHeader },
  { path: "/", component: TenderSelector }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
