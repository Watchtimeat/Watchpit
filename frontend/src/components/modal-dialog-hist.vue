<template>
  <q-dialog v-model="toggleDialogHist">
    <q-card style="width: 500px; max-width: 80vw" class="wt-border q-pa-md">
      <q-card-section class="row items-center q-pa-none">
        <div class="title-style q-pa-none">  Lançar histórico OS {{ OS }}</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>



      <q-card-section class="q-mt-md">
        <q-input v-model="userTitle" label="Título" class="q-mt-md" outlined placeholder="Digite o título aqui..." />
        <q-input v-model="userText" type="textarea" label="Texto" class="q-mt-md"  outlined placeholder="Digite o texto aqui..." />
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
  "text",
  "OS"
]);
const emit = defineEmits(["confirm", "close", "update:dialog","userTitle","userText"]);

const userText = ref('')
const userTitle = ref('')

const toggleDialogHist = computed({
  get() {
    return props.toggleDialogHist;
  },
  set(value) {
    emit("update:dialog", value);
  },
});

async function confirm() {
    emit("confirm", userTitle.value,userText.value);
    userTitle.value = ''
    userText.value = ''

}

function close() {
  emit("close");
  
}
</script>
