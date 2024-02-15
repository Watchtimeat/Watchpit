import { createApp } from "vue";
import { Quasar, Dialog, Notify } from "quasar";
import App from "./App.vue";
import router from "./router";
import Api from "./services/Api";
import langPt from "quasar/lang/pt-BR";
import VueApexCharts from "vue3-apexcharts";
import "@quasar/extras/material-icons/material-icons.css";
import "@quasar/extras/material-icons-outlined/material-icons-outlined.css";
import "quasar/dist/quasar.css";
import "./style.css";
import Vue3Autocounter from "vue3-autocounter";

if (import.meta.env.VITE_API_URL) Api.setBaseURL(import.meta.env.VITE_API_URL);

const app = createApp(App);
app.use(Quasar, {
  lang: langPt,
  config: {
    brand: {
      primary: "#1976d2",
      secondary: "#8c897d",
      grey: "#555567",
      dark: "#333333",
      white: "#FFFFFF",
      success: "#4caf50",
      danger: "#bd0700",
    },
    notify: {
      position: "top-right",
    },
  },
  plugins: { Dialog, Notify },
});
app.use(VueApexCharts);
app.use(Vue3Autocounter);
app.use(router);
app.mount("#app");
