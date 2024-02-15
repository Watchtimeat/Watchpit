<template>
  <modal-form title="Devolução" v-model:show="showDevolution">

    <div class="column" style="max-width: 10% ">
      <div class="text-h6">Notas </div> 
    </div>
    <div class="q-gutter-md row items-center q-mt-md" v-for="item in itens">
      <q-input outlined stack-label label="Código do Produto" type="text" v-model="item.referencia_produto" color="grey-7" style="width:10%" />
      <q-input outlined stack-label label="OS" type="text" v-model="item.codigo_os" color="grey-7" style="width:10%"/>
      <q-input outlined stack-label label="NF Entrada (Cliente)" type="text" v-model="item.nf_cliente" color="grey-7" style="width:10%"/>
      <q-input outlined stack-label label="NF Entrada (Estoklus)" type="text" v-model="item.nf_estoklus" color="grey-7" style="width:10%"/>
      <q-input outlined stack-label label="Valor"  v-model.number="item.valor_produto" type="number" step="0.01" color="grey-7" style="width:10%"/>
      <q-input outlined stack-label label="Quantidade de OS devolvida" type="text" v-model="item.quantidade_devolvida" color="grey-7" readonly style="width:10%" />
      <q-input outlined stack-label label="Qtde de OS NF" type="text" v-model="item.quantidade_recebida" color="grey-7" readonly style="width:10%"/>
      <q-input outlined stack-label label="Tipo Devolução" type="text" v-model="item.devolucao" color="grey-7" style="width:10%" />
       <q-btn color="green" :disabled="item.valor_produto == 0 || (item.nf_cliente == 0 && item.nf_estoklus == 0)" v-if="!item.inserido" @click="inserirItem(item)" icon="arrow_drop_down" class="q-mt-md" style="height:5px;width:5px"/>
    </div>
   
      <q-list class ="q-mt-md" bordered outlined padding>
          <q-toolbar class="bg-primary text-black shadow-2">
          <q-toolbar-title class="bg-primary">Itens da Nota - Cliente: {{ cabecalho.nome }}</q-toolbar-title>
        </q-toolbar>
        <q-item-label class="text-h4 bg-primary text-black shadow-2">Valor total NF: R${{data.total_nf.toFixed(2)}}</q-item-label>
      
          <q-item v-for="item in itens_nf" clickable v-ripple>
            <q-item-section bg-primary text-black shadow-2>
              <q-item-label style="text-dark">Relógio {{item.marca}} REF: {{item.referencia_produto}} SERIE: {{item.serie}} OS {{item.codigo_os}} OS CLIENTE: {{item.referencia_os_cliente}}</q-item-label>
              <q-item-label caption> VALOR: {{ item.valor_produto.toFixed(2) }}
              </q-item-label>
              
              
            </q-item-section>
            
            <q-btn v-if="item.inserido"  color="red" @click="removerItem(item)" icon="remove" class="q-mt-md" style="height:5px;width:5px"/>
            <q-separator spaced />
          </q-item>
         
          <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey">Sem opções</q-item-section>
          </q-item>
        </template>
      </q-list>

      <q-input outlined label="Informações complementares" type="textarea" v-model="data.info_complementar" color="grey-7" class="q-mt-md"/>
      <q-btn color="red" @click="inserirNF()" label="Gravar NF" :loading="loading" :disabled="itens_nf.length == 0" class="q-mt-sm" />
            
  </modal-form>
</template>

<script setup>
import { computed, ref} from "@vue/reactivity";
import {watchEffect,watch,onMounted} from "vue";
import { debounce } from 'lodash';
import { toLocalISOString } from "../../functions";
import { useQuasar } from "quasar";
import OrdersServicesService from "../../services/Services";
import PurchaseOrdersService from "../../services/PurchaseOrdersService";
import ModalForm from "../../components/modal-os-form.vue";
import ModalDialog from "../../components/modal-dialog-orc.vue";
import CameraModal from "../../components/CameraModal.vue";
import axios from "axios";
import ErrorDialog from '../../types/ErrorDialog.vue';
import { Notify } from 'quasar';
import AuthService from "../../services/AuthService";
const props = defineProps(["showDevolution",'itens','cabecalho']);
const emit = defineEmits(["update:showDevolution", "update:modelValue","confirm","modalClosed"]);
const data = ref(props.data)
const os = ref([])
const itens_nf = ref([])
const nf = ref([])
const loading = ref(false)
const showDevolution = computed({
  get: () => {
    data.value = {
      info_complementar:'',
      total_nf: 0,
      
    };
    os.value = props.cabecalho
    return props.showDevolution;
  },
  set: (value) => {
    emit("update:showDevolution", value);
  },
});

watch(() => props.showDevolution, (newValue) => {
  if (newValue == false){
    data.total_nf =0
    itens_nf.value = []
  }
});

function inserirItem(value){
    value.inserido = true
    data.value.info_complementar = ''

    value.descricao = `Relógio ${value.marca} REF: ${value.referencia_produto} SERIE: ${value.serie} OS ${value.codigo_os} OS CLIENTE: ${value.referencia_os_cliente}`
    itens_nf.value.push(value)
    itens_nf.value.forEach(item => {
    data.value.info_complementar  += `Devolução ${item.devolucao} - NF ${item.nf_cliente} - OS LOJA: ${item.referencia_os_cliente} \n`
    }
    
);
    data.value.total_nf += value.valor_produto

}function removerItem(remover){
  itens_nf.value = itens_nf.value.filter((value) => value.codigo_os !== remover.codigo_os);
  remover.inserido = false
  data.value.info_complementar = ''
  itens_nf.value.forEach(item => {
    data.value.info_complementar  += `Devolução ${item.devolucao} - NF ${item.nf_cliente}\n`
    })
    
  

    data.value.total_nf -= remover.valor_produto

  }const inserirNF = async () => {
      loading.value = true
      data.value.itens = itens_nf.value
      data.value.tipo_pessoa = os.value.codigo_tipo_pessoa
      data.value.cliente_id = os.value.cliente_id
      data.value.loja = os.value.loja
      data.value.tipo_entrada = 'S'
      try {
    const response = await axios.post(
      `https://app.watchtime.com.br/api/estoklus/nf_remessa`,
      data.value
    );
    if (response.data){
      Notify.create({
              type: 'positive',
              message: `NF ${response.data} criada no estoklus`
            })
          
      emit("update:showDevolution", false);
    }
  }

    catch(error){
      Notify.create({
              type: 'negative',
              message: `Erro ao emitir NF`
            })
    }

    loading.value = false
    itens_nf.value = []
    data.value = []
  }



    
  





</script>

<style scoped>
.custom-dialog-size {
  width: 1000px; /* Defina a largura que desejar */
  height: 1000px; /* Defina a altura que desejar */
}

.input-error {
    border: 2px solid red;
}
.smaller-input .q-field__native {
  font-size: 5px; /* Adjust to desired size */
  height: 10px; /* Adjust to desired height */
}
</style>
