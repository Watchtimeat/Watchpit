<template>
  <modal-form title="Item" v-model:show="showItem" @confirm="confirmProduct">
    <q-form @submit.prevent="confirm" class="q-gutter-md">
      <q-select
        label="Produto"
        outlined
        stack-label
        use-input
        hide-selected
        fill-input
        input-debounce="0"
        :options="products"
        @filter="getProductsBySearch"
        @update:model-value="productSelected"
        type="find"
        v-model="dataItem.product"
        color="grey-7"
        :disable="disabledProduct()"
      >
        <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey">Sem opções</q-item-section>
          </q-item>
        </template>
      </q-select>

      <q-input
        label="Custo Unitário"
        stack-label
        outlined
        step="any"
        type="number"
        v-model.number="dataItem.cost"
        color="grey-7"
      />

      <q-input
        label="Quantidade Solicitada"
        stack-label
        outlined
        step="any"
        type="number"
        v-model.number="dataItem.requested_quantity"
        color="grey-7"
      />

      <div v-for="(control, index) in formItem" :key="index">
        <div>{{ control.label }}</div>
        <q-btn-toggle
          :options="control.options"
          v-model="dataItem[control.field]"
          toggle-color="secondary"
        />
      </div>

      <div class="row">
        <q-space />
        <q-btn
          label="Confirmar"
          type="submit"
          class="full-width wt-border"
          color="dark"
          :loading="working"
        />
      </div>
    </q-form>
  </modal-form>
</template>

<script setup>
import { computed, ref } from "vue";
import ProductsService from "../../services/ProductsService";
import ModalForm from "../../components/modal-form.vue";

const props = defineProps(["show", "item", "brand"]);
const emit = defineEmits(["update:show", "update:item", "confirm"]);
const working = ref(false);
const products = ref([]);
const dataItem = ref({});
const isEdit = ref(false);

function disabledProduct() {
  if (props.item.product_id) {
    return true;
  }

  return false;
}

const showItem = computed({
  get() {
    if (props.show && props.item.product_id) {
      dataItem.value = {
        product: {
          value: props.item.product_id,
          label: props.item.product_name + " (" + props.item.product_code + ")",
        },
        cost: props.item.product_cost,
        requested_quantity: props.item.requested_quantity,
        status: props.item.status,
        OS: props.item.OS,
      };

      if (props.item.product_id && isEdit.value) {
        isEdit.value = true;
      }

      isEdit.value = false;
    } else {
      dataItem.value = {
        status: "active",
      };
    }
    return props.show;
  },
  set(value) {
    emit("update:show", value);
  },
});

const formItem = ref([
  {
    name: "status",
    label: "Situação",
    field: "status",
    type: "select",
    options: [
      { label: "Ativo", value: "active" },
      { label: "Cancelado", value: "cancelled" },
    ],
  },
]);

async function getProductsBySearch(value, update, abort) {
  setTimeout(() => {
    update(async () => {
      if (value && value.length > 2) {
        const search = (
          await ProductsService.getProducts({
            brand: props.brand,
            "code.lk,name.lk": value + "%",
          })
        ).data;
        products.value = [];
        for (let item of search) {
          products.value.push({
            value: item.id,
            label: item.name + " (" + item.code + ")",
          });
        }
      } else {
        products.value = [];
      }
    });
  }, 1000);
}

async function productSelected(selectedProduct) {
  const product = await ProductsService.getProductById(selectedProduct.value);
  if (product) {
    dataItem.value.cost = product.cost;
  }
}

async function confirm() {
  if (dataItem.value) {
    const productId = dataItem.value.product.value;
    const response = await ProductsService.getProductById(productId);
    const product = response.data[0];
    const purchaseOrderItem = {
      product_id: product.id,
      product_code: product.code,
      product_category: product.category,
      product_name: product.name,
      product_cost: dataItem.value.cost,
      requested_quantity: dataItem.value.requested_quantity,
      status: dataItem.value.status,
      OS: dataItem.value.OS,
    };

    emit("update:item", purchaseOrderItem);
  }
  dataItem.value = {};
  emit("update:show", false);
  emit("confirm");
}
</script>
