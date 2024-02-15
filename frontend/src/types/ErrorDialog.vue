<template>
  <q-dialog v-model="localShowErrorDialog">
    <q-card>
      <q-card-section>
        <h5>Erros encontrados</h5>
        <ul>
          <li v-for="(error, index) in errors" :key="index">{{ error.id }}: {{ error.problem }}</li>
        </ul>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Fechar" color="primary" v-close-popup 
        @click="fecharModal"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  props: {
    showErrorDialog: {
      type: Boolean,
      default: false
    },
    errors: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      localShowErrorDialog: this.showErrorDialog
    };
  },
  watch: {
    showErrorDialog(newVal) {
      this.localShowErrorDialog = newVal;
    }
  },
  methods: {
    fecharModal() {
      this.localShowErrorDialog = false;
      this.$emit('close-dialog');
    }
  },
  emits: ['close-dialog']
}
</script>






