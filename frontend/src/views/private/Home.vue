<template>
  <div class="q-px-sm">
    <div class="q-py-lg row justify-between items-center">
      <p class="title-style q-ma-none">Bem vindo(a), {{ currentUser.name }}!</p>
      <div class="col-3">
        <q-select
          label="Filtrar por marca"
          outlined
          input-debounce="0"
          :options="brandsFiltered"
          @filter="filterBrand"
          v-model="search"
          stack-label
          use-input
          dense
          color="grey-7"
          class="q-mr-md wt-border"
        />
      </div>
    </div>

    <div class="section-status">
      <q-card flat class="wt-border">
        <q-card-section class="title-style"
          >Pedidos de Compra
          {{ search.label !== "-" ? `- ${search.label}` : "" }}</q-card-section
        >
        <q-card-section>
          <chart-purchase-status
            :summaryStatus="filteredSummary"
            :orderDetails="orderDetails"
          />
        </q-card-section>
      </q-card>
      <q-card flat class="wt-border">
        <q-card-section class="title-style"
          >Invoices
          {{ search.label !== "-" ? `- ${search.label}` : "" }}</q-card-section
        >
        <q-card-section>
          <chart-invoice-status
            :invoiceSummary="invoiceSummary"
            :invoicingDetails="invoicingDetails"
          />
        </q-card-section>
      </q-card>
      <q-card flat class="wt-border">
        <q-card-section class="title-style">
          Total Pedidos por Marca
        </q-card-section>
        <q-card-section>
          <chart-purchase-by-brand
            :brandLabels="getBrandLabels()"
            :brandValues="getBrandValues()"
            v-if="summaryByBrand"
          />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>
<script>
import ChartPurchaseStatus from "@/components/Home/ChartPurchaseStatus.vue";
import ChartPurchaseByBrand from "@/components/Home/ChartPurchaseByBrand.vue";
import ChartInvoiceStatus from "@/components/Home/ChartInvoiceStatus.vue";
import ProductsService from "@/services/ProductsService";
import PurchaseOrdersService from "@/services/PurchaseOrdersService";
import PurchaseInvoicesService from "@/services/PurchaseInvoicesService";
import AuthService from "@/services/AuthService";

export default {
  props: ["summary"],
  components: {
    ChartInvoiceStatus,
    ChartPurchaseStatus,
    ChartPurchaseByBrand,
  },
  data() {
    return {
      search: { label: "-", value: "-" },
      brands: [],
      brandsFiltered: [],
      summary: {},
      summaryByBrand: null,
      invoiceSummary: {
        requested: 0,
        receiving: 0,
        received: 0,
        cancelled: 0,
      },
      filters: {},
      user: {},
      invoicingDetails: {
        requested: [],
        receiving: [],
        cancelled: [],
      },
      orderDetails: {
        draft: [],
        approved: [],
        requested: [],
        confirmed: [],
        receiving: [],
        finished: [],
      },
    };
  },
  watch: {
    search(newValue) {
      if (newValue.value === "-") {
        delete this.filters.brand;
        this.loadPurchaseOrders();
        this.loadPurchaseInvoices();
      } else {
        this.filters.brand = newValue.value;
        this.loadPurchaseOrders();
        this.loadPurchaseInvoices();
      }
    },
  },

  mounted() {
    this.loadBrands();
    this.loadPurchaseOrders();
    this.loadPurchaseByBrand();
    this.loadStatusDetails();
    this.loadPurchaseInvoices();
    this.loadStatusInvoicing();
  },
  computed: {
    filteredSummary() {
      return this.summary;
    },
    currentUser() {
      return AuthService.user;
    },
  },
  methods: {
    async loadPurchaseByBrand() {
      this.summaryByBrand =
        await PurchaseOrdersService.getPurchaseOrdersSummary("brand");
    },
    getBrandLabels() {
      return Object.keys(this.summaryByBrand);
    },
    getBrandValues() {
      return Object.values(this.summaryByBrand);
    },
    async loadBrands() {
      const response = await ProductsService.getProducts({
        _select: "brand",
        _distinct: true,
        _order_a: "brand",
      });

      this.brands = response.data?.map((b) => {
        return { label: b.brand.toUpperCase(), value: b.brand };
      });
    },
    filterBrand(val, update) {
      if (val === "") {
        update(() => {
          this.brandsFiltered = this.brands;
        });
        return;
      }

      update(() => {
        this.brandsFiltered = this.brands.filter(
          (brand) => brand.label.toLowerCase().indexOf(val.toLowerCase()) > -1
        );
      });
    },
    async loadStatusInvoicing() {
      this.invoicingDetails.requested =
        await PurchaseInvoicesService.getPurchaseInvoicesSummary("brand", {
          status: "requested",
        });

      this.invoicingDetails.receiving =
        await PurchaseInvoicesService.getPurchaseInvoicesSummary("brand", {
          status: "receiving",
        });

      this.invoicingDetails.cancelled =
        await PurchaseInvoicesService.getPurchaseInvoicesSummary("brand", {
          status: "cancelled",
        });
    },
    async loadStatusDetails() {
      this.orderDetails.draft =
        await PurchaseOrdersService.getPurchaseOrdersSummary("brand", {
          status: "draft",
        });

      this.orderDetails.approved =
        await PurchaseOrdersService.getPurchaseOrdersSummary("brand", {
          status: "approved",
        });

      this.orderDetails.requested =
        await PurchaseOrdersService.getPurchaseOrdersSummary("brand", {
          status: "requested",
        });

      this.orderDetails.confirmed =
        await PurchaseOrdersService.getPurchaseOrdersSummary("brand", {
          status: "confirmed",
        });

      this.orderDetails.receiving =
        await PurchaseOrdersService.getPurchaseOrdersSummary("brand", {
          status: "receiving",
        });

      this.orderDetails.finished =
        await PurchaseOrdersService.getPurchaseOrdersSummary("brand", {
          status: "finished",
        });
    },
    async loadPurchaseOrders() {
      try {
        if (this.filters) {
          this.summary = await PurchaseOrdersService.getPurchaseOrdersSummary(
            "status",
            this.filters
          );
        } else {
          this.summary = await PurchaseOrdersService.getPurchaseOrdersSummary(
            "status"
          );
        }
      } catch (error) {}
    },
    async loadPurchaseInvoices() {
      if (this.filters) {
        this.invoiceSummary =
          await PurchaseInvoicesService.getPurchaseInvoicesSummary(
            "status",
            this.filters
          );
      } else {
        this.invoiceSummary =
          await PurchaseInvoicesService.getPurchaseInvoicesSummary("status");
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.section-status {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;

  @media screen and (max-width: 720px) {
    grid-template-columns: 1fr;
  }
}
</style>
