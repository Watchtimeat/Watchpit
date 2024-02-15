<template>
  <q-dialog v-model="toggleDialog">
    <q-card style="width: 500px; max-width: 80vw" class="wt-border q-pa-md">
      <q-card-section class="row items-center q-pa-none">
        <div class="title-style q-pa-none">{{ title }}</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>

      <q-card-section class="q-px-none"> {{ message }} </q-card-section>


      <q-card-section v-if="requireInput" class="q-px-none">
        <q-input v-model="userInput" outlined placeholder="Digite aqui..." />
      </q-card-section>

      <q-card-actions align="right" class="q-pa-none q-mt-sm">
        <q-btn
          flat
          :label="cancelText ? cancelText : `Cancelar`"
          color="grey"
          v-close-popup
          @click="close"
          class="wt-border"
        />
        <q-btn
          unelevated
          :label="confirmationText ? confirmationText : `Confirmar`"
          color="secondary"
          @click="confirm"
          v-close-popup
          class="wt-border"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { computed,ref } from "vue";
const props = defineProps([
  "title",
  "confirmationText",
  "dialog",
  "cancelText",
  "message",
  "requireInput",
  "text"
]);
const emit = defineEmits(["confirm", "close", "update:dialog","userInput"]);

const userInput = ref(props.text ? props.text : '');

const toggleDialog = computed({
  get() {
    return props.toggleDialog;
  },
  set(value) {
    emit("update:dialog", value);
  },
});

async function confirm() {
  if (props.requireInput) {
    emit("confirm", userInput.value);
    userInput.value = props.text
  }else{
  emit("confirm");
}
}

function close() {
  emit("close");
  
}
</script>
