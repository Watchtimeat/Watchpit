<template>
  <app-table
    ref="invoicesRef"
    :pagination="pagination"
    :columns="columns"
    :rows="rows"
    row-key="id"
    no-data-label="Não há dados disponíveis"
    class="q-pa-md wt-border"
    flat
    :loading="loading"
    @request="loadPurchaseInvoices"
    :filter="search"
  >
    <template v-slot:top>
      <div class="row full-width q-mb-lg">
        <div class="title-style">Invoices</div>
        <q-space />
        <q-select
          label="Filtrar por marca"
          outlined
          input-debounce="0"
          :options="brandsFiltered"
          @filter="filterBrand"
          v-model="search.brand"
          stack-label
          use-input
          dense
          color="grey-7"
          class="q-mr-md wt-border"
        />
        <q-input
          v-model="search.text"
          dense
          outlined
          color="grey-7"
          type="search"
          label="Código/Responsável"
          class="q-pr-md"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        <q-btn
          size="md"
          color="green"
          icon="add_circle"
          unelevated
          class="wt-border"
          label="Nova Proforma"
          @click="newPurchaseInvoice"
        >
          <q-tooltip>Adicionar uma nova proforma</q-tooltip>
        </q-btn>
      </div>

      <div class="row q-my-md overflow-auto">
        <q-tabs
          inline-label
          v-model="statusFilter"
          @update:model-value="statusSelected"
          class="text-dark q-mb-md"
          indicator-color="grey"
          active-color="black"
          no-caps
        >
          <q-tab
            v-for="status in statusToggle"
            :key="status.name"
            :name="status.value"
            :icon="getStatusIcon(status.value)"
            :label="status.label"
            :class="status.value"
          >
          </q-tab
        ></q-tabs>
      </div>
    </template>
  </app-table>

  <modal-form
    title="Finalizar invoice"
    v-model:show="finishInvoiceDialog"
    @confirm="finishInvoiceForm"
  >
    <q-form @submit.prevent="finishInvoiceForm" class="q-gutter-md">
      <q-input
        outlined
        stack-label
        label="Número da NF"
        lazy-rules="ondemand"
        type="number"
        color="grey-7"
        v-model="finishInvoiceFields.nf_number" />

      <q-input
        outlined
        stack-label
        label="Número DI / DIR"
        lazy-rules="ondemand"
        type="text"
        color="grey-7"
        v-model="finishInvoiceFields.customs_number" />

      <q-input
        outlined
        stack-label
        label="Valor NF"
        lazy-rules="ondemand"
        type="cost"
        color="grey-7"
        v-model="finishInvoiceFields.nf_value" />

      <q-input
        outlined
        stack-label
        label="Data NF"
        lazy-rules="ondemand"
        type="date"
        color="grey-7"
        v-model="finishInvoiceFields.nf_date" />

      <div class="row">
        <div class="col">
          <q-file
            outlined
            bottom-slots
            v-model="fileInput.nota_fiscal"
            label="Upload nota fiscal"
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
                @click.stop.prevent="fileInput.nota_fiscal = null"
                class="cursor-pointer"
              />
            </template>
          </q-file>
        </div>

        <div class="row items-center">
          <q-btn
            v-if="
              !finishInvoiceFields?.nota_fiscal_file_id && fileInput.nota_fiscal
            "
            color="secondary"
            class="wt-border q-ml-md"
            style="height: 40px"
            @click="handleUploadFile('nota_fiscal')"
          >
            <q-icon name="done" />
          </q-btn>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <q-file
            outlined
            bottom-slots
            v-model="fileInput.fatura"
            label="Upload fatura"
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
                @click.stop.prevent="fileInput.fatura = null"
                class="cursor-pointer"
              />
            </template>
          </q-file>
        </div>

        <div class="row items-center">
          <q-btn
            v-if="!finishInvoiceFields?.fatura_file_id && fileInput.fatura"
            color="secondary"
            class="wt-border q-ml-md"
            style="height: 40px"
            @click="handleUploadFile('fatura')"
          >
            <q-icon name="done" />
          </q-btn>
        </div>
      </div>

      <div class="row">
        <q-btn
          label="Finalizar"
          type="submit"
          class="full-width wt-border"
          color="dark"
          :disabled="
            !finishInvoiceFields.nf_number ||
            !finishInvoiceFields.nf_value ||
            !finishInvoiceFields.customs_number ||
            !finishInvoiceFields.fatura_file_id ||
            !finishInvoiceFields.nota_fiscal_file_id
          "
        /></div
    ></q-form>
  </modal-form>

  <modal-form
    title="Receber invoice"
    v-model:show="receiveInvoiceDialog"
    @confirm="receiveInvoiceForm"
  >
    <q-form @submit.prevent="receiveInvoiceForm" class="q-gutter-md">
      <q-input
        outlined
        stack-label
        label="Código da invoice*"
        lazy-rules="ondemand"
        type="text"
        color="grey-7"
        v-model="receiveInvoiceFields.code" />

      <q-input
        outlined
        stack-label
        label="Tracking*"
        lazy-rules="ondemand"
        type="text"
        color="grey-7"
        v-model="receiveInvoiceFields.tracking" />

      <q-input
        outlined
        stack-label
        label="Data da invoice*"
        lazy-rules="ondemand"
        type="date"
        color="grey-7"
        v-model="receiveInvoiceFields.invoice_date" />

      <div class="row">
        <div class="col">
          <q-file
            outlined
            bottom-slots
            v-model="fileInput.awb"
            label="Upload AWB"
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
                @click.stop.prevent="fileInput.awb = null"
                class="cursor-pointer"
              />
            </template>
          </q-file>
        </div>

        <div class="row items-center">
          <q-btn
            v-if="!receiveInvoiceFields?.awb_file_id && fileInput.awb"
            color="secondary"
            class="wt-border q-ml-md"
            style="height: 40px"
            @click="handleUploadFile('awb')"
          >
            <q-icon name="done" />
          </q-btn>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <q-file
            outlined
            bottom-slots
            v-model="fileInput.invoice"
            label="Upload invoice"
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
                @click.stop.prevent="fileInput.invoice = null"
                class="cursor-pointer"
              />
            </template>
          </q-file>
        </div>

        <div class="row items-center">
          <q-btn
            v-if="!receiveInvoiceFields?.invoice_file_id && fileInput.invoice"
            color="secondary"
            class="wt-border q-ml-md"
            style="height: 40px"
            @click="handleUploadFile('invoice')"
          >
            <q-icon name="done" />
          </q-btn>
        </div>
      </div>

      <div class="row">
        <q-btn
          label="Receber"
          type="submit"
          class="full-width wt-border"
          color="dark"
          :disabled="
            !receiveInvoiceFields.code ||
            !receiveInvoiceFields.tracking ||
            !receiveInvoiceFields.invoice_date ||
            !receiveInvoiceFields.awb_file_id ||
            !receiveInvoiceFields.invoice_file_id
          "
        /></div
    ></q-form>
  </modal-form>

  <modal-form
    title="Lançar Pagamento"
    v-model:show="requestInvoiceDialog"
    @confirm="requestInvoiceForm"
  >
    <q-form @submit.prevent="requestInvoiceForm" class="q-gutter-md">
      <q-input
        outlined
        stack-label
        label="Código do contrato*"
        lazy-rules="ondemand"
        type="text"
        color="grey-7"
        v-model="requestInvoiceFields.cambio_code" />

      <q-input
        outlined
        stack-label
        label="Data do pagamento*"
        lazy-rules="ondemand"
        type="date"
        color="grey-7"
        v-model="requestInvoiceFields.payment_date" />

      <div class="row">
        <div class="col">
          <q-file
            outlined
            bottom-slots
            v-model="fileInput.cambio"
            label="Upload Contrato"
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
                @click.stop.prevent="fileInput.cambio = null"
                class="cursor-pointer"
              />
            </template>
          </q-file>
        </div>

        <div class="row items-center">
          <q-btn
            v-if="!requestInvoiceFields?.cambio_file_id && fileInput.cambio"
            color="secondary"
            class="wt-border q-ml-md"
            style="height: 40px"
            @click="handleUploadFile('cambio')"
          >
            <q-icon name="done" />
          </q-btn>
        </div>
      </div>

      <div class="row">
        <q-btn
          label="Gravar"
          type="submit"
          class="full-width wt-border"
          color="dark"
          :disabled="
            !requestInvoiceFields.cambio_code ||
            !requestInvoiceFields.cambio_file_id
          "
        /></div
    ></q-form>
  </modal-form>



  <modal-dialog
    title="Cancelar"
    mode
    v-model="cancelInvoiceDialog"
    :message="`Você deseja cancelar a invoice ${selectedInvoice.proforma_code}?`"
    @confirm="cancelInvoice"
  />

  <purchase-invoice
    v-model:show="showPurchaseInvoice"
    :id="id"
    :dataPurchaseInvoice="dataPurchaseInvoice"
    @close="purchaseInvoiceClosed"
  />

  <details-invoice
    v-model:show="showDetailsInvoice"
    :data="detailsInvoiceData"
    @close="closeShowDetailsInvoice"
  />
</template>

<script setup>
import { computed, ref, onMounted, watch } from "vue";
import { useQuasar } from "quasar";
import AppTable from "../../components/app-table.vue";
import PurchaseInvoice from "./PurchaseInvoice.vue";
import DetailsInvoice from "@/components/Invoice/DetailsInvoice.vue";
import PurchaseInvoicesService from "../../services/PurchaseInvoicesService";
import { STATUSES } from "../../types/PurchaseInvoices";
import ModalForm from "../../components/modal-form.vue";
import ModalDialog from "../../components/modal-dialog.vue";
import ProductsService from "@/services/ProductsService";
import PurchaseOrdersService from "@/services/PurchaseOrdersService";

const $q = useQuasar();
const search = ref({
  text: "",
  brand: null,
});
const invoicesRef = ref();
const loading = ref(false);
const rows = ref([]);
const requestInvoiceDialog = ref(false);
const finishInvoiceDialog = ref(false);
const receiveInvoiceDialog = ref(false);
const pagination = ref({ rowsPerPage: 50, page: 1 });
const summary = ref([]);
const id = ref(null);
const dataPurchaseInvoice = ref(null);
const showPurchaseInvoice = ref(false);
const showDetailsInvoice = ref(false);
const detailsInvoiceData = ref(null);
const requestInvoiceFields = ref({});
const finishInvoiceFields = ref({});
const receiveInvoiceFields = ref({});
const selectedInvoice = ref({});
const cancelInvoiceDialog = ref(false);
const brands = ref([]);
const brandsFiltered = ref([]);
const statusFilter = ref(null);
const fileInput = ref({});

const columns = [
  {
    name: "code",
    align: "left",
    label: "Código da invoice",
    field: "code",
    type: "text",
    sortable: true,
  },
  {
    name: "brand",
    align: "left",
    label: "Marca",
    field: "brand",
    type: "text",
    sortable: true,
  },
  {
    name: "owner",
    align: "left",
    label: "Responsável",
    field: "owner",
    type: "text",
    sortable: true,
  },
  {
    name: "createdAt",
    align: "left",
    label: "Criada Em",
    field: "createdAt",
    type: "datetime",
    sortable: true,
  },
  {
    name: "total_quantity",
    align: "left",
    label: "Quantidade",
    field: "total_quantity",
    type: "int",
    sortable: true,
  },
  {
    name: "total_cost",
    align: "left",
    label: "Custo",
    field: "total_cost",
    type: "number",
    sortable: true,
  },
  {
    name: "actions",
    align: "center",
    type: "actions",
    actions: [],
  },
];

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

watch(statusFilter, () => {
  const itemColum = columns.find((colum) => colum.name === "actions");
  if (statusFilter.value === "requested") {
    itemColum.actions = [
      {
        icon: "visibility",
        color: "dark",
        toolTip: "Visualizar invoice",
        action: (props) => {
          openDetailsInvoice(props);
        },
      },

      {
        icon: "local_shipping",
        color: "teal",
        toolTip: "Receber invoice",
        action: (props) => {
          openReceiveInvoiceDialog(props);
        },
      },
      {
        icon: "delete",
        color: "red",
        toolTip: "Cancelar invoice",
        action: (props) => {
          openCancelInvoiceDialog(props);
        },
      },      
    ];
  }

  if (statusFilter.value === "receiving") {
    itemColum.actions = [
      {
        icon: "visibility",
        color: "dark",
        toolTip: "Visualizar invoice",
        action: (props) => {
          openDetailsInvoice(props);
        },
      },
      {
        icon: "check",
        color: "green",
        toolTip: "Finalizar invoice",
        action: (props) => {
          openFinishInvoiceDialog(props);
        },
      },
      {
        icon: "delete",
        color: "red",
        toolTip: "Cancelar invoice",
        action: (props) => {
          openCancelInvoiceDialog(props);
        },
      },
    ];
  }

  if (statusFilter.value === "received") {
    itemColum.actions = [
      {
        icon: "visibility",
        color: "dark",
        toolTip: "Visualizar invoice",
        action: (props) => {
          openDetailsInvoice(props);
        },
      },
    ];
  }

  if (statusFilter.value === "cancelled") {
    itemColum.actions = [];
  }

  if (statusFilter.value === "created") {
    itemColum.actions = [
      {
        icon: "visibility",
        color: "dark",
        toolTip: "Visualizar invoice",
        action: (props) => {
          openDetailsInvoice(props);
        },
      },
      {
        icon: "currency_exchange",
        color: "dark",
        toolTip: "Lançar Pagamento",
        action: (props) => {
          openRequestedInvoiceDialog(props);
        },
      },{
        icon: "delete",
        color: "red",
        toolTip: "Cancelar invoice",
        action: (props) => {
          openCancelInvoiceDialog(props);
        },
      },
    ];
  }
});

function openFinishInvoiceDialog(props) {
  selectedInvoice.value = props.row;
  finishInvoiceDialog.value = true;
  finishInvoiceFields.value = {};
  fileInput.value = {};
}

function openReceiveInvoiceDialog(props) {
  selectedInvoice.value = props.row;
  receiveInvoiceDialog.value = true;
  receiveInvoiceFields.value = {};
  fileInput.value = {};
}

  function openRequestedInvoiceDialog(props) {
  selectedInvoice.value = props.row;
  requestInvoiceDialog.value = true;
  requestInvoiceFields.value = {};
  fileInput.value = {};
}


function openCancelInvoiceDialog(props) {
  selectedInvoice.value = props.row;
  cancelInvoiceDialog.value = true;
}

async function cancelInvoice() {
  selectedInvoice.value.status = "cancelled";
  await PurchaseInvoicesService.updatePurchaseInvoice(
    selectedInvoice.value
  ).then(() => {
    invoicesRef.value.requestServerInteraction();
    $q.notify({
      message: "Invoice atualizada",
      type: "positive",
      color: "green",
    });
  });
}

async function finishInvoiceForm() {
  selectedInvoice.value.status = "received";
  selectedInvoice.value.nf_date = finishInvoiceFields.value.nf_date;
  selectedInvoice.value.customs_number =
    finishInvoiceFields.value.customs_number;
  selectedInvoice.value.nf_number = finishInvoiceFields.value.nf_number;
  selectedInvoice.value.nf_value = finishInvoiceFields.value.nf_value;
  selectedInvoice.value.fatura_file_id =
    finishInvoiceFields.value.fatura_file_id;
  selectedInvoice.value.nota_fiscal_file_id =
    finishInvoiceFields.value.nota_fiscal_file_id;

  await PurchaseInvoicesService.updatePurchaseInvoice(
    selectedInvoice.value
  ).then(() => {
    invoicesRef.value.requestServerInteraction();
    $q.notify({
      message: "Invoice atualizada",
      type: "positive",
      color: "green",
    });
    finishInvoiceFields.value = {};
    finishInvoiceDialog.value = false;
  });
}

async function receiveInvoiceForm() {
  selectedInvoice.value.status = "receiving";
  selectedInvoice.value.code = receiveInvoiceFields.value.code;
  selectedInvoice.value.tracking = receiveInvoiceFields.value.tracking;
  selectedInvoice.value.invoice_date = receiveInvoiceFields.value.invoice_date;
  selectedInvoice.value.awb_file_id = receiveInvoiceFields.value.awb_file_id;
  selectedInvoice.value.invoice_file_id =
    receiveInvoiceFields.value.invoice_file_id;

  await PurchaseInvoicesService.updatePurchaseInvoice(
    selectedInvoice.value
  ).then(() => {
    invoicesRef.value.requestServerInteraction();
    $q.notify({
      message: "Invoice atualizada",
      type: "positive",
      color: "green",
    });
    receiveInvoiceFields.value = {};
    receiveInvoiceDialog.value = false;
    
  });
}

async function requestInvoiceForm() {
  selectedInvoice.value.status = "requested";
  selectedInvoice.value.cambio_code = requestInvoiceFields.value.cambio_code;
  selectedInvoice.value.cambio_file_id = requestInvoiceFields.value.cambio_file_id;
  selectedInvoice.value.payment_date = requestInvoiceFields.value.payment_date;
  await PurchaseInvoicesService.updatePurchaseInvoice(
    selectedInvoice.value
  ).then(() => {
    invoicesRef.value.requestServerInteraction();
    $q.notify({
      message: "Invoice atualizada",
      type: "positive",
      color: "green",
    });
    requestInvoiceFields.value = {};
    requestInvoiceDialog.value = false;
  });
}

const statusToggle = computed(() => {
  const options = [];
  for (let status of STATUSES) {
    const number = summary.value[status.value];
    options.push({
      value: status.value,
      label: status.label + " (" + (number ?? 0) + ")",
      slot: "default",
      summary: number,
    });
  }
  return options;
});

function getStatusIcon(status) {
  const icons = {
    requested: "currency_exchange",
    receiving: "local_shipping",
    received: "check_circle",
    cancelled: "cancel",
    created: "edit_square"
  };

  return icons[status];
}

onMounted(() => {
  invoicesRef.value.requestServerInteraction();
});

onMounted(() => {
  loadBrands();
});

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

function statusSelected() {
  invoicesRef.value.requestServerInteraction();
}

function purchaseInvoiceClosed() {
  invoicesRef.value.requestServerInteraction();
}

async function loadPurchaseInvoices(props) {
  const { page, rowsPerPage, sortBy, descending } = props.pagination;

  loading.value = true;
  try {
    if (!statusFilter.value) statusFilter.value = STATUSES[0].value;
    const filters = {};

    if (props.filter.brand) {
      filters["brand.lk"] = props.filter.brand.value;
    }

    if (props.filter.text) {
      filters["proforma_code.lk,owner.lk"] = props.filter.text;
    }

    if (statusFilter.value) filters.status = statusFilter.value;
    if (rowsPerPage) filters._limit = rowsPerPage;
    if (page) filters._offset = (page - 1) * rowsPerPage;
    if (sortBy && !descending) filters._order_a = sortBy;
    if (sortBy && descending) filters._order_d = sortBy;
    summary.value = await PurchaseInvoicesService.getPurchaseInvoicesSummary(
      "status"
    );
    const invoices = await PurchaseInvoicesService.getPurchaseInvoices(filters);
    rows.value = invoices.data;
    pagination.value = {
      sortBy: sortBy,
      descending: descending,
      page: page,
      rowsPerPage: rowsPerPage,
      rowsNumber: invoices.rows,
    };
  } catch (error) {}
  loading.value = false;
}

function openDetailsInvoice(props) {
  showDetailsInvoice.value = true;
  detailsInvoiceData.value = props.row;
}
function closeShowDetailsInvoice() {
  showDetailsInvoice.value = false;
}

function newPurchaseInvoice() {
  id.value = null;
  dataPurchaseInvoice.value = null;
  showPurchaseInvoice.value = true;
}

function editPurchaseInvoice(props) {
  id.value = props.key;
  showPurchaseInvoice.value = true;
  dataPurchaseInvoice.value = props.row;
}

async function handleUploadFile(fileType) {
  try {
    let file;

    if (fileType === "fatura") {
      file = fileInput.value.fatura;
    } else if (fileType === "nota_fiscal") {
      file = fileInput.value.nota_fiscal;
    } else if (fileType === "awb") {
      file = fileInput.value.awb;
    } else if (fileType === "invoice") {
      file = fileInput.value.invoice;
    }
    else if (fileType === "cambio") {
      file = fileInput.value.cambio;
    }


    const formdata = new FormData();
    formdata.append("file", file);

    const response = await PurchaseOrdersService.uploadFiles(formdata);

    if (fileType === "fatura") {
      finishInvoiceFields.value.fatura_file_id = response.id;
    } else if (fileType === "nota_fiscal") {
      finishInvoiceFields.value.nota_fiscal_file_id = response.id;
    } else if (fileType === "awb") {
      receiveInvoiceFields.value.awb_file_id = response.id;
    } else if (fileType === "invoice") {
      receiveInvoiceFields.value.invoice_file_id = response.id;
    } else if (fileType === "cambio") {
      requestInvoiceFields.value.cambio_file_id = response.id;
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

<style lang="scss">
.received {
  color: #555567;
  i {
    color: $green-6;
  }
}

.receiving {
  color: #555567;
  i {
    color: teal;
  }
}

.cancelled {
  color: #555567;
  i {
    color: red;
  }
}

.requested {
  color: #555567;
  i {
    color: $primary;
  }
}
</style>
