<template>
  <q-dialog
    v-model="showPurchaseOrder"
    full-width
    position="top"
    @hide="$emit('close')"
  >
    <q-card v-if="purchaseOrder">
      <q-card-section class="row">
        <div class="title-style">Pedido de Compra</div>
        <q-space />
        <q-btn
          icon="close"
          flat
          round
          dense
          @click="showPurchaseOrder = false"
        />
      </q-card-section>
      <q-card-section class="row q-pt-none">
        <div class="q-mb-md col-md-12">
          <q-stepper
            v-model="step"
            ref="stepper"
            color="secondary"
            flat
            animated
            done-color="green"
            active-color="secondary"
            inactive-color="grey"
          >
            <q-step
              :name="1"
              title="Rascunho"
              :caption="format(purchaseOrder.created, 'datetime')"
              icon="edit_square"
              :done="step >= 1"
            />

            <q-step
              :name="2"
              title="Aprovado"
              :caption="
                purchaseOrder.approved &&
                format(purchaseOrder.approved, 'datetime')
              "
              icon="verified"
              :done="step > 2"
            />

            <q-step
              :name="3"
              title="Solicitado"
              :caption="
                purchaseOrder.requested &&
                format(purchaseOrder.requested, 'datetime')
              "
              icon="shopping_cart_checkout"
              :done="step > 3"
            />
            <q-step
              :name="4"
              title="Confirmado"
              :caption="
                purchaseOrder.requested &&
                format(purchaseOrder.confirmed, 'datetime')
              "
              icon="currency_exchange"
              :done="step > 4"
            />
            <q-step
              :name="5"
              title="Recebendo"
              :caption="
                purchaseOrder.requested &&
                format(purchaseOrder.received, 'datetime')
              "
              icon="local_shipping"
              :done="step > 5"
            />
            <q-step
              :name="6"
              title="Finalizado"
              icon="check_circle"
              :done="step === 6"
            />
            <q-step
              :name="7"
              title="Cancelado"
              icon="cancel"
              :caption="
                purchaseOrder.cancelled &&
                format(purchaseOrder.cancelled, 'datetime')
              "
              v-if="purchaseOrder.status === 'cancelled'"
            />
          </q-stepper>
          <q-separator color="gray-5 q-my-sm" />
        </div>

        <div class="row q-gutter-x-md">
          <div class="q-mb-sm" v-if="handleVisible()">
            <q-icon name="code" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Código: {{ purchaseOrder.code ? purchaseOrder.code : "-" }}</span
            >
          </div>
          <div class="q-mb-sm" v-if="purchaseOrder.proforma_code">
            <q-icon name="description" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Código Proforma: {{ purchaseOrder.proforma_code }}</span
            >
          </div>
          <div class="q-mb-sm">
            <q-icon name="watch" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Marca: {{ purchaseOrder.brand }}</span
            >
          </div>
          <div class="q-mb-sm">
            <q-icon name="person" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Responsável: {{ purchaseOrder.owner }}</span
            >
          </div>

          <div class="q-mb-sm" v-if="purchaseOrder.approver">
            <q-icon name="person" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Aprovador: {{ purchaseOrder.approver }}</span
            >
          </div>

          <div class="q-mb-sm" v-if="purchaseOrder.requester">
            <q-icon name="person" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Solicitante: {{ purchaseOrder.requester }}</span
            >
          </div>

          <div class="q-mb-sm" v-if="purchaseOrder.canceller">
            <q-icon name="person" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Cancelador: {{ purchaseOrder.canceller }}</span
            >
          </div>

          <div class="q-mb-sm">
            <q-icon name="construction" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Quantidade de peças:
              {{ format(purchaseOrder.requested_items, "int") }}</span
            >
          </div>
          <div class="q-mb-sm">
            <q-icon name="add_shopping_cart" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Quantidade Total:
              {{ format(purchaseOrder.requested_quantity, "int") }}</span
            >
          </div>
          <div class="q-mb-sm">
            <q-icon name="savings" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Custo Total: R$
              {{ format(purchaseOrder.total_cost, "number") }}</span
            >
          </div>
          <div class="q-mb-sm" v-if="purchaseOrder.mode == 'Algoritimo'">
            <q-icon name="calendar_month" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Janela da análise: {{purchaseOrder.first_period}} até {{ purchaseOrder.last_period }}</span
            >
          </div>
        </div>
        <q-space />
      </q-card-section>
      <q-card-section class="q-pa-none">
        <div class="row justify-end">
          <q-input
            v-model="filter"
            dense
            outlined
            stack-label
            color="grey-7"
            type="search"
            label="Código/nome"
            class="q-pr-md wt-border"
            debounce="300"
            style="width: 250px"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </div>
      </q-card-section>
      <q-card-section>
        <app-table
          v-model:pagination="purchaseOrderItemsPagination"
          :columns="purchaseOrderItemsColumns"
          :rows="purchaseOrder.items"
          row-key="id"
          :loading="loadingPurchaseOrder"
          :filter="filter"
          dense
        >
        </app-table>
      </q-card-section>
      <q-card-section class="row q-gutter-sm">
        <template v-if="purchaseOrder.status == 'draft'">
          <q-space />
          <q-btn
            v-if="purchaseOrder.mode != 'Algoritimo'"
            color="secondary"
            icon="add_circle"
            label="Novo Item"
            @click="newItem"
            unelevated
            class="wt-border"
          >
            <q-tooltip>Adicionar um novo item</q-tooltip>
          </q-btn>
          <q-btn
            v-if="purchaseOrder.mode == 'Algoritimo'"
            color="primary"
            icon="file_download"
            label="BAIXAR ALGORÍTIMO GERADO"
            unelevated
            class="wt-border"
            download
            @click="getUploadedFile(purchaseOrder.forecast_file, 'alg')"
            :disable="!purchaseOrder.forecast_file"
          >
            <q-tooltip>Baixar Pedido de Compra</q-tooltip>
          </q-btn>
          <div>
            <q-btn
              v-if="purchaseOrder.mode != 'Algoritimo'"
              color="blue"
              icon="add_circle"
              label="Importar Items"
              @click="openFileSelector"
              unelevated
              class="wt-border"
            >
              <q-tooltip>Importar items através de um XLS</q-tooltip>
            </q-btn>

            <input
            v-if="purchaseOrder.mode != 'Algoritimo'"
              type="file"
              ref="fileInput"
              style="display: none"
              accept=".xls,.xlsx"
              @change="onFileAdded"
            />
            <q-btn
              v-if="purchaseOrder.mode == 'Algoritimo'"
              color="blue"
              icon="add_circle"
              label="IMPORTAR ALGORITIMO TRATADO"
              @click="openFileSelector"
              unelevated
              class="wt-border"
            >
              <q-tooltip>Importar excel Algoritimo tratado</q-tooltip>
            </q-btn>

            <input
            v-if="purchaseOrder.mode == 'Algoritimo'"
              type="file"
              ref="fileInput"
              style="display: none"
              accept=".xls,.xlsx"
              @change="onFileAdded"
            />
          </div>

          <q-btn
            color="red"
            icon="delete"
            label="Excluir"
            unelevated
            class="wt-border"
            @click="removeProductDialog = true"
          >
            <q-tooltip>Excluir Pedido de Compra</q-tooltip>
          </q-btn>
          <q-btn
            color="green"
            icon="done"
            label="Aprovar"
            unelevated
            class="wt-border"
            @click="approveDialog = true"
            :disable="purchaseOrder && !purchaseOrder.items.length"
          >
            <q-tooltip>Aprovar Pedido de Compra</q-tooltip>
          </q-btn>
        </template>

        <template v-if="purchaseOrder.status == 'requested'">
          <q-space />
          <q-btn
            color="red"
            icon="cancel"
            label="Cancelar"
            unelevated
            class="wt-border"
            @click="cancelDialog = true"
          >
            <q-tooltip>Cancelar pedido de compra</q-tooltip>
          </q-btn>
        </template>

        <template v-if="purchaseOrder.status == 'approved'">
          <q-space />
          <q-btn
            color="secondary"
            icon="arrow_back"
            label="Retornar a Rascunho"
            unelevated
            class="wt-border"
            @click="draftReturnDialog = true"
          >
            <q-tooltip>Retornar Pedido de Compra para Rascunho</q-tooltip>
          </q-btn>
          <q-btn
            color="primary"
            icon="file_download"
            label="XLS"
            unelevated
            class="wt-border"
            :href="purchaseOrder.file_url"
            download
            @click="getUploadedFile(purchaseOrder.excel_url, 'xls')"
            :disable="!purchaseOrder.excel_url"
          >
            <q-tooltip>Baixar Pedido de Compra</q-tooltip>
          </q-btn>
          <q-btn
            color="green"
            icon="done"
            label="Confirmar Solicitação"
            unelevated
            class="wt-border"
            @click="showRequest = true"
          >
            <q-tooltip>Confirmar Solicitação do Pedido de Compra</q-tooltip>
          </q-btn>
        </template>

        <template
          v-if="
            purchaseOrder.status == 'confirmed' ||
            purchaseOrder.status == 'receiving' ||
            purchaseOrder.status == 'finished'
          "
        >
          <q-space />
          <q-btn
            v-if="purchaseOrder.proforma_url"
            color="primary"
            icon="file_download"
            label="Proforma"
            unelevated
            class="wt-border"
            download
            @click="getUploadedFile(purchaseOrder.proforma_url, 'pdf')"
          >
            <q-tooltip>Baixar Proforma</q-tooltip>
          </q-btn>
          <q-btn
            v-if="purchaseOrder.cambio_url"
            color="primary"
            icon="file_download"
            label="Contrato"
            unelevated
            class="wt-border"
            download
            @click="getUploadedFile(purchaseOrder.cambio_url, 'cambio')"
          >
            <q-tooltip>Baixar Contrato</q-tooltip>
          </q-btn>
        </template>
      </q-card-section>
    </q-card>
  </q-dialog>

  <modal-dialog
    title="Pedidos de Compra"
    v-model="approveDialog"
    message="Aprovar pedido de compra?"
    @confirm="approvePurchaseOrder"
  />

  <modal-dialog
    title="Cancelar pedido de compra"
    v-model="cancelDialog"
    message="Você desejar cancelar o pedido de compra?"
    @confirm="cancelPurchaseOrder"
  />

  <modal-dialog
    title="Retornar para rascunho"
    v-model="draftReturnDialog"
    message="Você quer retornar o pedido de compra para rascunho?"
    @confirm="draftPurchaseOrder"
  />

  <modal-dialog
    title="Excluir item"
    v-model="removeProductItemDialog"
    :message="`Confirma remoção do item ${selectedProduct?.row?.product_name}?`"
    @confirm="removeItem"
    @close="resetState"
  />

  <modal-dialog
    title="Excluir"
    mode
    v-model="removeProductDialog"
    message="Você desejar remover o pedido de compra?"
    @confirm="removePurchaseOrder"
  />

  <purchase-order-item
    v-model:show="showItem"
    v-model:item="purchaseOrderItem"
    :brand="purchaseOrder?.brand"
    @confirm="confirmItem"
  />

  <purchase-order-request
    v-model:show="showRequest"
    v-model="purchaseOrder"
    @confirm="requestPurchaseOrder"
  />

  <error-dialog 
  :showErrorDialog="isDialogVisible"
  :errors="errors"
  @close-dialog="handleCloseDialog"
  >
  </error-dialog>

</template>

<script setup>
import { computed, ref } from "vue";
import { useQuasar } from "quasar";
import AppTable from "../../components/app-table.vue";
import PurchaseOrdersService from "../../services/PurchaseOrdersService";
import { STATUSES } from "../../types/PurchaseOrder";
import { format } from "../../functions";
import PurchaseOrderItem from "./PurchaseOrderItem.vue";
import PurchaseOrderRequest from "./PurchaseOrderRequest.vue";
import ModalDialog from "../../components/modal-dialog.vue";
import AuthService from "@/services/AuthService";
import axios from "axios";
import ErrorDialog from '../../types/ErrorDialog.vue'

const props = defineProps(["show", "purchaseOrderId"]);
const emit = defineEmits(["update:show", "close",'close-dialog']);

const $q = useQuasar();
const purchaseOrder = ref();
const approveDialog = ref(false);
const cancelDialog = ref(false);
const draftReturnDialog = ref(false);
const removeProductItemDialog = ref(false);
const removeProductDialog = ref(false);
const selectedProduct = ref();
const currentUser = computed(() => AuthService.user);
const fileInput = ref();
const proformaCode = ref();
const cambioCode = ref();
const filter = ref("");
const fileInputCambio = ref();
const errors = ref([]);
const isDialogVisible = ref(false)


async function getStep() {
  const statusIndex = STATUSES.find(
    (s) => s.value == purchaseOrder.value.status
  )?.label;

  const steps = {
    Rascunho: 1,
    Aprovado: 2,
    Solicitado: 3,
    Confirmado: 4,
    Recebendo: 5,
    Finalizado: 6,
    Cancelado: 7,
  };

  step.value = steps[statusIndex];
}

const handleVisible = () => {
  const draft = step.value === 1;
  const approved = step.value === 2;

  if (draft || approved) {
    return false;
  }

  return true;
};

const purchaseOrderActiveItems = computed(() =>
  purchaseOrder.value.items.filter((i) => i.status == "active")
);
const purchaseOrderItem = ref();
const loadingPurchaseOrder = ref(false);
const purchaseOrderItemsPagination = ref({
  page: 1,
  rowsPerPage: 50,
});
const showPurchaseOrder = computed({
  get() {
    if (props.show) loadPurchaseOrder();
    return props.show;
  },
  set(value) {
    emit("update:show", value);
  },
});
const showItem = ref(false);
const step = ref(1);
const showRequest = ref(false);

const purchaseOrderItemsColumns = computed(() => {
  const columns = [];
  if (purchaseOrder.value) {
    columns.push({
      name: "product_code",
      required: true,
      label: "Código",
      align: "left",
      field: "product_code",
      sortable: true,
      "sort-method": (a, b) =>
        a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" }),
    });
    columns.push({
      name: "product_category",
      align: "left",
      label: "Categoria",
      field: "product_category",
      type: "text",
    });
    columns.push({
      name: "product_name",
      align: "left",
      label: "Nome",
      field: "product_name",
      type: "text",
    });
    if (purchaseOrder.value.mode == "OS") {
      columns.push({
        name: "OS",
        align: "left",
        label: "OS",
        field: "OS",
        type: "info",
      });
    }
    columns.push({
      name: "status",
      align: "left",
      label: "Situação",
      field: "status",
      type: "label",
      options: [
        { label: "Ativo", value: "active" },
        { label: "Cancelado", value: "cancelled" },
      ],
    });
    columns.push({
      name: "requested_quantity",
      align: "right",
      label: "Solicitado",
      field: "requested_quantity",
      type: "number",
      sortable: true,
    });
    columns.push({
      name: "received_quantity",
      align: "right",
      label: "Recebido",
      field: "received_quantity",
      type: "number",
      sortable: true,
    });
    columns.push({
      name: "invoiced_quantity",
      align: "right",
      label: "Confirmado",
      field: "invoiced_quantity",
      type: "number",
      sortable: true,
    });
    columns.push({
      name: "product_cost",
      align: "right",
      label: "Custo Unitário",
      field: "product_cost",
      type: "number",
      sortable: true,
    });
    columns.push({
      name: "total_cost",
      align: "right",
      label: "Custo Total",
      field: "total_cost",
      type: "number",
    });
    if (purchaseOrder.value.status == "draft") {
      columns.push({
        name: "actions",
        align: "right",
        type: "actions",
        actions: [
          {
            icon: "edit",
            color: "dark",
            toolTip: "Modificar item",
            action: (props) => {
              editItem(props);
            },
          },
          {
            icon: "delete",
            color: "red",
            toolTip: "Remover item",
            action: (props) => {
              openRemoveDialog(props);
            },
          },
        ],
      });
    } else if (purchaseOrder.value.status == "requested") {
      columns.push({
        name: "actions",
        align: "right",
        type: "actions",
        actions: [
          {
            icon: "edit",
            color: "dark",
            toolTip: "Modificar item",
            action: (props) => {
              editItem(props);
            },
          },
        ],
      });
    }
  }
  return columns;
});

async function loadPurchaseOrder() {
  if (props.purchaseOrderId) {
    loadingPurchaseOrder.value = true;
    try {
      purchaseOrder.value = await PurchaseOrdersService.getPurchaseOrderById(
        props.purchaseOrderId
      );
      getStep();
    } catch (error) {}
    loadingPurchaseOrder.value = false;
  } else {
    purchaseOrder.value = null;
  }
}

async function newItem() {
  purchaseOrderItem.value = {};
  showItem.value = true;
}

async function editItem(props) {
  const indexItem = purchaseOrder.value.items.indexOf(props.row);
  purchaseOrderItem.value = purchaseOrder.value.items[indexItem];

  showItem.value = true;
}

async function confirmItem() {
  if (purchaseOrderItem.value) {
    const index = purchaseOrder.value.items.findIndex(
      (item) => item.product_id == purchaseOrderItem.value.product_id
    );
    if (index >= 0) {
      purchaseOrder.value.items[index] = purchaseOrderItem.value;
    } else {
      purchaseOrder.value.items.push(purchaseOrderItem.value);
    }
    purchaseOrder.value = await PurchaseOrdersService.updatePurchaseOrder(
      purchaseOrder.value
    );
    $q.notify({
      message: "Pedido de compra atualizado",
      type: "positive",
      color: "green",
    });
  }
}

async function removeItem() {
  try {
    const indexItem = purchaseOrder.value.items.indexOf(
      selectedProduct.value.row
    );
    purchaseOrder.value.items.splice(indexItem, 1);
    purchaseOrder.value = await PurchaseOrdersService.updatePurchaseOrder(
      purchaseOrder.value
    );

    removeProductItemDialog.value = false;
    $q.notify({
      message: "Item removido",
      type: "positive",
      color: "green",
    });
  } catch (error) {
    $q.notify({
      message: "Erro ao remover o item removido",
      type: "negative",
      color: "danger",
    });
  }
}

async function removePurchaseOrder() {
  try {
    await PurchaseOrdersService.deletePurchaseOrder(purchaseOrder.value.id);
    showPurchaseOrder.value = false;

    removeProductDialog.value = false;
    $q.notify({
      message: "Pedido de compra removido",
      type: "positive",
      color: "green",
    });
  } catch (error) {
    $q.notify({
      message: "Erro ao excluir o pedido de compra",
      type: "negative",
      color: "danger",
    });
  }
}

async function approvePurchaseOrder() {
  try {
    purchaseOrder.value.approver = currentUser.value.name;
    purchaseOrder.value.status = "approved";
    purchaseOrder.value.approved = new Date().toISOString();
    purchaseOrder.value = await PurchaseOrdersService.updatePurchaseOrder(
      purchaseOrder.value
    );
    showPurchaseOrder.value = false;
    approveDialog.value = false;

    $q.notify({
      message: "Pedido de compra aprovado",
      type: "positive",
      color: "green",
    });
  } catch (error) {
    $q.notify({
      message: "Erro ao aprovar o pedido de compra",
      type: "negative",
      color: "danger",
    });
  }
}

async function cancelPurchaseOrder() {
  try {
    purchaseOrder.value.canceller = currentUser.value.name;
    purchaseOrder.value.status = "cancelled";
    purchaseOrder.value.cancelled = new Date().toISOString();
    purchaseOrder.value = await PurchaseOrdersService.updatePurchaseOrder(
      purchaseOrder.value
    );
    showPurchaseOrder.value = false;
    cancelDialog.value = false;

    $q.notify({
      message: "Pedido de compra cancelado",
      type: "positive",
      color: "green",
    });
  } catch (error) {
    $q.notify({
      message: "Erro ao cancelar o pedido de compra",
      type: "negative",
      color: "danger",
    });
  }
}

async function draftPurchaseOrder() {
  try {
    purchaseOrder.value.status = "draft";
    purchaseOrder.value.approved = null;
    purchaseOrder.value = await PurchaseOrdersService.updatePurchaseOrder(
      purchaseOrder.value
    );
    showPurchaseOrder.value = false;
    draftReturnDialog.value = false;

    $q.notify({
      message: "Pedido de compra retornado para rascunho",
      type: "positive",
      color: "green",
    });
  } catch (error) {
    $q.notify({
      message: "Erro ao retornar para rascunho",
      type: "negative",
      color: "danger",
    });
  }
}

async function requestPurchaseOrder() {
  emit("update:show", false);
}

function openRemoveDialog(props) {
  selectedProduct.value = props;
  removeProductItemDialog.value = true;
}


function resetState() {
  selectedProduct.value = {};
}

function downloadFile(file) {
  var blob = new Blob([file], { type: "application/pdf" });
  var url = window.URL.createObjectURL(blob);

  var a = document.createElement("a");
  a.href = url;
  a.download = "proforma.pdf";

  document.body.appendChild(a);
  window.open(url);
  a.click();

  setTimeout(function () {
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }, 0);
}

async function getUploadedFile(fileId, fileType) {
  const url = `https://app.watchtime.com.br/api/resources/${fileId}/stream`;
  axios
    .get(url, {
      responseType: "blob",
    })
    .then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      if (fileType === "xls") {
        link.setAttribute("download", "pedido.xlsx");
      }
      if (fileType === "cambio") {
        link.setAttribute("download", "contrato cambio.pdf");
      }
      if (fileType === "pdf") {
        link.setAttribute("download", "proforma.pdf");
      }      if (fileType === "alg") {
        link.setAttribute("download", `Algoritimo ${purchaseOrder.value.brand}.xlsx`);
      }

      document.body.appendChild(link);
      link.click();
    });
  $q.notify({
    message: "Download efetuado com sucesso",
    type: "positive",
    color: "green",
  });
}

async function updatePurchaseOrderProforma(proformaId) {
  try {
    purchaseOrder.value.proforma_url = proformaId;
    purchaseOrder.value = await PurchaseOrdersService.updatePurchaseOrder(
      purchaseOrder.value
    ).then(() => {
      loadPurchaseOrder();
    });
  } catch (error) {
    console.error(error);
  }
}

async function updatePurchaseOrderCambio(cambioId) {
  try {
    purchaseOrder.value.cambio_url = cambioId;
    purchaseOrder.value = await PurchaseOrdersService.updatePurchaseOrder(
      purchaseOrder.value
    ).then(() => {
      loadPurchaseOrder();
    });
  } catch (error) {
    console.error(error);
  }
}

function handleCloseDialog(){
  isDialogVisible.value = false;
}

async function handleUploadFile() {
  try {
    const file = fileInput.value;
    const formdata = new FormData();
    formdata.append("file", file);

    const response = await PurchaseOrdersService.uploadFiles(formdata);

    await updatePurchaseOrderProforma(response.id);
    fileInput.value = null;

    $q.notify({
      message: "Upload proforma efetuada com sucesso.",
      type: "positive",
      color: "green",
    });
  } catch {
    $q.notify({
      message: "Erro ao realizar o upload proforma",
      type: "negative",
      color: "danger",
    });
  }
}

async function handleUploadFileCambio() {
  try {
    const file = fileInputCambio.value;
    const formdata = new FormData();
    formdata.append("file", file);
    const id = purchaseOrder.value.id;

    const response = await PurchaseOrdersService.ImportExcel(formdata, id);
    console.log(response);

    $q.notify({
      message: "Arquivo importado com sucesso.",
      type: "positive",
      color: "green",
    });
  } catch {
    $q.notify({
      message: "Erro ao importar arquivo.",
      type: "negative",
      color: "danger",
    });
  } finally {
    loadPurchaseOrder();
  }
}

async function importXls() {
  try {
  const file = fileInput.value;
  const formdata = new FormData();
  formdata.append("file", file);
  const id = purchaseOrder.value.id;
  console.log('teste')
  const response = await PurchaseOrdersService.ImportExcel(formdata, id);
  console.log(response);


  if (response[0].status === 'success') {
    $q.notify({
      message: response[0].message,
      type: "positive",
      color: "green",
    });
  } else if (response[0].status === 'warning') {
    response[0].problem = 'Não cadastrado no Cockpit',
    errors.value = response[0].message,
    isDialogVisible.value = true;

  } else if (response[0].status === 'error') {
    $q.notify({
      message: response[0].message,
      type: "negative",
      color: "danger",
    });
  }

} catch (error) {
  console.log(error);
  $q.notify({
    message: "Erro ao importar arquivo.",
    type: "negative",
    color: "danger",
  });
} finally {
  loadPurchaseOrder();
}
}



function openFileSelector() {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = ".xls, .xlsx";

  input.addEventListener("change", () => {
    fileInput.value = input.files[0];
    importXls();
  });

  input.click();
}
</script>

<style lang="scss">
.info-container {
  background: #e6e6f091;
  padding: 8px;
  border-radius: 8px;
  margin-right: 8px;
}

.q-stepper__tab {
  padding: 8px 0px !important;
}

.upload-wrapper {
  border: 1px solid $grey;
  border-radius: 9px;
}

.spacing {
  margin-top: 6px;
}

.downloadLink {
  cursor: pointer;
  color: $primary;
  font-weight: 500;
  align-self: center;
}
</style>
