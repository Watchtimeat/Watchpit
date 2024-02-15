<template>
  <q-dialog v-model="showDialog">
    <q-card style="min-width: 70%" class="wt-border q-pa-md" >
      <q-card-section class="row items-center q-pa-none">
        <div class="title-style q-pa-none">{{ title }}</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>
      <q-card-section class="fit row wrap justify-center items-start content-start" style="align-self: center">
        <q-table
                      style="height: 25%; width:90%"
                      flat bordered
                      ref="tableRef"
                      :rows="Pedidos"
                      :columns="columnsPedido"
                      :table-colspan="2"
                      virtual-scroll
                      :virtual-scroll-item-size="48"
                      :pagination="pagination"
                      :rows-per-page-options="[0]"
                      class="q-mt-md"
                    >
                    <template v-slot:top-left>
                      <div class="title-style" style=" padding-left: 10px !important;">Pedidos</div>
                      </template>
                    <template v-slot:top-right>
                        <q-input @keydown.enter="fetchDados()" background="blue" dense v-model="filter" placeholder="Pesquisa" class="q-mt-md">
                        </q-input>
                        <q-btn
                        color="red"
                        @click="fetchDados()"
                        class="q-mt-md"
                        icon="search"
                       
                        />
                      </template>
                      <template v-slot:body="props">
                       
        <q-tr :props="Pedidos">
          <q-td>
            {{ props.row.pedido_code }}
          </q-td>
          <q-td>
            {{ props.row.mode }}
          </q-td>
          <q-td>
            {{ props.row.OS }}
          </q-td>
          <q-td>
            {{ props.row.requested_quantity }}
          </q-td>
          <q-td>
            {{ props.row.received_quantity }}
          </q-td>
          <q-td>
            {{ props.row.status }}
          </q-td>
        </q-tr>
      </template>
                    </q-table>
                    <q-table
                      style="height: 25%; width:90%"
                      flat bordered
                      ref="tableRef"
                      :rows="Romaneios"
                      :columns="columnsRomaneio"
                      :table-colspan="2"
                      virtual-scroll
                      :virtual-scroll-item-size="48"
                      :pagination="pagination"
                      :rows-per-page-options="[0]"
                      class="q-mt-md"
                    >
                    <template v-slot:top-left>
                      <div class="title-style" style=" padding-left: 10px !important;">Romaneios</div>
                      </template>
                    <template v-slot:top-right>
                        <q-input  @key.enter="fetchDados()" background="blue" dense v-model="filter" placeholder="Pesquisa" class="q-mt-md">
                        </q-input>
                        <q-btn
                        color="red"
                        @click="fetchDados()"
                        class="q-mt-md"
                        icon="search"
                        />
                      </template>
                      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td>
            {{ props.row.romanio }}
          </q-td>
          <q-td>
            {{ props.row.status_romaneio }}
          </q-td>
          <q-td>
            {{ props.row.OS }}
          </q-td>
          <q-td>
            {{ props.row.quantidade }}
          </q-td>
          <q-td>
            {{ props.row.loja_destino }}
          </q-td>
          <q-td>
            {{ props.row.loja_origem }}
          </q-td>
          <q-td>
            {{ props.row.data_romaneio }}
          </q-td>
        </q-tr>
      </template>
                    </q-table>
                  </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { computed,ref } from "vue";
import { date } from 'quasar';
import axios from "axios";
const props = defineProps(["title", "show"]);
const emit = defineEmits(["update:show", "close"]);
const filter = ref('')
const Pedidos= ref([])
const loading = ref(false)
const columnsPedido = [{ name: 'Pedido', align: 'left', label: 'Pedido', field: 'pedido_code', sortable: true },
{name: 'Tipo', align: 'left', label: 'Tipo', field: 'mode', sortable: true},
{name: 'OS', align: 'left', label: 'OS', type:'text',field: 'OS', sortable: true},
{name: 'requested_quantity', align: 'left', label: 'Qtde. Solicitada', field: 'requested_quantity', sortable: true},
{name: 'received_quantity', align: 'left', label: 'Qtde. Recebida', field: 'received_quantity', sortable: true},
{name: 'status', align: 'left', label: 'Status', field: 'status', sortable: true}]

const columnsRomaneio = [{ name: 'Romaneio', align: 'left', label: 'Romaneio', field: 'romanio', sortable: true },
{name: 'Status', align: 'left', label: 'Status', field: 'status_romaneio', sortable: true},
{name: 'OS', align: 'left', label: 'OS', type:'text',field: 'OS', sortable: true},
{name: 'Quantidade',type:"number", align: 'left', label: 'Quantidade', field: 'quantidade', sortable: true},
{name: 'Destino', align: 'left', label: 'Destino', field: 'loja_destino', sortable: true},
{name: 'Origem', align: 'left', label: 'Origem', field: 'loja_origem', sortable: true},
{name: 'Data', align: 'left', label: 'Data', type:"date" , field: 'data_romaneio', sortable: true}]
const       pagination = {
        rowsPerPage: 0
      }

const userInput = ref(props.text ? props.text : '');
const Romaneios = ref([])
const showDialog = computed({
  get() {
    return props.show;
  },
  set(value) {
    emit("update:show", value);
  },
});

async function confirm() {
  if (props.requireInput) {
    emit("confirm", userInput.value);
  }else{
  emit("confirm");
  }
}

function close() {
  emit("close");
}

const fetchDados = async () => {
  loading.value = true;

  let product = { 'code': filter.value.toUpperCase() };
  
  try {
    const response = await axios.post(
      `https://app.watchtime.com.br/api/purchase_orders/consulta_pedidos`, product
    );
    
    const options = response.data.map(item => ({
      pedido_code: item.pedido_code,
      mode: item.mode,
      OS: item.OS,
      requested_quantity: item.requested_quantity,
      received_quantity: item.received_quantity,
      status: item.status,
    }));

    Pedidos.value = options;
  } catch (err) {
    console.error("Erro ao buscar dados dos pedidos:", err);
  }

  try {
    const response1 = await axios.post(
      `https://app.watchtime.com.br/api/estoklus/consulta_romaneios`, product
    );
    
    const options1 = response1.data.map(item => ({
      OS: item.OS,
      data_romaneio: date.formatDate(item.data_romaneio, 'DD/MM/YYYY'),
      loja_destino: item.loja_destino,
      loja_origem: item.loja_origem,
      quantidade: parseInt(item.quantidade),
      romanio: item.romanio,
      status_romaneio: item.status_romaneio
    }));

    Romaneios.value = options1;
  } catch (error) {
    console.error("Erro ao buscar dados dos romaneios:", error);
  } finally {
    loading.value = false;
  }
}


</script>
