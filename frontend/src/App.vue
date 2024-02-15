<template>
  <router-view />
</template>

<script>
import { useQuasar } from "quasar";
import Emitter from "./services/EventBus";

export default {
  setup() {
    const $q = useQuasar();
    Emitter.on("error", (message) => {
      $q.notify({
        caption: message,
        type: "negative",
        color: "danger",
      });
    });
  },
};
</script>
