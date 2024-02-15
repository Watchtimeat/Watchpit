<template>
  <app-table
    ref="purchaseOrdersRef"
    :pagination="purchaseOrdersPagination"
    :columns="columns"
    :rows="purchaseOrders"
    row-key="id"
    class="q-pa-md"
    :loading="loadingPurchaseOrders"
    @request="loadPurchaseOrders"
    :filter="search"
    :total-cost="totalCost"
  >
    <template v-slot:top>
      <div class="row full-width q-mb-lg">
        <div class="title-style">Pedidos de Compra</div>
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
          stack-label
          color="grey-7"
          type="search"
          label="Responsável ou modo"
          class="q-pr-md wt-border"
          debounce="300"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        <q-input
          v-model="search.code"
          dense
          outlined
          stack-label
          color="grey-7"
          type="search"
          label="Código"
          class="q-pr-md wt-border"
          debounce="300"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        <q-btn
          color="primary"
          unelevated
          style="border-radius: 8px"
          icon="search"
          @click="openSearch"
          class="q-mr-md wt-border"
        >
          <q-tooltip>Pesquisa de Peças</q-tooltip>
        </q-btn>
        <q-btn
          color="green"
          unelevated
          style="border-radius: 8px"
          icon="add_circle"
          label="Novo Pedido"
          @click="newPurchaseOrder"
          class="q-pr-md wt-border"
        >
          <q-tooltip>Adicionar um novo pedido de compra</q-tooltip>
        </q-btn>

      </div>
      <div class="row q-my-md overflow-auto">
        <q-tabs
          inline-label
          v-model="statusFilter"
          @update:model-value="selectedStatus"
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
          </q-tab>
        </q-tabs>
      </div>
    </template>
  </app-table>

  <modal-form
    title="Novo Pedido"
    v-model:show="showPlanner"
    @confirm="confirmPlanner"
  >
    <q-form @submit.prevent="confirmPlanner" class="q-gutter-md">
      <div>
        <q-radio
          class="q-mr-md"
          v-model="planner.mode"
          color="teal"
          val="manual"
          label="Manual"
          @update:model-value="clearSelectedBrands"
        />
        <q-radio
          class="q-mr-md"
          v-model="planner.mode"
          color="teal"
          val="OS"
          label="Ordem de Serviço"
          @update:model-value="clearSelectedBrands"
        />
        <q-radio
          v-model="planner.mode"
          color="teal"
          val="planned"
          label="Planejamento"
          @update:model-value="clearSelectedBrands"
        />
      </div>

      <div v-if="planner.mode && planner.mode != 'OS'">
        <q-select
          label="Marcas"
          outlined
          input-debounce="0"
          :options="brandsFilteredNewPurchase"
          v-model="planner.brands"
          @filter="filterBrandNewPurchase"
          multiple
          counter
          use-chips
          stack-label
          use-input
          :hint="
            planner.brands.length > 1
              ? `Itens selecionados`
              : `Item selecionado`
          "
          color="grey-7"
        >
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey">Sem opções</q-item-section>
            </q-item>
          </template>

          <template v-slot:selected-item="scope">
            <q-chip
              removable
              @remove="scope.removeAtIndex(scope.index)"
              :tabindex="scope.tabindex"
              color="secondary"
              text-color="white"
            >
              {{ scope.opt.label }}
            </q-chip>
          </template>
        </q-select>
      </div>

      <div v-if="planner.mode && planner.mode == 'OS'">
        <q-select
          label="Marcas"
          outlined
          input-debounce="0"
          :options="brandsByOsFilteredNewPurchase"
          v-model="planner.brands"
          @filter="filterBrandByOsNewPurchase"
          stack-label
          use-input
          color="grey-7"
        >
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey">Sem opções</q-item-section>
            </q-item>
          </template>

          <template v-slot:selected-item="scope">
            {{ scope.opt.label }}
          </template>
        </q-select>
      </div>

      <div v-if="planner.mode === 'planned'">
        <q-input
          label="Meses à serem planejados"
          stack-label
          class="q-mb-md"
          outlined
          step="any"
          type="number"
          v-model.number="planner.windowSize"
          color="grey-7"
          :rules="[positiveNumberRule]"
        />
        <q-input
          outlined
          stack-label
          label="Início da Janela de Análise"
          lazy-rules="ondemand"
          type="month"
          v-model="planner.plannedMonth"
          color="grey-7"
        />

        <q-input
          outlined
          stack-label
          class="q-mb-md q-mt-sm"
          label="Fim da Janela de Análise"
          lazy-rules="ondemand"
          type="month"
          v-model="planner.lastMonth"
          color="grey-7"
        />


      </div>

      <div class="row">
        <q-btn
          type="submit"
          class="full-width wt-border"
          color="dark"
          label="Confirmar"
          :loading="creatingPurchaseOrder"
          :disable="
            (planner.mode != 'OS' && !planner.brands.length) ||
            (planner.mode == 'OS' && !planner.brands.value)
          "
        />
      </div>
    </q-form>
  </modal-form>

  <purchase-order
    v-model:show="showPurchaseOrder"
    :purchase-order-id="purchaseOrderId"
    @close="purchaseOrderClosed"
  />

  <modal-dialog
    v-model:show="pesquisaopen"
  />

</template>
<script setup>
import { computed, onMounted, ref } from "vue";
import { useQuasar } from "quasar";
import PurchaseOrdersService from "../../services/PurchaseOrdersService";
import ProductsService from "../../services/ProductsService";
import AppTable from "../../components/app-table.vue";
import PurchaseOrder from "./PurchaseOrder.vue";
import { STATUSES } from "../../types/PurchaseOrder";
import { autoCapitalize } from "@/functions.js";
import ModalForm from "../../components/modal-form.vue";
import ModalDialog from "../../components/modal-dialog-search.vue";
import AuthService from "@/services/AuthService";

const currentUser = computed(() => AuthService.user);

const $q = useQuasar();

const positiveNumberRule = (value) => {
  if (!value || isNaN(value) || value <= 0) {
    return "Insira um número positivo";
  }
  return true;
};

const search = ref({
  text: "",
  brand: null,
  code: "",
});
const purchaseOrdersRef = ref();
const loadingPurchaseOrders = ref(false);
const creatingPurchaseOrder = ref(false);
const purchaseOrdersSummary = ref({});
const purchaseOrders = ref([]);
const purchaseOrderId = ref();
const brands = ref([]);
const brandsByOs = ref([]);
const statusFilter = ref(null);
const planner = ref({ mode: "", brands: null });
const purchaseOrdersPagination = ref({
  page: 1,
  rowsPerPage: 50,
});
const showPurchaseOrder = ref(false);
const showPlanner = ref(false);
const brandsFiltered = ref([]);
const brandsFilteredNewPurchase = ref([]);
const brandsByOsFilteredNewPurchase = ref([]);
const totalCost = ref(0);
const columns = ref(getColumns(statusFilter))
const pesquisaopen = ref(false)


function filterBrandNewPurchase(val, update) {
  if (val === "") {
    update(() => {
      brandsFilteredNewPurchase.value = brands.value;
    });
    return;
  }

  update(() => {
    brandsFilteredNewPurchase.value = brands.value.filter(
      (brand) => brand.label.toLowerCase().indexOf(val.toLowerCase()) > -1
    );
  });
}

function filterBrandByOsNewPurchase(val, update) {
  if (val === "") {
    update(() => {
      brandsByOsFilteredNewPurchase.value = brandsByOs.value;
    });
    return;
  }

  update(() => {
    brandsByOsFilteredNewPurchase.value = brandsByOs.value.filter(
      (brand) => brand.label.toLowerCase().indexOf(val.toLowerCase()) > -1
    );
  });
}

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

const statusToggle = computed(() => {
  const options = [];
  for (let status of STATUSES) {
    const number = purchaseOrdersSummary.value[status.value];
    if (status.value !== "cancelled" || currentUser.value.administrator) {
      options.push({
        value: status.value,
        label: autoCapitalize(status.label) + " (" + (number ?? 0) + ")",
        slot: "default",
        summary: number,
      });
    }
  }
 
  return options;
});



function getColumns(statusFilter){
  
  const purchaseOrdersColumns = []

  if (statusFilter.value === 'draft' || statusFilter.value === 'approved' || !statusFilter.value){
    purchaseOrdersColumns.push( 
      {
        name: "brand",
        align: "left",
        label: "Marca",
        field: "brand",
        type: "text",
        sortable: true,
      }
     )
  }
  if (statusFilter.value != 'draft' && statusFilter.value != 'approved'){
    purchaseOrdersColumns.push( 
      {
        name: "code",
        align: "left",
        label: "Código",
        field: "code",
        type: "text",
        sortable: true,
      }
     )
  }


purchaseOrdersColumns.push(

  {
    name: "created",
    align: "left",
    label: "Criado em",
    field: "created",
    type: "datetime",
    sortable: true,
  },
  {
    name: "mode",
    align: "left",
    label: "Modo",
    field: "mode",
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
    name: "status",
    align: "center",
    label: "Situação",
    field: "status",
    type: "label",
    color: "red",
    options: STATUSES,
  },
  {
    name: "requested_quantity",
    align: "right",
    label: "Quantidade solicitada",
    field: "requested_quantity",
    type: "int",
    sortable: true,
  },
  {
    name: "received_quantity",
    align: "right",
    label: "Quantidade recebida",
    field: "received_quantity",
    type: "int",
    sortable: true,
  },
  {
    name: "invoiced_quantity",
    align: "right",
    label: "Confirmado",
    field: "invoiced_quantity",
    type: "int",
    sortable: true,
  },
  {
    name: "total_cost",
    align: "right",
    label: "Custo total",
    field: "total_cost",
    type: "number",
    sortable: true,
  },
  {
    name: "actions",
    align: "center",
    type: "actions",
    field: "status",
    sortable: true,
    options: STATUSES,
    actions: [
      {
        color: "dark",
        toolTip: "Visualizar pedido",
        action: (props) => {
          editPurchaseOrder(props);
        },
      },
    ],
  },
);

return purchaseOrdersColumns}

onMounted(() => {
  purchaseOrdersRef.value.requestServerInteraction();
  getBrandsAvaiableByOs();
});

function selectedStatus() {
  purchaseOrdersRef.value.requestServerInteraction();
}

async function loadPurchaseOrders(props) {
  const { page, rowsPerPage, sortBy, descending } = props.pagination;
  loadingPurchaseOrders.value = true;

  columns.value = getColumns(statusFilter);

  try {
    if (brands.value.length == 0) {
      brands.value = (
        await ProductsService.getProducts({
          _select: "brand",
          _distinct: true,
          _order_a: "brand",
        })
      ).data.map((b) => {
        return { label: b.brand.toUpperCase(), value: b.brand };
      });
    }
    if (!statusFilter.value) {
      statusFilter.value = STATUSES[0].value;
    }

    const filters = {};

    if (props.filter.brand) {
      filters["brand.lk"] = props.filter.brand.value;
    }

    if (props.filter.text) {
      filters["mode.lk,owner.lk"] = props.filter.text;
    }
    if (props.filter.code) {
      filters["code.lk"] = `%${props.filter.code}%`;
    }

    if (statusFilter.value) {
      filters.status = statusFilter.value;
    }
    if (rowsPerPage) filters._limit = rowsPerPage;
    if (page) filters._offset = (page - 1) * rowsPerPage;
    if (sortBy && !descending) filters._order_a = sortBy;
    if (sortBy && descending) filters._order_d = sortBy;

    const statusFiltered = structuredClone(filters);
    delete statusFiltered.status;

    purchaseOrdersSummary.value =
      await PurchaseOrdersService.getPurchaseOrdersSummary(
        "status",
        statusFiltered
      );
    const { data, rows } = await PurchaseOrdersService.getPurchaseOrders(
      filters
    );

    purchaseOrders.value = data;
    totalCost.value = purchaseOrders.value.reduce(
      (sum, order) => sum + (order.total_cost || 0),
      0
    );
    purchaseOrdersPagination.value = {
      sortBy: sortBy,
      descending: descending,
      page: page,
      rowsPerPage: rowsPerPage,
      rowsNumber: rows,
    };
  } catch (error) {}
  loadingPurchaseOrders.value = false;
}

async function clearSelectedBrands(selectedType) {
  planner.value = { brands: [], mode: selectedType };
}

function newPurchaseOrder() {
  planner.value = { brands: [], mode: "" };
  showPlanner.value = true;
}



async function getBrandsAvaiableByOs() {
  brandsByOs.value = (
    await PurchaseOrdersService.getBrandListOsOrderAvaiable()
  ).data.map((b) => {
    return {
      label: b.brand.toUpperCase(),
      value: b.brand,
      brand_id: b.brand_id,
    };
  });
}

async function confirmPlanner() {
  if (planner.value.mode == "manual") {
    for (let brand of planner.value.brands) {
      await PurchaseOrdersService.addPurchaseOrder({
        brand: brand.label,
        status: "draft",
        mode: "manual",
        created: new Date().toISOString(),
        items: [],
      }).then(() => {
        $q.notify({
          message: `Pedidos de compra adicionados`,
          type: "positive",
          color: "green",
        });
      });
    }
  } else if  (planner.value.mode == "OS") {
    await PurchaseOrdersService.addPurchaseOrderByOs({
      brand_id: planner.value.brands.brand_id,
      agrupa: "S",
    }).then((response) => {
      if (response.message.indexOf(`nenhum pedido pedido`) != -1) {
        $q.notify({
          message: response.message,
          type: "warning",
          color: "warning",
        });
      } else {
        $q.notify({
          message: response.message,
          type: "positive",
          color: "green",
        });
      }
    });
  } else   if (planner.value.mode == "planned") {
    creatingPurchaseOrder.value = true
    for (let brand of planner.value.brands) {
      await PurchaseOrdersService.addPurchaseOrderByPlanner({
        brand: brand.label,
        status: "draft",
        mode: "Algoritimo",
        first_period:planner.value.plannedMonth,
        last_period:planner.value.lastMonth,
        month_forecast:planner.value.windowSize,
        owner: currentUser.value.name
      }).then(() => {
        creatingPurchaseOrder.value = false
        $q.notify({
          message: `Pedidos de compra adicionados`,
          type: "positive",
          color: "green",
        });
      });
    }
    creatingPurchaseOrder.value = false
  purchaseOrdersRef.value.requestServerInteraction();
  showPlanner.value = false;
}
}

async function editPurchaseOrder(props) {
  purchaseOrderId.value = props.row.id;
  showPurchaseOrder.value = true;
}

function getStatusIcon(status) {
  const icons = {
    draft: "edit_square",
    approved: "verified",
    requested: "shopping_cart_checkout",
    confirmed: "currency_exchange",
    receiving: "local_shipping",
    finished: "check_circle",
    cancelled: "cancel",
  };

  return icons[status];
}

function purchaseOrderClosed() {
  purchaseOrdersRef.value.requestServerInteraction();
}

function openSearch() {
  pesquisaopen.value = true;
}


</script>

<style lang="scss">
.q-table__card {
  box-shadow: none;
  border-radius: 8px;
}

.draft {
  color: #555567;
  i {
    color: grey;
  }
}

.approved {
  color: #555567;
  i {
    color: $green-6;
  }
}

.requested {
  color: #555567;
  i {
    color: $purple-5;
  }
}

.confirmed {
  color: #555567;
  i {
    color: $primary;
  }
}

.receiving {
  color: #555567;
  i {
    color: teal;
  }
}

.finished {
  color: #555567;
  i {
    color: $blue-grey-8;
  }
}

.cancelled {
  color: #555567;
  i {
    color: red;
  }
}
</style>
