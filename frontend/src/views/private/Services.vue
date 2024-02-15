<template>
    <app-table
      ref="tableRef"
      :pagination="pagination"
      :columns="columns"
      :rows="services"
      row-key="id"
      
      class="q-pa-md wt-border"
      :loading="loading"
      @request="loadservices"
      :filter="search"
      flat
    >



      <template v-slot:top>
          
        <div class="row full-width q-mb-lg">
          <div class="title-style">Ordens de Serviço</div>
            <q-space/>
          <q-select
            label="Marca"
            outlined
            input-debounce="0"
            :options="brandsFiltered"
            v-model="search.brand"
            @filter="filterBrand"
            stack-label
            use-input
            dense
            style="max-width:8%"
            color="grey-7"
            class="q-mr-md wt-border"
          />
          <q-select
            label="Loja"
            outlined
            input-debounce="0"
            :options="lojaFiltered"
            v-model="search.loja"
            @filter="filterLoja"
            stack-label
            use-input
            style="max-width:8%"
            dense
            color="grey-7"
            class="q-mr-md wt-border"
          />
          <q-input
            v-model="search.os_loja"
            dense
            outlined
            stack-label
            color="grey-7"
            type="search"
            label="OS da Loja"
            style="max-width:12%"
            debounce="300"
            class="q-mr-md wt-border"
          >
          
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
          <q-input
            v-model="search.referencia_produto"
            dense
            outlined
            stack-label
            color="grey-7"
            type="search"
            label="Referência ou Série"
            debounce="300"
            class="q-mr-md wt-border"
          >
          
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
          <q-input
            v-model="search.text"
            dense
            outlined
            stack-label
            color="grey-7"
            type="search"
            label="Código ou nome"
            debounce="300"
            class="q-mr-md"
          >
          
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        
        </div>
        <q-btn
          size="md"
          color="green"
          unelevated
          style="border-radius: 8px"
          icon="add_circle"
          label="Nova OS"
          class="wt-border"
          @click="showRequest = true"
        >
          <q-tooltip>Adicionar OS</q-tooltip>
        </q-btn>
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
    <service-request
    v-model:showRequest="showRequest"
    persistent
    :maximized="true"
    @os="handleOSAberta"
    />
    <service-estimate
    v-model:showEstimate="showEstimate"
    v-model:modelValue="selectedService"
    persistent
    @os="handleOrcamento"
    />
    <service-devolution
    v-model:showDevolution="showDevolution"
    v-model:cabecalho="selectedService"
    v-model:itens="itens"
    persistent
    />
    <service-approval
    v-model:showApproval="showApproval"
    v-model:modelValue="selectedService"
    persistent
    />

    <modal-dialog
    title="Cancelar"
    mode
    v-model="gerarNFICMS"
    :message="`Tem certeza que deseja gerar a NF da OS ${selectedService.id}?`"
    @confirm="handleGerarNFICMS"
  />

  <modal-dialog
    title="Cancelar"
    mode
    v-model="enviarEmail"
    :message="`O e-mail será enviado para ${selectedService.metodo_envio}, você tem certeza?`"
    @confirm="handleEnviarEmail"
  />

  <modal-dialog
    title="Cancelar"
    mode
    v-model="enviarEmailOrcamento"
    :message="`O e-mail será enviado para ${selectedService.metodo_envio}, você tem certeza?`"
    @confirm="handleEnviarOrcamento"
  />

  <modal-dialog
    title="Cancelar"
    mode
    v-model="enviarWPP"
    :message="`O Whatsapp será enviado para o número ${selectedService.metodo_envio}, você tem certeza?`"
    @confirm="handleEnviarWPP"
  />

  <modal-dialog
  :requireInput="true"
  v-model="enviarOficina"
  :message="`Texto do Histórico da OS`"
  @confirm="handleEnviarOficina"
  :text="`Subiu para oficina - Previsão de conclusão `"
/>

<q-dialog v-model="cameraModalOpen" maximized>
          <q-card class="custom-dialog-size">
            <div class="title-style flex q-mt-md row items-center justify-center">{{ selectedService.id }}</div>
            <q-card-section>
              <div class="flex full-height row items-end justify-end q-mt-md">
    <q-btn color="grey" label="Fechar" @click="stopCameraAndCloseModal"></q-btn>
  </div>
          </q-card-section>
            <q-card-section >
            <camera-modal v-if="cameraModalOpen" :photoType="photoType" :data="selectedService" @modalClosed="stopCameraAndCloseModal"></camera-modal>
            </q-card-section>

          

        </q-card>
</q-dialog>

<modal-dialog-hist
  v-model="inserirHistorico"
  @confirm="handleGerarHistorico"
/>

<modal-dialog-refusal
  v-model="showReprovarOS"
  @confirm="handleReprovarOS"
  :os="selectedService"
/>

<modal-dialog-mail
  v-model="showEnviarEmail"
  :imagesBase64="imagesBase64"
  :OS="selectedService"
/>

<service-repair
  v-model:ShowServiceRepair="ShowServiceRepair"
  v-model="ShowServiceRepair"
  :OS="selectedService"
  >
</service-repair>

  </template>
  
  <script setup>

  import { ref, onMounted, computed, watch } from "vue";
  import { useQuasar } from "quasar";
  import OrdersServicesService from "../../services/Services";
  import ServiceEstimate from "./ServiceEstimate.vue";
  import ServiceRequest from "./ServiceRequest.vue";
  import ServiceDevolution from "./ServiceDevolution.vue";
  import ServiceApproval from "./ServiceApproval.vue";
  import AppTable from "../../components/app-table.vue";
  import { STATUSES } from "../../types/Services";
  import axios from "axios";
  import { QSpinnerGears } from "quasar";
  import { autoCapitalize } from "@/functions.js";
  import ModalDialog from "../../components/modal-dialog.vue";
  import ModalDialogHist from "../../components/modal-dialog-hist.vue";
  import ModalDialogRefusal from "../../components/modal-dialog-refusal.vue";
  import ModalDialogMail from "../../components/modal-dialog-mail.vue";
  import { Notify } from 'quasar';
  import CameraModal from "../../components/CameraModal.vue";
  import AuthService from "../../services/AuthService";
  import ServiceRepair from "./ServiceRepair.vue";

  const ShowServiceRepair = ref(false)
  const dadosOS = ref([]) 
  const currentUser = computed(() => AuthService.user);
  const imagesBase64 = ref([])
  const showEnviarEmail = ref(false)
  const enviarEmailOrcamento = ref(false)
  const enviarEmail = ref(false)
  const enviarWPP = ref(false)
  const showReprovarOS = ref(false)
  const cameraModalOpen = ref(false)
  const gerarNFICMS = ref(false);
  const enviarOficina = ref(false);
  const inserirHistorico = ref(false);
  const $q = useQuasar();
  const text = ref("");
  const valor_liquido = ref(null);
  const name = ref("");
  const cliente = ref("");
  const marca = ref("");
  const search = ref({
    text: "",
    brand: null,
    os_loja:"",
    referencia_produto:""
  });
  const tableRef = ref();
  const services = ref([]);
  const statusFilter = ref(1);
  const loading = ref(false);
  const pagination = ref({
  rowsPerPage: 50,
  page: 1,
  rowsNumber: 0,
  sortBy: 'codigo_estoklus',
  descending: true // Define como true por padrão
});
  const brands = ref([]);
  const loja = ref([]);
  const brandsFiltered = ref([]);
  const lojaFiltered = ref([]);
  const isLoadingP = ref(false);
  const isLoadingD = ref(false);
  const isLoading = ref(false);
  const servicesSummary = ref({})
  const columns = ref(getColumns(statusFilter));
  const showRequest = ref(false);
  const showEstimate = ref(false);
  const serviceOrder = ref();
  const selectedService = ref({});
  const showDevolution = ref(false)
  const showApproval = ref(false)
  QSpinnerGears;
  const itens = ref([])
  const photoType= ref('')
  
  onMounted(() => {
    loadBrands();
    loadLojas();
 
  });
  function selectedStatus(newValue) {
    statusFilter.value = newValue;
    tableRef.value.requestServerInteraction();
}

const stopCameraAndCloseModal = () => {
            cameraModalOpen.value = false;
        };

    const openCamera = (type) => {
      selectedService.value = type.row;
      photoType.value = type;
      cameraModalOpen.value = true;
    };
const statusToggle = computed(() => {
  const options = [];
  for (let status of STATUSES) {
    const number = servicesSummary.value[status.value];
    if (status.value !== "cancelled") {
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

async function newOS() {

}
  
  function getColumns(statusFilter){
  

  
  const baseColumns = [
    {
      name: "codigo_estoklus",
      align: "left",
      label: "Código",
      field: "codigo_estoklus",
      type: "decimal",
      sortable: true,
    },
    {
      name: "loja",
      align: "left",
      label: "Unidade",
      field: "loja",
      type: "text",
      sortable: true,
    style: "max-width: 200px"
    },    {
      name: "sistema",
      align: "left",
      label: "Sistema",
      field: "sistema",
      type: "text",
      sortable: true,
    style: "max-width: 200px"
    },
    {
      name: "marca",
      align: "left",
      label: "Marca",
      field: "marca",
      type: "text",
      sortable: true,
      style: "max-width: 200px"
    },
    {
      name: "nome",
      align: "left",
      label: "Cliente",
      field: "nome",
      type: "name",
      sortable: true,
    },
  ]
  
  if (statusFilter.value === '1' ) {
    baseColumns.push({
      name: "data_os",
      align: "right",
      label: "Data",
      field: "data_os",
      type: "date",
      sortable: true,
    },
    {
      name: "modelo",
      align: "right",
      label: "modelo",
      field: "modelo",
      type: "text",
      sortable: true,
    });
  } else if (statusFilter.value === '2') {
    baseColumns.push({
      name: "data_analise",
      align: "right",
      label: "Data Orçamento",
      field: "data_analise",
      type: "date",
      sortable: true,
    },
    {
      name: "valor_cliente",
      align: "right",
      label: "Valor",
      field: "valor_cliente",
      type: "number",
      sortable: true,
    });
  } else if (['3','8'].includes(statusFilter.value)) {
    baseColumns.push({
      name: "data_reprovado",
      align: "right",
      label: "Data reprovação",
      field: "data_reprovado",
      type: "date",
      sortable: true,
    },
    {
      name: "valor_liquido",
      align: "right",
      label: "Valor",
      field: "valor_cliente",
      type: "number",
      sortable: true,
    });
  } else if (statusFilter.value === '4') {
    baseColumns.push({
      name: "data_aprovado",
      align: "right",
      label: "Data Aprovação",
      field: "data_aprovado",
      type: "date",
      sortable: true,
    },{
      name: "data_prevista_entrega",
      align: "right",
      label: "Data Prevista",
      field: "data_prevista_entrega",
      type: "date",
      sortable: true,
    },
    {
      name: "valor_cliente",
      align: "left",
      label: "Valor",
      field: "valor_cliente",
      type: "number",
      sortable: true,
    });
  } else if (statusFilter.value === '5') {
    baseColumns.push({
      name: "data_inicio_conserto",
      align: "right",
      label: "Início Conserto",
      field: "data_inicio_conserto",
      type: "date",
      sortable: true,
    },{
      name: "data_prevista_entrega",
      align: "right",
      label: "Data Prevista",
      field: "data_prevista_entrega",
      type: "date",
      sortable: true,
    },
    {
      name: "valor_liquido",
      align: "left",
      label: "Valor",
      field: "valor_cliente",
      type: "number",
      sortable: true,
    });
  } else if (statusFilter.value === '6') {
    baseColumns.push({
      name: "data_termino_conserto",
      align: "right",
      label: "Data Liberado",
      field: "data_termino_conserto",
      type: "date",
      sortable: true,
    },
    {
      name: "valor_liquido",
      align: "left",
      label: "Valor",
      field: "valor_cliente",
      type: "number",
      sortable: true,
    });
    };

    let actions = [];
    if (statusFilter.value == '1') {
    actions = [
      {
        icon: "currency_exchange",
        color: "dark",
        toolTip: "Lançar orçamento",
        action: (props) => {
          openLancarOrcamento(props)
        }},{
        icon: "camera",
        color: "dark",
        toolTip: "Tirar Fotos",
        action: (props) => {
          openCamera(props)
        }}, {
        class:"material-symbols-outlined",
        icon: "comment",
        color: "blue",
        toolTip: "Lançar histórico",
        loading: loading,
        action: (props) => {

          openInserirHistorico(props)
        },
      },{
        icon: "attach_email",
        color: "bue",
        toolTip: "Enviar OS por e-mail",
        action: (props) => {
          openEnviarEmail(props)
        }},{
        icon: "security_update_warning",
        color: "green",
        toolTip: "Enviar OS por Whatsapp",
        action: (props) => {
          openEnviarWPP(props)
        }}, {
        class:"material-symbols-outlined",
        icon: "person",
        color: "red",
        toolTip: "Via Cliente",
        loading: loading,
        action: (props) => {

          openPDFInNewTab(props.row,'via_cliente')
        },
      },{
        class:"material-symbols-outlined",
        icon: "store",
        color: "dark",
        toolTip: "Via Interna",
        loading: loading,
        action: (props) => {

          openPDFInNewTab(props.row,'via_interna')
        },
      },{
        icon: "sync",
        color: "green",
        toolTip: "Sincronizar com Estoklus",
        loading: loading,
        action: (props) => {

          syncEstoklus(props)
        },
      }
        ]}
      if (['4','5'].includes(statusFilter.value)) {
        
        actions = [
      {
        class:"material-symbols-outlined",
        icon: "checklist",
        color: "green",
        toolTip: "Enviar p/ Oficina",
        loading: loading,
        action: (props) => {

          openServiceRepair(props)
        },
      },    {
        class:"material-symbols-outlined",
        icon: "comment",
        color: "blue",
        toolTip: "Lançar histórico",
        loading: loading,
        action: (props) => {

          openInserirHistorico(props)
        },
      },{
        icon: "camera",
        color: "dark",
        toolTip: "Tirar Fotos",
        action: (props) => {
          openCamera(props)
        }}, {
        class:"material-symbols-outlined",
        icon: "person",
        color: "red",
        toolTip: "Via Cliente",
        loading: loading,
        action: (props) => {

          openPDFInNewTab(props.row,'via_cliente')
        },
      },{
        class:"material-symbols-outlined",
        icon: "store",
        color: "dark",
        toolTip: "Via Interna",
        loading: loading,
        action: (props) => {

          openPDFInNewTab(props.row,'via_interna')
        },
      },{
        class:"material-symbols-outlined",
        icon: "payments",
        color: "red",
        toolTip: "imprimir Orçamento",
        loading: loading,
        action: (props) => {

          openPDFInNewTab(props.row,'orcamento_cliente')
        }},{
        class:"material-symbols-outlined",
        icon: "picture_as_pdf",
        color: "red",
        toolTip: "imprimir Orçamento com Imagem",
        loading: loading,
        action: (props) => {

          openPDFInNewTab(props.row,'orcamento_cliente_ci')
        }
      },{
        icon: "attach_email",
        color: "bue",
        toolTip: "Enviar OS por e-mail",
        action: (props) => {
          openEnviarEmail(props)
        }},{
        icon: "security_update_warning",
        color: "green",
        toolTip: "Enviar OS por Whatsapp",
        action: (props) => {
          openEnviarWPP(props)
        }},{
        icon: "sync",
        color: "green",
        toolTip: "Sincronizar com Estoklus",
        loading: loading,
        action: (props) => {

          syncEstoklus(props)
        },
      }]}
      if (['2'].includes(statusFilter.value)) {
        actions = [ {
        icon: "currency_exchange",
        color: "dark",
        toolTip: "Lançar orçamento",
        action: (props) => {
          openLancarOrcamento(props)
        }},
      {
        class:"material-symbols-outlined",
        icon: "done",
        color: "green",
        toolTip: "Aprovar",
        loading: loading,
        action: (props) => {

          openServiceApproval(props)
        },
      },      {
        class:"material-symbols-outlined",
        icon: "block",
        color: "red",
        toolTip: "Reprovar",
        loading: loading,
        action: (props) => {

          openReprovarOS(props)
        },
      },    {
        class:"material-symbols-outlined",
        icon: "comment",
        color: "blue",
        toolTip: "Lançar histórico",
        loading: loading,
        action: (props) => {

          openInserirHistorico(props)
        },
      } ,{
        class:"material-symbols-outlined",
        icon: "store",
        color: "dark",
        toolTip: "Via Interna",
        loading: loading,
        action: (props) => {

          openPDFInNewTab(props.row,'via_interna')
        },
      },{
        class:"material-symbols-outlined",
        icon: "picture_as_pdf",
        color: "red",
        toolTip: "imprimir Orçamento com Imagem",
        loading: loading,
        action: (props) => {

          openPDFInNewTab(props.row,'orcamento_cliente_ci')
        }
      },
      {
        class:"material-symbols-outlined",
        icon: "payments",
        color: "red",
        toolTip: "imprimir Orçamento",
        loading: loading,
        action: (props) => {

          openPDFInNewTab(props.row,'orcamento_cliente')
        },
      }, {
        class:"material-symbols-outlined",
        icon: "person",
        color: "red",
        toolTip: "Via Cliente",
        loading: loading,
        action: (props) => {

          openPDFInNewTab(props.row,'via_cliente')
        },
      },{
        icon: "camera",
        color: "dark",
        toolTip: "Tirar Fotos",
        action: (props) => {
          openCamera(props)
        }},{
        icon: "attach_email",
        color: "bue",
        toolTip: "Enviar OS por e-mail",
        action: (props) => {
          openEnviarEmail(props)
        }},{
        icon: "security_update_warning",
        color: "green",
        toolTip: "Enviar OS por Whatsapp",
        action: (props) => {
          openEnviarWPP(props)
        }},{
        icon: "sync",
        color: "green",
        toolTip: "Sincronizar com Estoklus",
        loading: loading,
        action: (props) => {

          syncEstoklus(props)
        },
      }]}

      
      if (['3','6','8'].includes(statusFilter.value)) {
        actions = [  {
        class:"material-symbols-outlined",
        icon: "checklist",
        color: "green",
        toolTip: "Enviar p/ Oficina",
        loading: loading,
        action: (props) => {

          openServiceRepair(props)
        },
      },
      {
        icon: "local_shipping",
        color: "teal",
        toolTip: "Nota de Devolução",
        loading: loading,
        action: (props) => {

          openServiceDevolution(props)
        },
      },
      {
        icon: "article",
        color: "orange",
        toolTip: "Nota de peças",
        loading: loading,
        action: (props) => {
          openLancarNFICMS(props)
        },
      },{
        icon: "camera",
        color: "dark",
        toolTip: "Tirar Fotos",
        action: (props) => {
          openCamera(props)
        }}, {
        class:"material-symbols-outlined",
        icon: "comment",
        color: "blue",
        toolTip: "Lançar histórico",
        loading: loading,
        action: (props) => {

          openInserirHistorico(props)
        },
      },{
        icon: "attach_email",
        color: "bue",
        toolTip: "Enviar OS por e-mail",
        action: (props) => {
          openEnviarEmail(props)
        }},{
        icon: "security_update_warning",
        color: "green",
        toolTip: "Enviar OS por Whatsapp",
        action: (props) => {
          openEnviarWPP(props)
        }},{
        icon: "sync",
        color: "green",
        toolTip: "Sincronizar com Estoklus",
        loading: loading,
        action: (props) => {

          syncEstoklus(props)
        },
      }]
    
    
  }  if (['7'].includes(statusFilter.value)) {
        actions = [
      {
        icon: "article",
        color: "orange",
        toolTip: "Nota de peças",
        loading: loading,
        action: (props) => {
          openLancarNFICMS(props)
        },
      },{
        icon: "camera",
        color: "dark",
        toolTip: "Tirar Fotos",
        action: (props) => {
          openCamera(props)
        }}, {
        class:"material-symbols-outlined",
        icon: "comment",
        color: "blue",
        toolTip: "Lançar histórico",
        loading: loading,
        action: (props) => {

          openInserirHistorico(props)
        },
      },{
        icon: "attach_email",
        color: "bue",
        toolTip: "Enviar OS por e-mail",
        action: (props) => {
          openEnviarOrcamento(props)
        }},{
        icon: "security_update_warning",
        color: "green",
        toolTip: "Enviar OS por Whatsapp",
        action: (props) => {
          openEnviarWPP(props)
        }},{
        icon: "sync",
        color: "green",
        toolTip: "Sincronizar com Estoklus",
        loading: loading,
        action: (props) => {

          syncEstoklus(props)
        },
      }]
  }
    baseColumns.push({
    name: "actions",
    align: "center",
    type: "actions",
    actions: actions,
   
    });

    return baseColumns
  }

  const form = [
    { name: "codigo_estoklus", label: "Código *", field: "codigo_estoklus", type: "text" },
    { name: "marca", label: "Marca *", field: "marca", type: "text" },
    { name: "nome", label: "Cliente", field: "nome", type: "text" },
    { name: "name", label: "Nome *", field: "name", type: "text" },
    {
      name: "valor_liquido",
      label: "Valor *",
      field: "valor_liquido",
      type: "number",
      mask: "############",
    },
  ];
  
  onMounted(() => {
    tableRef.value.requestServerInteraction();
  });
  
  async function loadBrands() {
    const response = await OrdersServicesService.getServices({
      _select: "marca",
      _distinct: true,
      _order_a: "marca",
    });
    

    brands.value = response.data?.filter(item => item.marca !== null).map((b) => {
      return { label: b.marca.toUpperCase(), value: b.marca };
    });
  }

  async function loadLojas() {
    const responsel = await OrdersServicesService.getServices
    ({_select:"loja",
      _distinct:true,
      _order_a: "loja"})
   
  
    loja.value = responsel.data?.filter(item => item.loja !== null).map((l) => {
      return { label: l.loja.toUpperCase(), value: l.loja };
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
        (brand) =>{
    // Verifique se brand.label é uma string
    if (typeof brand.label !== 'string') {
      console.warn('brand.label não é uma string:', brand.label);
      return false; // Skip this iteration
    }

    // Verifique se val é uma string
    if (typeof val !== 'string') {
      console.warn('val não é uma string:', val);
      return false; // Skip this iteration
    }
        

    return brand.label.toLowerCase().indexOf(val.toLowerCase()) > -1;
  });

      
    });
  }
  function filterLoja(val, update) {
    if (val === "") {
      update(() => {
        lojaFiltered.value = loja.value;
      });
      return;
    }

    update(() => {
      lojaFiltered.value = loja.value.filter((loja) => {
        // Verifique se brand.label é uma string
        if (typeof loja.label !== 'string') {
          console.warn('brand.label não é uma string:', loja.label);
          return false; // Skip this iteration
        }

        // Verifique se val é uma string
        if (typeof val !== 'string') {
          console.warn('val não é uma string:', val);
          return false; // Skip this iteration
        }

        // Agora você sabe que ambos são strings, então você pode chamar toLowerCase()
        return loja.label.toLowerCase().indexOf(val.toLowerCase()) > -1;
      });
    });
}
  
  async function loadservices(props) {

    const { page, rowsPerPage, sortBy, descending} = props.pagination || {};
    
    const filter = props.filter;
    columns.value = getColumns(statusFilter);
  
    loading.value = true;
    try {
      const filters = {};
      if (filter.brand) {
        filters["marca.lk"] = props.filter.brand.value;
      }
  
      if (filter.text) {
        filters["nome.lk,id.lk"] = '%'+props.filter.text+'%';
      }
      if (filter.loja) {
        filters["loja"] = props.filter.loja.value;
      }
      if (filter.os_loja) {
        filters["os_loja.lk"] = '%'+props.filter.os_loja+'%';
      }
      if (filter.referencia_produto) {
        filters["referencia_produto.lk,serie.lk"] = '%'+props.filter.referencia_produto+'%';
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

    servicesSummary.value =  await OrdersServicesService.getServicesSummary(
        "status",
        statusFiltered
      );
      

      const params = new URLSearchParams(filters);
    const url = "https://app.watchtime.com.br/api/service_orders?" + params.toString();

    const response = await axios.get(url);
   
        const dataArray = response.data.data.map(item => {
          if (item.id !== undefined && (item.id.startsWith('SPA') || item.id.startsWith('RJA') || item.id.startsWith('PRA'))) {
          item.sistema = 'Antigo';
            }
            else{
              item.sistema= 'Novo'
            }

            
        let newItem = {};
        for (let key of Object.keys(item)) {
            if (typeof item[key] === 'string') {
                newItem[key] = item[key].toUpperCase();
            } else {
                newItem[key] = item[key];
            }
        
         

        }
        return newItem;
    });
    const rows = response.data.rows;
    

    services.value.splice(0, services.value.length, ...dataArray);
    pagination.value = {
        sortBy: sortBy,
        descending: descending,
        page: page,
        rowsPerPage: rowsPerPage,
        rowsNumber: rows,
    };
} catch (error) {
    console.error(error);
}
    loading.value = false;
  }

  function getStatusIcon(status) {
  const icons = {
    1: "troubleshoot",
    2: "pending",
    3: "dangerous",
    4: "pause",
    5: "healing",
    6: "check_circle",
    7: "send",
    8: "dangerous"
  };

  return icons[status];
}

const fetchDados = async (val, update) => {
  loading.value = true;

  try {
      const response = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/nf_saida/`+selectedService.value.cliente_id
      );

      const options = response.data.map(item =>  ({
        status: item.status,
        codigo_produto_cliente: item.codigo_produto_cliente,
        nf_cliente: item.nf_cliente === "0" ? parseInt(item.nf_estoklus): item.nf_cliente  ,
        nf_estoklus: item.nf_estoklus,
        loja_os:item.loja_os,
        valor_produto:parseFloat(item.valor_produto, 10),
        referencia_os_cliente:item.referencia_os_cliente,
        codigo_tipo_pessoa:item.codigo_tipo_pessoa,
        referencia_produto:item.referencia_produto,
        serie:item.serie,
        modelo:item.modelo,
        codigo_os:item.codigo_os,
        quantidade_recebida:item.quantidade_recebida,
        quantidade_devolvida:item.quantidade_devolvida,
        item_inserido:false,
        marca:item.marca,
        devolucao: item.quantidade_recebida === 1 || item.quantidade_recebida === 0 ? "Total" : "Parcial"
      }));

      itens.value = options;

    
  } catch (err) {
    console.error("Erro ao buscar dados:", err);
  }
  loading.value = false;
};

function openLancarNFICMS(props) {
  selectedService.value = props.row;
  gerarNFICMS.value=true;
}

function openEnviarOficina(props) {
  selectedService.value = props.row;
  enviarOficina.value=true;
}
function openInserirHistorico(props) {
  selectedService.value = props.row;
  inserirHistorico.value=true;
}
async function openServiceRepair(props) {
  selectedService.value = props.row;
  selectedService.value.data_termino_preparacao = '1'
  selectedService.value.data_termino_polimento= '1'
 // selectedService.value.data_termino_conserto = '1'
 const  responseData = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/get_os_completa/`+selectedService.value.codigo_estoklus
      )
      selectedService.value= responseData.data
      selectedService.value.itens.forEach(item => {
  // Calcula a quantidade a retirar somente se tiver estoque disponível
  if (item.estoque > 0) {
    item.quantidade_a_retirar = item.quantidade - item.quantidade_retirada;
  }else if(item.estoque < item.quantidade){
    item.quantidade_a_retirar = item.estoque
  } else {
    item.quantidade_a_retirar = 0; // Define como 0 se não houver estoque
  }
});

  selectedService.value.loja= props.row.loja
  if (selectedService.value.tecnico_conserto == ''){

    delete selectedService.value.tecnico_conserto 

  }  if (selectedService.value.tecnico_polimento == ''){
    delete selectedService.value.tecnico_polimento 
}  if (selectedService.value.tecnico_preparacao == ''){
    delete selectedService.value.tecnico_preparacao
}

  ShowServiceRepair.value=true;
}

const openEnviarEmail = async (props) => {
  selectedService.value = props.row;
  let dado = await getCustomerData(props.row.cliente_id,'EMAIL')
  if(dado == ''){
    Notify.create({
              type: 'negative',
              message: `E-mail em branco`
            });
  }

  else {
    const dataOs = selectedService.value.data_os;
let partesData = dataOs.split('/');

if (partesData.length !== 3) {
    partesData = dataOs.split('-');
    if (partesData.length === 3) {
        // If the date is in the format YYYY-MM-DD
        partesData = [partesData[2], partesData[1], partesData[0]];
    }
}

const ano = partesData[2]; // Year
const mes = partesData[1]; // Month

const dataToSubmit = {
    "codigo_estoklus": selectedService.value.codigo_estoklus,
    "ano": parseInt(ano, 10),
    "mes": parseInt(mes, 10)
};
    const response = await axios.post(
      `https://app.watchtime.com.br/api/mail/listar_fotos`,
      dataToSubmit
    );
    selectedService.value.texto_email = '' 
    imagesBase64.value = response.data
    if(selectedService.value.status == '1'){
      selectedService.value.titulo_email = `Abertura de Ordem de serviço - ${selectedService.value.id}${selectedService.value.brand_id} `
      selectedService.value.texto_email = `Olá, ${selectedService.value.nome}!

Este e-mail foi enviado para documentar que sua ordem de serviço de número ${selectedService.value.id}${selectedService.value.brand_id} foi aberta.

Para orçamento, informamos que o prazo para envio de orçamento é de até 3 dias úteis.

Qualquer dúvida, estamos a disposição!

Atenciosamente,

${currentUser.value.name}
`
    }else if (selectedService.value.status == '2'){
     const  responseData = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/get_os_completa/`+selectedService.value.codigo_estoklus
      )
      selectedService.value.diagnostico = responseData.data.diagnostico_tecnico
      selectedService.value.prazo = responseData.data.prazo_entrega
      selectedService.value.garantia = responseData.data.garantia
      selectedService.value.titulo_email = `Orçamento Ordem de serviço - ${selectedService.value.id}${selectedService.value.brand_id} `
      selectedService.value.texto_email = `Olá, ${selectedService.value.nome}!
Envio anexo em PDF, Orçamento do Relógio:  ${selectedService.value.marca} , Modelo:  ${selectedService.value.modelo} , Referência:  ${selectedService.value.referencia_produto} , Serie: ${selectedService.value.serie}.
OS ${selectedService.value.id}
Segue a explicação do orçamento em relação a execução e garantia do serviço.

OBSERVAÇÕES TÉCNICAS:${selectedService.value.diagnostico}

GARANTIA:${selectedService.value.garantia}

PRAZO DE ENTREGA: ${selectedService.value.prazo}

Orçamento válido por 10 dias.

Favor responder este e-mail com aprovação (opcionais ou sem opcionais) ou recusa.
Caso aprovado, necessário um sinal de 50% do valor total
Ficamos a disposição para maiores esclarecimentos.
Att,
${currentUser.value.name}
`
    }


    

    showEnviarEmail.value = true
  }
}

const openEnviarOrcamento = async (props) => {
  selectedService.value = props.row;
  let dado = await getCustomerData(props.row.cliente_id,'EMAIL')
  console.log(dado)
  if(dado == ''){
    Notify.create({
              type: 'negative',
              message: `E-mail em branco`
            });
  }

  else {
    enviarEmailOrcamento.value=true;
  }
}


const openEnviarWPP = async (props) => {
  selectedService.value = props.row;
  let dado = await getCustomerData(props.row.cliente_id,'TEL_CELULAR')

  selectedService.value.metodo_envio = formataCelular(selectedService.value.metodo_envio)

  if(dado == ''){
    Notify.create({
              type: 'negative',
              message: `Telefone celular em branco`
            });
  }
  else{enviarWPP.value=true;
}}
  
  

function openReprovarOS(props) {
  selectedService.value = props.row;
  if(selectedService.value.brand_id == 'BE'){
    selectedService.value.repair_bre = '007';
  }
  
  showReprovarOS.value=true;

}

function formataCelular(numero){
      // Remove caracteres não numéricos
      let numeroLimpo = numero.replace(/\D/g, '');

      // Verifica se o número começa com o dígito de código de área brasileiro "4"
      if (numeroLimpo.startsWith('4')) {
        if (numeroLimpo.length === 11) {
          return numeroLimpo.replace(/^(\d{2})(\d{1})(\d{4})(\d{4})$/, '($1) $2 $3-$4');
        } else if (numeroLimpo.length === 10) {
          return numeroLimpo.replace(/^(\d{2})(\d{4})(\d{4})$/, '($1) $2-$3');
        }
      } else {
        // Caso não comece com "4", ajuste a formatação como desejar
        // Aqui está apenas um exemplo genérico
        return numeroLimpo.replace(/^(\d{2})(\d{4,5})(\d{4})$/, '($1) $2-$3');
      }
      
      return num; // retorna o número original caso não corresponda a nenhum formato
    }

function openLancarOrcamento(props) {
  selectedService.value = props.row;
  showEstimate.value=true;

}async function openServiceDevolution(props) {
  selectedService.value = props.row;
  await fetchDados()
  showDevolution.value=true;
}async function openServiceApproval(props) {
  selectedService.value = props.row;
  showApproval.value=true;

}

 async function handleOSAberta(val) { 

    await  openPDFInNewTab(val,'via_interna')
    await  openPDFInNewTab(val,'via_cliente')
  
}
  function handleOrcamento(val) { 

  openPDFInNewTab(val,'orcamento_cliente')


}


const handleGerarNFICMS = async (val, update) => {
  try {

      const response = await axios.post(
        `https://app.watchtime.com.br/api/estoklus/nf_icms`,selectedService.value
      );      
      if(response.data.success != undefined){
        Notify.create({
              type: 'positive',
              message: `NF ${response.data.success} gerada no Estoklus`
            });

      }
      else{
        Notify.create({
              type: 'warning',
              
              message: `${response.data.error}`
            });

      }
    }catch(error){Notify.create({
              type: 'negative',
              message: `Erro ao emitir NF`
            });
    }

  }

  const handleEnviarWPP = async (type) => {
  try {

      const response = await axios.post(
        `https://app.watchtime.com.br/api/wpp/envia_OS`,selectedService.value
      );      
      if(response.data == null){
        Notify.create({
              type: 'positive',
              message: `Whatsapp enviado`
            });

      }
      else{
        Notify.create({
              type: 'warning',
              
              message: `${response.data.error}`
            });

      }
    }catch(error){Notify.create({
              type: 'negative',
              message: `Erro`
            });
    }

  }
  const handleEnviarEmail = async (type) => {
  try {

      const response = await axios.post(
        `https://app.watchtime.com.br/api/mail/via_cliente`,selectedService.value
      );      
      if(response.data!= undefined){
        Notify.create({
              type: 'positive',
              message: `E-mail enviado`
            });

      }
      else{
        Notify.create({
              type: 'warning',
              
              message: `${response.data.error}`
            });

      }
    }catch(error){Notify.create({
              type: 'negative',
              message: `Erro`
            });
    }

  }

  const handleEnviarOrcamento = async (type) => {
  try {

      const response = await axios.post(
        `https://app.watchtime.com.br/api/mail/orcamento`,selectedService.value
      );      
      if(response.data!= undefined){
        Notify.create({
              type: 'positive',
              message: `E-mail enviado`
            });

      }
      else{
        Notify.create({
              type: 'warning',
              
              message: `${response.data.error}`
            });

      }
    }catch(error){Notify.create({
              type: 'negative',
              message: `Erro`
            });
    }

  }


  const handleGerarHistorico = async (titulo,texto) => {
    const dataToSubmit = {
    texto: texto,
    os:selectedService.value.codigo_estoklus,
    cliente:selectedService.value.cliente_id,
    titulo:titulo
  };
  try{
    const response = await axios.post(
        `https://app.watchtime.com.br/api/estoklus/historico`,dataToSubmit
      );
      
      if(response.status == 200){
        Notify.create({
              type: 'positive',
              message: `Histórico gravado na OS ${selectedService.value.codigo_estoklus}`
            });
      }
    
  }catch(error){Notify.create({
              type: 'negative',
              message: `Erro ao gravar Histórico`
            });
    }

  }; 

  const openPDFInNewTab = async (dados, type) => {
  try {
    const response = await axios.post(`https://app.watchtime.com.br/api/pdf/${type}`, dados, { responseType: 'blob' });
    
    // Convert the Blob into a Object URL
    const pdfBlob = new Blob([response.data], { type: 'application/pdf' });
    const pdfUrl = URL.createObjectURL(pdfBlob);

    // Abre uma nova janela/tab com o PDF
    const newWindow = window.open(pdfUrl, `_blank`);
    if (newWindow == null || typeof(newWindow)=='undefined') {
      Notify.create({
        type: 'negative',
        message: 'Por favor, permita pop-ups para visualizar o PDF.'
      });
    } 

  } catch (error) {
    Notify.create({
      type: 'negative',
      message: 'Erro ao IMPRIMIR a OS'
    });
  }
}


const getCustomerData = async (customer_id, data) => {
  try {
    let request = {
      "filter":customer_id,
      "data": data
    }
    const response = await axios.post(`https://app.watchtime.com.br/api/customers/fetch_data`, request);
    selectedService.value.metodo_envio = response.data.result
    return response.data.result
  }
  catch(error){

  }
  }

const sendEmail = async (dados, type) => {
  try {
    const response = await axios.post(`https://app.watchtime.com.br/api/mail/${type}`, dados);
   
    if (response.data == 'OK'){
        Notify.create({
          type: 'negative',
          message: 'Por favor, permita pop-ups para visualizar o PDF.'
        });
        
    } 

  } catch (error) {
    Notify.create({
      type: 'negative',
      message: 'Erro ao enviar E-mail'
    });
  }
}
const sendWPP = async (dados, type) => {
  try {
    const response = await axios.post(`https://app.watchtime.com.br/api/wpp/${type}`, dados);
    
    if (response.data == 'OK'){
        Notify.create({
          type: 'positive',
          message: 'Whatsapp enviado'
        });
        
    } 

  } catch (error) {
    Notify.create({
      type: 'negative',
      message: 'Erro ao enviar E-mail'
    });
  }
}



  const openHTMLInNewTab = async (dados, type) => {
  try {
    const response = await axios.post(`https://app.watchtime.com.br/api/html/${type}`, dados);
    const htmlContent = response.data.html;
    // Abre uma nova janela e escreve o conteúdo HTML
    const newWindow = window.open('', `${type} - ${dados.id}`);
    newWindow.document.open();
    newWindow.document.write(htmlContent);
    newWindow.document.close();
    openPDFInNewTab(dados,type)
   
   
  } catch (error) {
    Notify.create({
      type: 'negative',
      message: `Erro ao IMPRIMIR a OS`
    });
  }
}



const syncEstoklus = async (props) => {
  try {
    const response = await axios.post(`https://app.watchtime.com.br/api/service_orders/atualizar/`+props.row.codigo_estoklus);
    if(response.status == 200){
        Notify.create({
              type: 'positive',
              message: `OS ${props.row.codigo_estoklus} atualizada, faça a pesquisa novamente`
            });
            let oldValue = search.value.text
            search.value.text = ''
            search.value.text = oldValue

      }else{
        Notify.create({
              type: 'negative',
              message: `Erro ao atualizar a OS`
            });

      }

  } catch (error) {
    console.error(error);
  }
}

  const handleReprovarOS = async (value) => {
    try {

      const response = await axios.post(
        `https://app.watchtime.com.br/api/estoklus/reprovar_os`,selectedService.value
      );      
      if(response.status == 200){
        Notify.create({
              type: 'positive',
              message: `OS Reprovada com sucesso`
            });
          
      }
      else{
        Notify.create({
              type: 'warning',

              message: `Erro`
            });
          
      }
      }catch(error){Notify.create({
              type: 'negative',
              message: `Erro`
            });
      }


  }

const handleEnviarOficina = async (value) => {
  try {
    
    selectedService.value.texto_laboratorio = value
      const response = await axios.post(`https://app.watchtime.com.br/api/estoklus/liberado_execucao`,selectedService.value)
      if(response.data.success != undefined){
        Notify.create({
              type: 'positive',
              message: `OS Atualizada`
            });

      }
      else{
        Notify.create({
              type: 'warning',
              
              message: `Erro`
            });

      }
    }catch(error){Notify.create({
              type: 'negative',
              message: `Erro ao emitir NF`
            });
    }

  };  const sincronizarOS = async () => {
  try {
      loading.value = true
      const response = await axios.get(`https://app.watchtime.com.br/api/estoklus/atualizar/novo`)
      if(response.data == "OK"){
        Notify.create({
              type: 'positive',
              message: `OS's Atualizadas`
            });

      }
      else{
        Notify.create({
              type: 'warning',
              
              message: `Erro`
            });

      }
    }catch(error){Notify.create({
              type: 'negative',
              message: `Erro`
            });
    }
    loading.value = false
  }

  </script>


  