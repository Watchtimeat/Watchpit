<template>
  <modal-form title="Solicitação" v-model:show="show" @confirm="confirm">
    <q-form @submit.prevent="confirm" class="q-gutter-md">
      <q-input
        outlined
        stack-label
        label="Código da Ordem de Compra"
        lazy-rules="ondemand"
        type="text"
        v-model="data.code"
        color="grey-7"
        :rules="[
          (value) => !!value || 'O código da ordem de compra é obrigatório',
        ]"
      />
      <q-input
        outlined
        stack-label
        label="Data da Solicitação"
        lazy-rules="ondemand"
        type="date"
        v-model="data.date"
        color="grey-7"
        :rules="[(value) => !!value || 'A data da solicitação é obrigatória']"
      />

      <div class="row">
        <q-space />
        <q-btn
          label="Confirmar"
          type="submit"
          class="full-width wt-border"
          color="dark"
        />
      </div>
    </q-form>
  </modal-form>
</template>

<script setup>
import { computed, ref } from "@vue/reactivity";
import { toLocalISOString } from "../../functions";
import { useQuasar } from "quasar";
import PurchaseOrdersService from "../../services/PurchaseOrdersService";
import ModalForm from "../../components/modal-form.vue";

const $q = useQuasar();
const props = defineProps(["show", "modelValue"]);
const emit = defineEmits(["update:show", "update:modelValue", "confirm"]);
const data = ref({});

const show = computed({
  get: () => {
    let requested;
    if (props.modelValue?.requested) {
      requested = toLocalISOString(new Date(props.modelValue?.requested));
    } else {
      requested = toLocalISOString(new Date());
    }
    data.value = {
      code: props.modelValue?.code,
      date: requested ? requested.slice(0, 10) : null,
      time: requested ? requested.slice(11) : "00:00",
    };
    return props.show;
  },
  set: (value) => {
    emit("update:show", value);
  },
});

async function confirm() {
  const purchaseOrder = { ...props.modelValue };
  purchaseOrder.code = data.value.code;
  purchaseOrder.status = "requested";
  purchaseOrder.requested = new Date().toISOString();

  try {
    const updatedPurchaseOrder =
      await PurchaseOrdersService.updatePurchaseOrder(purchaseOrder);
    emit("update:modelValue", updatedPurchaseOrder);
    emit("update:show", false);
    emit("confirm");

    $q.notify({
      message: "Pedido de compra solicitado",
      type: "positive",
      color: "green",
    });
  } catch (error) {
    $q.notify({
      message: "Erro ao solicitar o pedido de compra",
      type: "negative",
      color: "danger",
    });
  }
}
</script>
