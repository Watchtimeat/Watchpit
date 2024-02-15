<template>
  <q-dialog
    full-width
    persistent
    position="top"
    v-model="_show"
    @hide="$emit('close')"
  >
    <q-card>
      <q-card-section class="row">
        <div class="title-style">
          {{ props.id ? "Editar Proforma" : "Nova Proforma" }}
        </div>
        <q-space />
        <q-btn icon="close" flat round dense @click="_show = false" />
      </q-card-section>
      <q-card-section class="row">
        <q-select
          label="Marca*"
          dense
          outlined
          stack-label
          use-input
          hide-selected
          fill-input
          input-debounce="0"
          :options="brandsFiltered"
          type="find"
          color="grey-7"
          class="col-md-2"
          v-model="invoiceForm.brand"
          @filter="filterBrand"
          @update:model-value="loadPurchaseOrders"
        >
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey">Sem opções</q-item-section>
            </q-item>
          </template>
        </q-select>
        <q-input
          v-model="invoiceForm.proforma_code"
          dense
          outlined
          stack-label
          color="grey-7"
          type="search"
          label="Código da Proforma*"
          debounce="300"
          class="wt-border q-ml-lg"
        />

      </q-card-section>

      <q-card-section v-if="invoiceForm.brand" class="q-pt-none">
        <div class="subtile-style q-mb-md">
          Lista de pedidos da marca
          <span class="text-weight-medium">{{ invoiceForm.brand.label }}</span>
          com status
          <span class="text-secondary text-weight-medium">Solicitado, </span>
          <span class="text-secondary text-weight-medium">Confirmado</span>

          e
          <span class="text-secondary text-weight-medium">Recebendo</span>
        </div>
        <invoice-purchase-list
          :purchaseList="orderList.data"
          :invoiceForm="invoiceForm"
          :closeModal="closeModal"
        />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import PurchaseOrdersService from "../../services/PurchaseOrdersService";
import ProductsService from "../../services/ProductsService";
import InvoicePurchaseList from "@/components/Invoice/InvoicePurchaseList.vue";

const props = defineProps(["show", "id", "dataPurchaseInvoice"]);
const emit = defineEmits(["update:show", "close"]);
const _show = computed({
  get: () => {
    if (props.show && ordersRef.value)
      ordersRef.value.requestServerInteraction();
    return props.show;
  },
  set: (value) => {
    invoiceForm.value = {};
    emit("update:show", value);
  },
});

const invoiceForm = ref({});
const ordersRef = ref();
const brands = ref([]);
const ordersLoading = ref(false);
const orderList = ref({});
const brandsFiltered = ref([]);

onMounted(() => {
  loadBrands();
});

function filterBrand(val, update) {
  if (val === "") {
    update(() => {
      brandsFiltered.value = brands.value;
    });
    return;
  }

  update(() => {
    brandsFiltered.value = brands.value.filter(
      (brand) => brand.label.toLowerCase().indexOf(val.toLowerCase()) > -1
    );
  });
}

async function loadBrands() {
  const response = await ProductsService.getProducts({
    _select: "brand",
    _distinct: true,
    _order_a: "brand",
  });

  brands.value = response.data?.map((b) => {
    return { label: b.brand.toUpperCase(), value: b.brand };
  });
}

function closeModal() {
  _show.value = false;
  clearFormData();
}

function clearFormData() {
  invoiceForm.value = {};
}

async function loadPurchaseOrders(props) {
  ordersLoading.value = true;

  try {
    const filters = {};
    filters.brand = invoiceForm.value.brand.value;

    orderList.value = await PurchaseOrdersService.getPurchaseInvoiceOrders(
      filters
    );
  } catch (error) {
    console.log(error);
  }
  ordersLoading.value = false;
}
</script>
