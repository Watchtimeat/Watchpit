<template>
  <q-dialog v-model="showDialog">
    <q-card style="width: 100%" class="wt-border">
      <q-card-section class="row">
        <div class="title-style">{{ title }}</div>
        <q-space />
        <q-btn icon="close" flat round dense @click="close" />
      </q-card-section>
      <q-card-section>
        <slot></slot>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps(["title", "show"]);
const emit = defineEmits(["update:show", "close"]);
const showDialog = computed({
  get() {
    return props.show;
  },
  set(value) {
    emit("update:show", value);
  },
});

async function confirm() {
  emit("confirm");
}

function close() {
  emit("update:show", false);
}
</script>
