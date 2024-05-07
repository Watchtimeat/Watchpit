<template>
  <app-table
    ref="tableRef"
    :pagination="pagination"
    :columns="columns"
    :rows="products"
    row-key="id"
    class="q-pa-md wt-border"
    :loading="loading"
    @request="loadProducts"
    :filter="search"
    flat
  >
    <template v-slot:top>
      <div class="row full-width q-mb-lg">
        <div class="title-style">Vendas</div>
        <q-space />
        <q-select
          label="Filtrar por marca"
          outlined
          input-debounce="0"
          :options="brandsFiltered"
          v-model="search.brand"
          @filter="filterBrand"
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
          label="Código ou nome"
          debounce="300"
          class="q-pr-md wt-border"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        <q-btn
          :loading="isLoading"
          color="primary"
          class="wt-border q-mr-md"
          label="Importar Produtos"
          unelevated
          @click="updateProducts('I')"
        />
        <q-btn
          :loading="isLoadingD"
          color="teal"
          class="wt-border q-mr-md"
          unelevated
          label="Atualizar Descrições"
          @click="updateProducts('D')"
        />
        <q-btn
          :loading="isLoadingP"
          color="green"
          class="wt-border"
          unelevated
          label="Atualizar Preços"
          @click="updateProducts('P')"
        />
      </div>
    </template>
  </app-table>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useQuasar } from "quasar";
import ProductsService from "../../../services/ProductsService";
import AppTable from "../../../components/app-table.vue";
import axios from "axios";
import { QSpinnerGears } from "quasar";
const $q = useQuasar();

const text = ref("");
const cost = ref(null);
const name = ref("");
const category = ref("");
const brand = ref("");
const search = ref({
  text: "",
  brand: null,
});
const tableRef = ref();
const products = ref([]);
const product = ref({});
const loading = ref(false);
const pagination = ref({ rowsPerPage: 50, page: 1, rowsNumber: 0 });
const brands = ref([]);
const brandsFiltered = ref([]);
const isLoadingP = ref(false);
const isLoadingD = ref(false);
const isLoading = ref(false);
QSpinnerGears;

onMounted(() => {
  loadBrands();
});

const columns = [
  {
    name: "code",
    align: "left",
    label: "Código",
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
    name: "category",
    align: "left",
    label: "Categoria",
    field: "category",
    type: "text",
    sortable: true,
  },
  {
    name: "name",
    align: "left",
    label: "Nome",
    field: "name",
    type: "text",
    sortable: true,
  },
  {
    name: "cost",
    align: "left",
    label: "Custo",
    field: "cost",
    type: "number",
    sortable: true,
  },
];

const form = [
  { name: "code", label: "Código *", field: "code", type: "text" },
  { name: "brand", label: "Marca *", field: "brand", type: "text" },
  { name: "category", label: "Categoria", field: "category", type: "text" },
  { name: "name", label: "Nome *", field: "name", type: "text" },
  {
    name: "cost",
    label: "Custo *",
    field: "cost",
    type: "text",
    mask: "############",
  },
];

onMounted(() => {
  tableRef.value.requestServerInteraction();
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

async function loadProducts(props) {
  const { page, rowsPerPage, sortBy, descending } = props.pagination || {};
  const filter = props.filter;

  loading.value = true;
  try {
    const filters = {};
    if (filter.brand) {
      filters["brand.lk"] = props.filter.brand.value;
    }

    if (filter.text) {
      filters["code.lk,name.lk"] = props.filter.text;
    }

    if (rowsPerPage) filters._limit = rowsPerPage;
    if (page) filters._offset = (page - 1) * rowsPerPage;
    if (sortBy && !descending) filters._order_a = sortBy;
    if (sortBy && descending) filters._order_d = sortBy;

    const { data, rows } = await ProductsService.getProducts(filters);

    products.value.splice(0, products.value.length, ...data);
    pagination.value = {
      sortBy: sortBy,
      descending: descending,
      page: page,
      rowsPerPage: rowsPerPage,
      rowsNumber: rows,
    };
  } catch (error) {}
  loading.value = false;
}

async function updateProducts(type) {
  let response;
  try {
    if (type === "I") {
      isLoading.value = true;
      response = await axios.get(
        "https://app.watchtime.com.br/api/estoklus/products_importation"
      );
    } else if (type === "P") {
      isLoadingP.value = true;
      response = await axios.patch(
        "https://app.watchtime.com.br/api/estoklus/products_cost"
      );
    } else if (type === "D") {
      isLoadingD.value = true;
      response = await axios.patch(
        "https://app.watchtime.com.br/api/estoklus/products_name"
      );
    }

    const message = response.data;

    if (message === 0) {
      $q.notify({
        color: "warning",
        message: "Não existem produtos à serem atualizados",
      });
    } else {
      $q.notify({
        color: "positive",
        message: "Produtos importados com sucesso.",
      });
    }
  } catch (error) {
    console.error("Erro na atualização dos produtos:", error);
  } finally {
    isLoading.value = false;
    isLoadingP.value = false;
    isLoadingD.value = false;
  }
}
</script>
