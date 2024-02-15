<template>
  <q-card flat class="q-mt-sm wt-border">
    <q-card-section class="row">
      <div class="title-style">Separação de Peças</div>
    </q-card-section>
    <q-card-section class="row">
      <q-select
        label="Unidade de origem *"
        dense
        outlined
        stack-label
        use-input
        hide-selected
        fill-input
        input-debounce="0"
        :options="orignUnits"
        type="find"
        color="grey-7"
        class="col-md-2 q-mr-md"
        v-model="romaneioForm.unidade_origem"
        @update:model-value="resetList"
        :disable="partsLoading"
      >
        <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey">Sem opções</q-item-section>
          </q-item>
        </template>
      </q-select>
      <q-spinner-hourglass
        color="teal"
        class="q-mt-sm"
        size="2em"
        v-if="partsLoading"
      />
      <q-select
        v-if="romaneioForm.unidade_origem"
        label="Unidade de destino *"
        dense
        outlined
        stack-label
        use-input
        hide-selected
        fill-input
        input-debounce="0"
        :options="destinationUnits"
        type="find"
        color="grey-7"
        class="col-md-2 q-mr-md"
        v-model="romaneioForm.unidade_destino"
        @update:model-value="resetList"
      >
        <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey">Sem opções</q-item-section>
          </q-item>
        </template>
      </q-select>
    </q-card-section>
    <div id="romaneio">
      <q-card-section v-if="romaneioForm.unidade_destino">
        <q-list bordered separator class="wt-border">
          <q-expansion-item
            default-opened
            expand-separator
            v-for="(part, index) in parts[romaneioForm.unidade_origem][
              romaneioForm.unidade_destino
            ]"
            :key="index"
            :label="'Marca: ' + index"
            header-class="text-black"
            ><q-card>
              <q-expansion-item
                  v-for="(os, index) in part"
                  :key="index"
                  :header-inset-level="1"
                  expand-separator
                  default-opened
                >
                  <template v-slot:header>
                    <div class="flex flex-space-between items-center full-width">
                    <div class="text-bold">OS: #{{index}}</div>
                    <q-separator />
                    </div>
                  </template>
                <q-card>
                  <q-card-section>
                    <q-table
                      flat
                      bordered
                      :rows="os.items"
                      :columns="columns"
                      class="wt-border no-shadow"
                      row-key="row_key"
                      selection="multiple"
                      v-model:selected="itemsRomaneioSelected.items"
                      :pagination="pagination"
                      dense
                    >
                      <template v-slot:body-cell="props">
                        <q-td :props="props">
                          <template v-if="props.col.type === 'currency'">
                            {{ format(props.row[props.col.field], "currency") }}
                          </template>
                          <template
                            v-if="
                              !['currency', 'actions', 'info'].includes(
                                props.col.type
                              )
                            "
                          >
                            {{ props.row[props.col.field] }}
                          </template>
                        </q-td>
                      </template>
                    </q-table>
                  </q-card-section>
                </q-card>
              </q-expansion-item>
            </q-card>
          </q-expansion-item>
        </q-list>
      </q-card-section>
      <q-card-section v-if="romaneioForm.unidade_destino">
        <div class="subtile-style">Itens selecionados:</div>
        <q-table
          flat
          bordered
          :rows="itemsRomaneioSelected.items"
          :columns="columnsWithActionRemove"
          class="wt-border no-shadow q-mt-md"
          row-key="row_key"
          :pagination="pagination"
          dense
        >
          <template v-slot:body-cell="props">
            <q-td :props="props">
              <template v-if="props.col.type === 'currency'">
                {{ format(props.row[props.col.field], "currency") }}
              </template>
              <template v-if="props.col.type === 'actions'">
                <q-btn
                  flat
                  round
                  padding="xs"
                  size="sm"
                  v-for="action in props.col.action"
                  :key="action.icon"
                  :icon="action.icon"
                  :color="action.color"
                  @click="action.action(props)"
                />
              </template>
              <template
                v-if="!['currency', 'actions', 'info'].includes(props.col.type)"
              >
                {{ props.row[props.col.field] }}
              </template>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </div>

    <q-dialog title="Editar item" v-model="editItemDialog">
      <q-card class="q-py-md q-px-md wt-border" style="width: 450px">
        <q-form @submit.prevent="confirmEditItem" class="q-gutter-md">
          <h5 class="title-style">Editar item</h5>
          <q-input
            outlined
            stack-label
            label="Quantidade"
            type="number"
            step="any"
            color="grey-7"
            v-model="dataEditItem.quantidade" />

          <div class="row">
            <q-btn
              label="Salvar"
              type="submit"
              class="full-width wt-border"
              color="dark"
            /></div></q-form
      ></q-card>
    </q-dialog>
    <q-card-section v-if="romaneioForm.unidade_destino">
      <div class="row">
        <q-space />
        <q-btn
          color="primary"
          icon="done"
          label="Imprimir Romaneio"
          unelevated
          class="wt-border q-mr-md"
          @click="printRomaneio"
        >
          <q-tooltip>Gerar romaneio</q-tooltip>
        </q-btn>
        <q-btn
          v-if="romaneioForm.unidade_destino != romaneioForm.unidade_origem"
          color="green"
          icon="done"
          label="Gerar Romaneio"
          unelevated
          :loading="loading"
          class="wt-border"
          @click="generateRomaneio"
          :disabled="
            itemsRomaneioSelected.items &&
            itemsRomaneioSelected.items.length === 0
          "
        >
          <q-tooltip>Gerar romaneio</q-tooltip>
        </q-btn>
        <q-btn
          v-if="romaneioForm.unidade_destino == romaneioForm.unidade_origem"
          color="green"
          icon="done"
          label="Baixar Peças"
          unelevated
          class="wt-border"
          @click="openConfirmarBaixa"
          :disabled="
            !itemsRomaneioSelected.items ||
            itemsRomaneioSelected.items.length === 0
          "
        >
          <q-tooltip>Baixar peças das ordens de serviço</q-tooltip>
        </q-btn>
      </div>
    </q-card-section>
  </q-card>

  {{ itemsRomaneioSelected }}

  <q-dialog v-model="baixarPecasOS" seamless position="bottom">
      <q-card style="width: 500px">

        <q-card-section class="row items-center no-wrap">
          <div>
            Tem certeza que deseja baixar os <strong>Itens selecionados </strong>?
          </div>

          <q-space />

          <q-btn flat round icon="done" color="green" @click="handleBaixarPecas()" :loading="loading"/>
          <q-btn flat round icon="close" color="red" v-close-popup />
        </q-card-section>
      </q-card>
    </q-dialog>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useQuasar } from "quasar";
import { format } from "@/functions";
import PartsConferenceService from "../../services/PartsConferenceService";
import modalDialog from "../../components/modal-dialog.vue";
import axios from "axios";
const $q = useQuasar();
const parts = ref([]);
const romaneioForm = ref({});
const orignUnits = ref([]);
const destinationUnits = ref([]);
const partsLoading = ref(false);
const pagination = ref({ rowsPerPage: 50 });
const itemsRomaneioSelected = ref();
const editItemDialog = ref(false);
const itemKeySelected = ref(null);
const dataEditItem = ref({});
const baixarPecasOS = ref(false)
const loading= ref(false)

onMounted(() => {
  loadPartsList();
});

const columns = [
{
    name: "referencia",
    align: "left",
    label: "Referência",
    field: "referencia",
    type: "text",
    sortable: true,
  },{
    name: "quantidade",
    align: "left",
    label: "Quantidade",
    field: "quantidade",
    type: "number",
    sortable: true,
  },
  {
    name: "descricao",
    align: "left",
    label: "Descrição",
    field: "descricao",
    type: "text",
    sortable: true,
  },
  {
    name: "preco",
    align: "left",
    label: "Preço",
    field: "preco",
    type: "currency",
    sortable: true,
  },  {
    name: "codigo_produto",
    align: "left",
    label: "Código produto",
    field: "codigo_produto",
    type: "text",
    sortable: true,
  },
  {
    name: "tipo",
    align: "left",
    label: "Separação",
    field: "tipo",
    type: "text",
    sortable: true,
  },
  {
    name: "data_previsao",
    align: "left",
    label: "Data Prevista",
    field: "data_previsao",
    type: "date",
    sortable: true,
  },
];

const columnsWithActionRemove = [
  ...columns,    {
    name: "codigo_os",
    align: "left",
    label: "OS",
    field: "codigo_os",
    type: "text",
    sortable: true,
  },
  {
    name: "actions",
    align: "right",
    type: "actions",
    action: [
      {
        icon: "edit",
        color: "dark",
        toolTip: "Modificar item",
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

function openConfirmarBaixa(){
  baixarPecasOS.value = true
  

}

function resetList() {
  itemsRomaneioSelected.value = {};
}

function resetPage() {
  itemsRomaneioSelected.value = {};
  romaneioForm.value = {};
  loadPartsList();
}

function printRomaneio() {
  const prtHtml = document.getElementById("romaneio").innerHTML;

  let stylesHtml = "";
  for (const node of [
    ...document.querySelectorAll('link[rel="stylesheet"], style'),
  ]) {
    stylesHtml += node.outerHTML;
  }

  const WinPrint = window.open(
    "",
    "",
    "left=0,top=0,width=800,height=900,toolbar=0,scrollbars=0,status=0"
  );

  WinPrint.document.write(`<!DOCTYPE html>
  <html>
    <head>
      ${stylesHtml}
    </head>
    <body>
      <div style="padding: 14px">
      <h4>Separação de Peças</h4>
      <h5>Unidade origem: ${romaneioForm.value.unidade_origem} | Unidade destino: ${romaneioForm.value.unidade_destino}</h5>
    </div>
      ${prtHtml}
    </body>
  </html>`);

  WinPrint.document.close();

  setTimeout(() => {
    WinPrint.focus();
    WinPrint.print();
    WinPrint.close();
  }, 500);
}

const handleRemoveItemPurchase = (itemKey) => {
  itemsRomaneioSelected.value.items = [
    ...itemsRomaneioSelected.value.items.filter(
      (item) => item.codigo_produto !== itemKey
    ),
  ];
};

async function handleBaixarPecas(){
  loading.value = true
  const payload = {
    
    items: itemsRomaneioSelected.value.items,
  };
  try {
    const response = await axios.post(
      `https://app.watchtime.com.br/api/estoklus/baixa_pecas`,
     payload
    );
    $q.notify({
      message: "Peças baixadas com sucesso",
      type: "positive",
      color: "green",
    });
    resetPage();
  } catch (error) {
    $q.notify({
      message: "Erro ao baixar peças",
      type: "negative",
      color: "danger",
    });
  }
  loading.value = false
 baixarPecasOS.value = false
 resetPage();
}

const handleEditPurchase = (itemKey) => {
  editItemDialog.value = true;
  itemKeySelected.value = itemKey;

  const orderItem = itemsRomaneioSelected.value.items.find(
    (item) => item.codigo_produto === itemKey
  );

  dataEditItem.value.quantidade = orderItem.quantidade;
};

const confirmEditItem = () => {
  const orderItem = itemsRomaneioSelected.value.items.find(
    (item) => item.codigo_produto === itemKeySelected.value
  );

  orderItem.quantidade = Number(dataEditItem.value.quantidade);

  editItemDialog.value = false;
  itemKeySelected.value = null;
};

async function loadPartsList() {
  partsLoading.value = true;
  try {
    parts.value = await PartsConferenceService.getPartsConference();
    destinationUnits.value =  ['RJ','SP','PR'];
    orignUnits.value = Object.keys(parts.value);
  } catch (error) {
    console.log(error);
  }
  partsLoading.value = false;
}

async function generateRomaneio() {

    loading.value = true
  const payload = {
    unidade_origem: romaneioForm.value.unidade_origem,
    unidade_destino: romaneioForm.value.unidade_destino,
    items: itemsRomaneioSelected.value.items,
  };

  try {
    await PartsConferenceService.generateRomaneio(payload);
    $q.notify({
      message: "Romaneio criado com sucesso",
      type: "positive",
      color: "green",
    });
    resetPage();
  } catch (error) {
    $q.notify({
      message: "Erro ao criar um romaneio",
      type: "negative",
      color: "danger",
    });
  }
  loading.value = false
}
</script>

