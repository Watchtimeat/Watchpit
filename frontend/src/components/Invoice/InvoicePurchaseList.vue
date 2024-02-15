<template>
  <div class="full-width">

    <q-list
      bordered
      separator
      class="wt-border"
      v-if="purchaseList && purchaseList?.length"
    >
      <q-item
        clickable
        v-ripple
        v-for="(item, index) in purchaseList"
        :key="index"
        @click="handleSelectPurchase(item)"
        :active="purchaseSelected.id === item.id"
        active-class="bg-teal-4 text-white item-active"
      >
        <q-item-section class="text-weight-medium">
          #{{ item.code || "-" }}
        </q-item-section>
        <q-item-section>
          <div>
            <span class="text-weight-medium">Data solicitação:</span>
            {{ format(item.requested, "date") || "-" }}
          </div>
        </q-item-section>
        <q-item-section>
          <div>
            <span class="text-weight-medium">Quantidade solicitada:</span>
            {{ item.requested_quantity || "-" }}
          </div>
        </q-item-section>
        <q-item-section>
          <div>
            <span class="text-weight-medium">Custo total:</span>
            {{ format(item.total_cost, "currency") || "-" }}
          </div>
        </q-item-section>
        <q-item-section>
          <div>
            <span class="text-weight-medium">Itens selecionados:</span>
            {{
              newInvoicingData.orders.find((order) => order.id === item.id)
                ?.items?.length || 0
            }}
          </div>
        </q-item-section>
        <q-item-section side>
          <q-icon name="visibility" />
        </q-item-section>
      </q-item>
    </q-list>

    <q-card class="q-pa-md wt-border no-shadow not-found-purchase" v-else>
      <div class="row items-center q-gutter-sm">
        <q-icon name="warning" size="sm" />
        <div>Não há pedidos disponíveis para gerar uma invoice.</div>
      </div>
    </q-card>

    <div class="q-mt-md" v-if="purchaseSelected.id">
      <div class="row overflow-auto">
        <q-tabs
          v-model="tab"
          class="text-dark q-mb-md"
          indicator-color="grey"
          active-color="black"
          inline-label
          no-caps
        >
          <q-tab label="Itens do Pedido" name="one" />
          <q-tab label="Itens selecionados" name="two" >
            <q-badge color="orange" floating>CHF: {{SelectedValue}}</q-badge>
            </q-tab>
        </q-tabs>
      </div>



      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="one">
          <div class="col">
            <selection-items-table
              class="q-mt-sm"
              :itemsList="purchaseItems"
              v-model:itemsSelected="itemsInvoicingSelected.items"
              selection="multiple"
              :columns="columnsTable.columns"
              :pagination="pagination"
            />
          </div>
        </q-tab-panel>

        <q-tab-panel name="two">
          <div class="col">
            <span class="text-weight-medium"> Itens selecionados</span>
            <selection-items-table
              class="q-mt-sm"
              :itemsList="itemsInvoicingSelected.items"
              :columns="columnsTable.columnsWithActionRemove"
              dense
              :pagination="pagination"
            />
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>

    <div class="row q-mt-md">
      <q-file
        outlined
        dense
        bottom-slots
        v-model="fileInput.proforma"
        label="Upload Proforma"
        accept=".pdf"
        color="grey-7"
        class="wt-border q-pb-none"
      >
        <template v-slot:prepend>
          <q-icon name="attach_file" />
        </template>

        <template v-slot:append>
          <q-icon
            name="close"
            @click.stop.prevent="fileInput.proforma = null"
            class="cursor-pointer"
          />
        </template>
      </q-file>

      <q-btn
        v-if="!proforma_file_id && fileInput.proforma"
        color="secondary"
        class="wt-border q-ml-md"
        style="height: 40px"
        @click="handleUploadFile('proforma')"
      >
        <q-icon name="done" />
      </q-btn>

      <q-space />
      <q-btn
        color="green"
        icon="done"
        label="Criar invoice"
        unelevated
        class="wt-border"
        @click="handleCreateInvoice"
        :disabled="
          isDisabledButton ||
          !props.invoiceForm.proforma_code ||
          props.invoiceForm.proforma_code?.length === 0 ||

          !proforma_file_id 

        "
      >
        <q-tooltip>Criar invoice</q-tooltip>
      </q-btn>
    </div>

    <q-dialog title="Finalizar invoice" v-model="editInvoiceDialog">
      <q-card class="q-py-md q-px-md wt-border" style="width: 450px">
        <q-form @submit.prevent="editItemPurchase" class="q-gutter-md">
          <h5 class="title-style">Editar item</h5>
          <q-input
            outlined
            stack-label
            label="Quantidade"
            type="number"
            step="any"
            color="grey-7"
            v-model="dataEditInvoice.quantity" />

          <q-input
            outlined
            stack-label
            label="Valor"
            type="number"
            color="grey-7"
            step="any"
            v-model="dataEditInvoice.cost" />

          <div class="row">
            <q-btn
              label="Finalizar"
              type="submit"
              class="full-width wt-border"
              color="dark"
            /></div></q-form
      ></q-card>
    </q-dialog>
  </div>


</template>

<script setup>
import { ref, watch } from "vue";
import { format } from "@/functions";
import { columns } from "./constants";
import SelectionItemsTable from "./SelectionItemsTable.vue";
import PurchaseOrdersService from "../../services/PurchaseOrdersService";
import PurchaseInvoicesService from "../../services/PurchaseInvoicesService";
import { useQuasar } from "quasar";

const pagination = ref({ rowsPerPage: 50 });
const $q = useQuasar();
const emit = defineEmits(["close"]);
const props = defineProps(["purchaseList", "invoiceForm", "closeModal"]);
const tab = ref("one");
const editInvoiceDialog = ref(false);
const dataEditInvoice = ref({});
const invoiceItemKeySelected = ref(null);
const columnsWithActionRemove = [
  ...columns,
  {
    name: "actions",
    align: "right",
    type: "actions",
    action: [
      {
        icon: "edit",
        color: "dark",
        toolTip: "Modificar pedido",
        action: (props) => {
          handleEditPurchase(props.key);
        },
      },
      {
        icon: "delete",
        color: "red",
        toolTip: "Remover item",
        action: (props) => {
          handleRemoveItemPurchase(props.key);
        },
      },
    ],
  },
];
const columnsTable = {
  columns,
  columnsWithActionRemove,
};
const purchaseSelected = ref({});
const purchaseItems = ref([]);
const itemsInvoicingSelected = ref({});
const newInvoicingData = ref({
  orders: [],
});
const isDisabledButton = ref(true);
const fileInput = ref({});
const proforma_file_id = ref();
const cambio_file_id = ref();
const invoicingDataMapped = ref([]);
const SelectedValue = ref(0)

watch(purchaseSelected, (state) => {
  itemsInvoicingSelected.value = newInvoicingData.value.orders.find(
    (order) => order.id === state.id
  );
});

watch(newInvoicingData.value, () => {
  isDisabledButton.value =
    newInvoicingData.value.orders.filter((order) => order.items.length > 0)
      .length === 0;
      SelectedValue.value = 0
      newInvoicingData.value.orders.forEach((order) => {
        order.items.forEach((item) => {
          SelectedValue.value += item.total_cost
        });
});
SelectedValue.value = SelectedValue.value.toFixed(2);
});

const handleEditPurchase = (itemKey) => {
  editInvoiceDialog.value = true;
  invoiceItemKeySelected.value = itemKey;

  const positionItemSelected = newInvoicingData.value.orders.findIndex(
    (order) => order.id === purchaseSelected.value.id
  );

  const orderItem = newInvoicingData.value.orders[
    positionItemSelected
  ].items.find((item) => item.id === itemKey);

  dataEditInvoice.value.quantity = orderItem.requested_quantity;
  dataEditInvoice.value.cost = orderItem.product_cost;
};

const editItemPurchase = () => {
  const positionItemSelected = newInvoicingData.value.orders.findIndex(
    (order) => order.id === purchaseSelected.value.id
  );

  const orderItem = newInvoicingData.value.orders[
    positionItemSelected
  ].items.find((item) => item.id === invoiceItemKeySelected.value);

  orderItem.invoiced_quantity = Number(dataEditInvoice.value.quantity);
  orderItem.product_cost = Number(dataEditInvoice.value.cost);
  orderItem.total_cost = orderItem.product_cost * orderItem.invoiced_quantity;

  editInvoiceDialog.value = false;
  invoiceItemKeySelected.value = null;
};

const handleRemoveItemPurchase = (itemKey) => {
  const positionItemSelected = newInvoicingData.value.orders.findIndex(
    (order) => order.id === purchaseSelected.value.id
  );

  newInvoicingData.value.orders[positionItemSelected].items = [
    ...newInvoicingData.value.orders[positionItemSelected].items.filter(
      (item) => item.id !== itemKey
    ),
  ];
};

const handleSelectPurchase = (orderSelected) => {
  purchaseSelected.value = orderSelected;
  loadPurchaseOrder(orderSelected.id);

  const orderWasNotSelected = !newInvoicingData.value.orders.find(
    (order) => order.id === orderSelected.id
  );

  if (orderWasNotSelected) {
    newInvoicingData.value.orders = [
      ...newInvoicingData.value.orders,
      {
        id: orderSelected.id,
        code: orderSelected.code,
        items: [],
      },
    ];
  }
};

async function loadPurchaseOrder(purchaseId) {
  try {
    const response = await PurchaseOrdersService.getPurchaseOrderInvoiceById(
      purchaseId
    );

    purchaseItems.value = response.items;
  } catch (error) {}
}

async function handleCreateInvoice() {
  invoicingDataMapped.value = newInvoicingData.value.orders.filter(
    (order) => order.items.length > 0
  );

  const payload = {
    brand: props.invoiceForm.brand.value,
    proforma_code: props.invoiceForm.proforma_code,
    order: invoicingDataMapped.value,
    status: "created",
    createdAt: new Date().toISOString(),
    proforma_file_id: proforma_file_id.value,
  };

  try {
    await PurchaseInvoicesService.addPurchaseInvoice(payload);
    props.closeModal();
    $q.notify({
      message: "Invoice criada com sucesso",
      type: "positive",
      color: "green",
    });
  } catch (error) {
    $q.notify({
      message: "Erro ao criar uma nova invoice",
      type: "negative",
      color: "danger",
    });
  }
}

async function handleUploadFile(fileType) {
  try {
    let file;

    if (fileType === "cambio") {
      file = fileInput.value.cambio;
    } else {
      file = fileInput.value.proforma;
    }

    const formdata = new FormData();
    formdata.append("file", file);

    const response = await PurchaseOrdersService.uploadFiles(formdata);

    if (fileType === "cambio") {
      cambio_file_id.value = response.id;
    } else {
      proforma_file_id.value = response.id;
    }

    $q.notify({
      message: `Upload ${fileType} efetuada com sucesso.`,
      type: "positive",
      color: "green",
    });
  } catch {
    $q.notify({
      message: `Erro ao realizar o upload ${fileType}`,
      type: "negative",
      color: "danger",
    });
  }
}
</script>

<style scoped lang="scss">
.not-found-purchase {
  border: 1px solid $grey;
}

.transfer-btn {
  align-self: center;
}

.item-active {
  div {
    color: white;
  }
}
</style>
