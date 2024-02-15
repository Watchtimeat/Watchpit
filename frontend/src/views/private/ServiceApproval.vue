<template>
    <modal-form title="Aprovação" v-model:show="showApproval">

      <div class="text-h7 flex flex-center">OS {{ data.id }} </div>
      <q-card class="items-center content-center q-pa-none ">
        <div class="full-width row  justify-evenly items-end content-end  q-my-lg" style="height:50%"> 
                  <q-input outlined style="width: 250px;" class="q-my-lg column" v-if="[2,5,7].includes(data.tipo_reparo) && data.brand_id && ['CA','BA','MB','OP','PI','JC','VC','PA'].includes(data.brand_id)" v-model="data.contrato_richemont" label ="Valor contrato Richemont" bordered>
                    <template v-slot:append><span style="font-size: 12px;">R$</span></template>
                  </q-input>
                  <q-input outlined label="Prazo" style="width: 100px;" class="q-my-lg column" v-model="data.prazo">
                    <template v-slot:append><span style="font-size: 12px;">dias</span></template>
                  </q-input>
                  <q-input outlined label="Prazo" style="width: 200px;" class="q-my-lg column" v-model="data.prazo_cx">
                    <template v-slot:append><span style="font-size: 12px;">C.Aux</span></template>
                  </q-input>
                  <q-input outlined label="Prazo 2" style="width: 200px;" class="q-my-lg column" v-model="data.prazo2">
                    <template v-slot:append><span style="font-size: 12px;">C.Aux</span></template>
                  </q-input>

                  <q-input outlined label="Garantia" style="width: 400px;" class="q-my-lg column" v-model="data.garantia">
                    <template v-slot:append><span style="font-size: 12px;">Cx.Aux</span></template>
                  </q-input>

                  <q-select label="Aprovador" outlined input-debounce="0" emit-value :options="UsersFiltered" v-model="data.aprovador" use-chips stack-label use-input color="grey-7" class="q-my-lg" @filter="filterUsers"/>
            </div>
            <div class="full-width row inline justify-evenly items-center content-center ">
              <div class="column">
              <q-input outlined label="Observação" class="q-my-lg" type="text" v-model="data.observacao_aprovacao"></q-input>
              <q-input outlined label="Contato" class="q-my-lg" type="text" v-model="data.contato_aprovacao"></q-input>
            </div>
                <q-card class=" q-my-lg" bordered style="width:30%;height:30%">
                  <div class="text-h6 flex flex-center">Histórico </div>
                <q-input outlined label="Título"  class="row q-mt-md" v-model="data.titulo_historico"></q-input>
              <q-input outlined label="Texto" class="row q-mt-md" type="textarea"  v-model="data.texto_historico"></q-input>
              <q-card-section class="flex flex-center flex-column">
                <q-btn color="green" label="inserir" @click="inserirHistorico()" :disable="!data.titulo_historico || !data.texto_historico"/>
              </q-card-section>
            </q-card>
              
            
            <q-card class="q-my-lg" bordered style="width:30%;height:30%">
  
    <div class="text-h6 flex flex-center flex-column">Financeiro </div>
    <q-input outlined label="Valor" input-debounce="300" class="row q-mt-md" hint="para valores com vírgula utilizar ponto - exemplo 10.50 ou invés de 10,50" v-model.number="data.valor_sinal"></q-input>
    <q-select label="Forma de Pagamento" outlined input-debounce="0" :options="pagamentosFiltered" v-model="data.forma_pagamento" use-chips stack-label use-input color="grey-7" class="q-my-lg" @filter="filterPagamentos"/>
    <q-input outlined label="Observação Financeiro" class="row q-mt-md" v-model="data.observacao_financeiro"></q-input>
    <q-card-section class="row q-mt-md justify-evenly">
      <q-input outlined label="Já Recebeu" style="width:30%" type="decimal"  readonly v-model="data.valor_pago">
        <template v-slot:label>
          <span class="q-px-sm bg-positive text-white text-italic rounded-borders">Recebido</span>
        </template></q-input>
      <q-input outlined label-slot  style="width:30%" text-color="red" type="decimal"  readonly v-model="data.valor_restante">
        <template v-slot:label>
          <span class="q-px-sm bg-negative text-white text-italic rounded-borders">Faltando</span>
        </template>
      </q-input>
      <q-input outlined label="Total a Receber" style="width:30%" type="decimal" readonly v-model="data.valor_cliente"></q-input>
    </q-card-section>
    <q-card-section class="flex flex-center flex-column">
    <q-btn color="green" label="inserir" :loading="loadingFinanceiro" @click="inserirFinanceiro()" :disable="!data.forma_pagamento ||  !data.valor_sinal || data.valor_sinal== 0"/>
  </q-card-section>
</q-card>
            </div>
            <div class="full-width row inline q-my-lg justify-center items-center content-center ">
      <q-input label="Total Bruto" class="q-pa-sm"  outlined v-model="data.total_bruto" readonly >
      <template v-slot:append><span style="font-size: 12px;">R$</span></template></q-input>
      <q-input label="Desconto" v-if="porcDesconto" :value="formatToTwoDecimals(data.desconto)" type="number" class="q-pa-sm" outlined v-model="data.desconto"   >
      <template v-slot:append>    <q-toggle
        v-model="porcDesconto"
        checked-icon="percent"
        color="green"
        unchecked-icon="attach_money"
      /></template></q-input>
     <q-input label="Desconto" v-if="!porcDesconto" type="number" class="q-pa-sm" outlined v-model="data.valor_desconto_todos"   >
      <template v-slot:append> <q-toggle
        v-model="porcDesconto"
        checked-icon="percent"
        color="green"
        unchecked-icon="attach_money"
      /></template>
    </q-input>



      <q-input label="Total a receber"  class="q-pa-sm" outlined v-model="data.valor_cliente" readonly  >
      <template v-slot:append><span style="font-size: 12px;">R$</span></template></q-input>

   
    </div>
      </q-card>
      <div class="full-width row inline no-wrap justify-evenly items-center content-center  q-mt-md">
                  <q-input @keydown.enter="inserirOrcamento('OB',data.peca)"  @keydown.shift="inserirOrcamento('I',data.peca)" @keydown.alt="inserirOrcamento('OP',data.peca)" 
                    label="Produto"  
                    style="width:20%" 
                    class="q-pa-none"
                    v-model="data.peca"
                  >
                    <q-btn :loading="loading" color="grey-9" @click="inserirOrcamento('OP',data.peca)" label="OP" class="q-mt-md" style="height:5px;width:5px">
                      <q-tooltip>Opcional</q-tooltip></q-btn>
                    <q-btn :loading="loading" color="grey-8" label="I" class="q-mt-md" @click="inserirOrcamento('I',data.peca)" style="height:5px;width:5px">
                      <q-tooltip>Incluso no serviço</q-tooltip></q-btn>
                    <q-btn :loading="loading" color="grey-7" @click="inserirOrcamento('OB',data.peca)" label="OB" class="q-mt-md" style="height:5px;width:5px">
                      <q-tooltip>Obrigatório</q-tooltip></q-btn>
                  </q-input>

                  
                  <div class="row">
                  <q-select label="Serviço" outlined input-debounce="0" fixed emit-value  style="text-overflow: ellipsis !important;white-space: nowrap !important; overflow: hidden !important;width: 300px!important;align-self: center;" :options="ServicosFiltered" v-model="data.servico" wrap use-input color="grey-7"   @filter="filterServicos" />
                  <q-btn color="grey-9" :loading="loading" @click="inserirOrcamento('SO','')" label="OP"  style="align-self: center;height:5px;width:5px" :disable="!data.servico">
                      <q-tooltip>Serviço opcional</q-tooltip>
                      <q-tooltip v-if="!data.servico">Serviço não selecionado!</q-tooltip></q-btn>
                  <q-btn color="grey-7" :loading="loading" @click="inserirOrcamento('S','')" label="OB" :disable="!data.servico" style="align-self: center;height:5px;width:5px">
                      <q-tooltip>Serviço obrigatório</q-tooltip>
                      <q-tooltip v-if="!data.servico">Serviço não selecionado!</q-tooltip></q-btn>
                  </div>
                </div>
                <div class = "q-mt-md" > 
                  <q-separator/> 
                </div>
                
                <div class="full-width row inline no-wrap justify-center items-center content-center  q-mt-md">
                    <div class="row text-h6"> Item Genérico </div>
                </div>
                <div class="full-width row inline no-wrap justify-evenly items-center content-center">
                    <q-input label="Referência" style="width:20%" class="q-mt-md" v-model="data.peca_generica_referencia" />
                      <q-input label="Descrição" style="width:40%" class="q-mt-md" v-model="data.peca_generica_descricao" />
                      <q-input label="Valor" style="width:20%" class="q-mt-md" v-model.number="data.peca_generica_valor" />
                      <div>
                        <q-btn color="grey-7" @click="inserirOrcamento('GO',data.peca)" label="OB" class="q-mt-md" :disable="!data.peca_generica_descricao" style="height:5px;width:5px">
                          <q-tooltip v-if="!data.servico">Descrição não preenchida!</q-tooltip></q-btn>
                        <q-btn color="grey-9" @click="inserirOrcamento('GOP',data.peca)" label="OP" class="q-mt-md" :disable="!data.peca_generica_descricao " style="height:5px;width:5px">
                          <q-tooltip v-if="!data.servico">Descrição não preenchida!</q-tooltip></q-btn>
                        <q-btn color="grey-7" @click="inserirOrcamento('GSO',data.peca)" label="S" class="q-mt-md" :disable="!data.peca_generica_descricao  " style="height:5px;width:5px">
                          <q-tooltip v-if="!data.servico">Descrição não preenchida!</q-tooltip></q-btn>
                        <q-btn color="grey-9" @click="inserirOrcamento('GSOP',data.peca)" label="SOP" class="q-mt-md" :disable="!data.peca_generica_descricao  "  style="height:5px;width:5px">
                          <q-tooltip v-if="!data.servico">Descrição não preenchida!</q-tooltip></q-btn>
                      </div>
                  </div>

<q-card style="width:100%" class="q-mt-md">
      <q-card-section>
      
        <q-card-section >
                <div class="full-width row inline no-wrap justify-between items-start content-start  q-mt-md">
                  
                  
                  <div class="text-h6" style ="min-width:49%">Itens Obrigatórios / Indispensáveis
                    <div class="column">
                      <q-table
                      style="height: 400px; max-width:100%"
                      flat bordered
                      ref="tableRef"
                      :rows="Obrigatorios"
                      :columns="columns"
                      :table-colspan="2"
                      row-key="referencia"
                      virtual-scroll
                      :virtual-scroll-item-size="48"
                      :pagination="pagination"
                      :rows-per-page-options="[0]"
                      :filter="filter"
                    >
                    <template v-slot:top-left>
                        <q-input background="blue" dense debounce="300" v-model="filter" placeholder="Pesquisa">
                          <template v-slot:append>
                            <q-icon name="search" />
                          </template>
                        </q-input>
                      </template>
                      <template v-slot:top-right>
                        <q-btn v-if="!editando" class="q-mt-md" color="grey-8" @click="edita('S')" icon="edit" style="align: left !important;height:1px !important;width:1px !important"/>
                        <q-btn v-if="editando" class="q-mt-md" color="green" @click="edita('N')" icon="done" style="height:5px;width:5px"/>
                      </template>

                      <template v-slot:body="props">
        <q-tr :props="props" :class="getBackgroundColor(props.row)">
          <q-tooltip v-if="props.row.tipo == 'S'">Serviço</q-tooltip>
          <q-tooltip v-else>Peça</q-tooltip>
          <q-td>
            <q-btn color="red" @click="remove('OB',props.row)" icon="remove" style="align-self: center; height:2px;width:2px"/>
          </q-td>
          <q-td :class="getBackgroundColorRow(props.row)">
            {{ props.row.referencia }}
            <q-popup-edit v-if="editando"  v-model="props.row.referencia" buttons persistent v-slot="scope">
              <q-input type="number" v-model="scope.value" dense autofocus hint="Itens sem custo são obrigatórios ser preenchido" />
            </q-popup-edit>
            <q-tooltip v-if="props.row.generico == 'S'">Item Genérico</q-tooltip>
          </q-td>
          <q-td>
            {{ props.row.quantidade }}
            <q-popup-edit v-if="editando"  v-model="props.row.quantidade" buttons persistent v-slot="scope">
              <q-input type="number" v-model.number="scope.value" dense autofocus hint="Quantidade não pode ser 0" />
            </q-popup-edit>
          </q-td>
          <q-td>
            {{ props.row.preco_venda }}
            <q-popup-edit v-if="editando" @save="newValue => updateValueInTodos(props.row, newValue)" v-model="props.row.preco_venda" buttons persistent v-slot="scope">
              <q-input type="number" v-model.number="scope.value" dense autofocus hint="Itens sem custo são obrigatórios ser preenchido" />
            </q-popup-edit>
          </q-td>
          <q-td>
            {{ props.row.preco_custo }}
            <q-popup-edit v-if="editando"  v-model="props.row.preco_custo" buttons persistent v-slot="scope">
              <q-input type="number" v-model.number="scope.value" dense autofocus hint="Itens sem custo são obrigatórios ser preenchido" />
            </q-popup-edit>
          </q-td>
          <q-td>
            {{ props.row.estoque }}

          </q-td>
          <q-td>
            {{ props.row.label }}
            <q-popup-edit v-if="editando" v-model="props.row.label" @save="newValue => updateLabelInTodos(props.row, newValue)" v-slot="scope" buttons >
              <q-input type="text" v-model="scope.value" dense autofocus hint="Alterar Descrição" />
            </q-popup-edit>
          </q-td>
        </q-tr>
      </template>
                    </q-table>

  
                      </div>              
                    </div>
                  <div class="text-h6" style ="width:49%">Itens Opcionais
                    <q-table
                      style="height: 400px; max-width:100%"
                      flat bordered
                      ref="tableRef"
                      :rows="Opcionais"
                      :columns="columns"
                      :table-colspan="2"
                      row-key="referencia"
                      virtual-scroll
                      :virtual-scroll-item-size="48"
                      :pagination="pagination"
                      :rows-per-page-options="[0]"
                      :filter="filter"
                    >
                    <template v-slot:top-left>
                        <q-input background="blue" dense debounce="300" v-model="filter" placeholder="Pesquisa">
                          <template v-slot:append>
                            <q-icon name="search" />
                          </template>
                        </q-input>
                      </template>
                      <template v-slot:top-right>
                        <q-btn v-if="!editando" class="q-mt-md" color="grey-8" @click="edita('S')" icon="edit" style="align: left !important;height:1px !important;width:1px !important"/>
                        <q-btn v-if="editando" class="q-mt-md" color="green" @click="edita('N')" icon="done" style="height:5px;width:5px"/>
                      </template>
                      <template v-slot:body="props">
                        <q-tr :props="props" :class="getBackgroundColor(props.row)">
          <q-tooltip v-if="props.row.tipo == 'SO'">Serviço</q-tooltip>
          <q-tooltip v-else>Peça</q-tooltip>
          <q-td>
            <q-btn color="red" @click="remove('OP',props.row)" icon="remove" style="align-self: center; height:2px;width:2px"/>
          </q-td>
          <q-td>
            {{ props.row.referencia }}
            <q-popup-edit v-if="editando"  v-model="props.row.referencia" buttons persistent v-slot="scope">
              <q-input type="number" v-model="scope.value" dense autofocus hint="Itens sem custo são obrigatórios ser preenchido" />
            </q-popup-edit>
          </q-td>
          <q-td>
            {{ props.row.quantidade }}
            <q-popup-edit v-if="editando"  v-model="props.row.quantidade" buttons persistent v-slot="scope">
              <q-input type="number" v-model.number="scope.value" dense autofocus hint="Itens sem custo são obrigatórios ser preenchido" />
            </q-popup-edit>
          </q-td>
          <q-td>
            {{ props.row.preco_venda }}
            <q-popup-edit v-if="editando" @save="newValue => updateValueInTodos(props.row, newValue)" v-model="props.row.preco_venda" buttons persistent v-slot="scope">
              <q-input type="number" v-model.number="scope.value" dense autofocus hint="Itens sem custo são obrigatórios ser preenchido" />
            </q-popup-edit>
          </q-td>
          <q-td>
            {{ props.row.preco_custo }}
            <q-popup-edit v-if="editando"  v-model="props.row.preco_custo" buttons persistent v-slot="scope">
              <q-input type="number" v-model.number="scope.value" dense autofocus hint="Itens sem custo são obrigatórios ser preenchido" />
            </q-popup-edit>
          </q-td>
          <q-td>
            {{ props.row.estoque }}
            <q-popup-edit v-if="editando"  v-model="props.row.estoque" buttons persistent v-slot="scope">
              <q-input type="number" v-model.number="scope.value" dense autofocus hint="Itens sem custo são obrigatórios ser preenchido" />
            </q-popup-edit>
          </q-td>
          <q-td>
            {{ props.row.label }}
            <q-popup-edit v-if="editando"  v-model="props.row.label" @save="newValue => updateLabelInTodos(props.row, newValue)" buttons persistent v-slot="scope">
              <q-input type="text" v-model="scope.value" dense autofocus hint="Itens sem custo são obrigatórios ser preenchido" />
            </q-popup-edit>
          </q-td>
        </q-tr>
      </template>
                    </q-table>
                  </div>
                     
                </div>
               </q-card-section>  
               <div class="row">
             
             <q-btn label="Aprovar OS" color="green" :loading="loading" @click="aprovarOrcamento()"></q-btn>   
             <q-select v-if="data.loja == 'RJ'" label="Status Aprovação" class="q-pa-lg" outlined input-debounce="0" style="width:14%" fixed emit-value  :options="StatusAprovacao" v-model="data.status_aprovacao" wrap color="grey-7" />  
            </div>
              </q-card-section>  
</q-card>

{{data}}

</modal-form>

</template>

<script setup>
import { computed, ref} from "@vue/reactivity";

import {watch} from 'vue';
import ModalForm from "../../components/modal-os-form.vue";
import axios from "axios";
import { Notify } from 'quasar';
import AuthService from "../../services/AuthService";
import { useQuasar } from "quasar";
import OrdersServicesService from "../../services/Services";
import { debounce } from 'lodash';


const loadingFinanceiro = ref(false)
const $q = useQuasar();
const UsersFiltered = ref([])
const loading = ref(false)
const selected = ref([])
const       pagination = {
        rowsPerPage: 0
      }
const columns = [{ name: ' ', align: 'left', label: '  ', field: 'referencia', sortable: true },
  { name: 'Referência', align: 'left', label: 'Referência', field: 'referencia', sortable: true },
{name: 'Quantidade', align: 'left', label: 'Q', field: 'quantidade', sortable: true},
{name: 'Valor', align: 'left', label: 'V', field: 'preco_venda', sortable: true},
{name: 'Custo', align: 'left', label: 'C', type:'cost',field: 'preco_custo', sortable: true},
{name: 'Estoque', align: 'left', label: 'ST', field: 'estoque', sortable: true},
{name: 'Descrição', align: 'left', label: 'Descrição', field: 'label', sortable: true}]
const  filter = ref('')
const props = defineProps(["showApproval", "modelValue"]);
const emit = defineEmits(["update:showApproval", "update:modelValue", "confirm","modalClosed"]);
const data = ref({

});
const porcDesconto = ref(true)
const currentUser = computed(() => AuthService.user);
const Obrigatorios = ref([]);
const Todos = ref([]);
const Opcionais = ref([]);
const editando = ref(false)
const estoklusUsers = ref([]);
const FormasPagamento = ref([]);
const pagamentosFiltered = ref([])
const Servicos = ref([]);
const ServicosFiltered = ref([]);
const codigo_item = ref(1);
const StatusAprovacao = ref([{
  value:'03',label:'Aprovado'
},{
  value:'05',label:'Aguardando Peças'
}])

function formatToTwoDecimals(value) {
    return parseFloat(value).toFixed(2);
}
const fetchPagamentos = async () => {
  try {
    const response = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/pagamentos`, 
      );
      const options = response.data.map(item => ({
        id: item.codigo_forma_pagamento,
        label: `${item.descricao_forma_pagamento} - ${item.codigo_forma_pagamento}`
      }));
      FormasPagamento.value = options
  
  
  }
  catch{

  }


}

const fetchFinanceiro = async () => {
  try {
    const response = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/financeiro/${data.value.codigo_estoklus}`, 
      );
      
        data.value.valor_pago = response.data[0].valor_pago
        data.value.valor_restante = response.data[0].valor_restante
        data.value.valor_receber = response.data[0].valor_receber
  
  
  }
  catch{

  }


}

function filterServicos(val, update) {
  if (val === "") {
    update(() => {
      ServicosFiltered.value = Servicos.value;
    });
    return;
  }

  update(() => {
    ServicosFiltered.value = Servicos.value.filter(
      (user) => user.label.toLowerCase().indexOf(val.toLowerCase()) > -1
    );
  });
}

const fetchOrcamento = async (val, update) => {
  try {
      const response = await axios.get(
        `https://app.watchtime.com.br/api/service_orders/analisar/`+data.value.codigo_estoklus, 
      );

      const options = response.data.map(item => ({
        id: item.id,
        nome: item.label,
        referencia: item.referencia
      }));
      let index = 0
      response.data.forEach(item => {
        if (item.tipo === 'S' || item.tipo === 'P' || item.tipo == 'I') {
          Obrigatorios.value.push({
            quantidade: item.quantidade,
            label: item.label,
            referencia: item.referencia,
            preco_custo: item.preco_custo,
            preco_venda: item.preco_venda,
            estoque: item.estoque,
            index:index,
            id:item.id,
            tipo:item.tipo.trim(),
            generico: item.id == '0000801' ? 'S' : 'N'

          });
          data.value.desconto = item.desconto
        }        if (item.tipo === 'OP' || item.tipo === 'SO') {
          Opcionais.value.push({
            quantidade: item.quantidade,
            label: item.label,
            referencia: item.referencia,
            preco_custo: item.preco_custo,
            preco_venda: item.preco_venda,
            estoque: item.estoque,
            index:index,
            id:item.id,
            tipo:item.tipo.trim(),
            generico: item.id == '0000801' ? 'S' : 'N'
          });
        }
        Todos.value.push({
            quantidade: item.quantidade,
            label: item.label,
            referencia: item.referencia,
            preco_custo: item.preco_custo,
            preco_venda: item.preco_venda,
            estoque: item.estoque,
            index:index,
            tipo:item.tipo.trim(),
            id:item.id,
            generico: item.id == '0000801' ? 'S' : 'N'
          })
        index = index+1;
      });

      const response1 = await axios.get(
        `https://app.watchtime.com.br/api/service_orders/capa/`+data.value.codigo_estoklus, 
      );
      data.value.desconto = response1.data.desconto
      data.value.prazo_cx = response1.data.prazo_cx
      if (data.value.tipo_reparo == '9'){
        data.value.garantia = ''
      }else{
      data.value.garantia = response1.data.garantia
      }
      data.value.prazo = response1.data.prazo
      data.value.aprovador = data.value.estoklus_id

      if(data.value.tipo_pessoa == 'F' || data.value.codigo_tipo_pessoa == 'F' ){
        data.value.desconto = 0
      }else{

        data.value.desconto = response1.data.desconto_pj ? response1.data.desconto_pj : 0

      }
      data.value.porc_sinal = 0
      data.value.valor_sinal =0
      data.value.diagnostico_tecnico = response1.data.diagnostico_tecnico

      


    }
   catch (err) {
    console.error("Erro ao buscar dados:", err);
  }
};

const inserirHistorico = async (val, update) => {

  const dataToSubmit = {
    texto: data.value.texto_historico,
    os:data.value.codigo_estoklus,
    cliente:data.value.cliente_id,
    titulo:data.value.titulo_historico,
  };
  try{
    const response = await axios.post(
        `https://app.watchtime.com.br/api/estoklus/historico`,dataToSubmit
      );
      
      if(response.status == 200){
        Notify.create({
              type: 'positive',
              message: `Histórico gravado na OS ${data.value.codigo_estoklus}`
            });
      }
    
  }catch{

  }finally{

    

    delete data.value.texto_historico
    delete data.value.titulo_historico
  }


}


const showApproval = computed({
  get: () => {

    if (props.showApproval == false){
        Obrigatorios.value = []
        Opcionais.value = []
        data.value = []
        Todos.value = []
        

    }
   
    
    return props.showApproval;
  },
  set: (value) => {
    emit("update:showApproval", value);
  },
  
});

function filterUsers(val, update) {
  if (val === "") {
    update(() => {
      UsersFiltered.value = estoklusUsers.value;
    });
    return;
  }

  update(() => {
    UsersFiltered.value = estoklusUsers.value.filter(
      (user) => user.label.toLowerCase().indexOf(val.toLowerCase()) > -1
    );
  });
}

function filterPagamentos(val, update) {
  if (val === "") {
    update(() => {
      pagamentosFiltered.value = FormasPagamento.value;
    });
    return;
  }

  update(() => {
    pagamentosFiltered.value = FormasPagamento.value.filter(
      (user) => user.label.toLowerCase().indexOf(val.toLowerCase()) > -1
    );
  });
}
async function loadEstoklusUsers() {
  const response = await OrdersServicesService.getUsersEstoklus();


  estoklusUsers.value = response?.map((b) => {
    return { label: b.label.toUpperCase(), value: b.id };
  });
}
const remove = async (val,itemToRemove) => {

try {
    if(val === 'OP'){
      Opcionais.value = Opcionais.value.filter((item) => item.index !== itemToRemove.index);
    }else{
      Obrigatorios.value = Obrigatorios.value.filter((item) => item.index !== itemToRemove.index);
    }
    

    Todos.value = Todos.value.filter((item) => item.index !== itemToRemove.index);
    calculaOrcamento()
} catch (err) {
  console.error("Erro ao buscar dados:", err);
}

  
};

watch(
  () => Todos.value,
  (newValue, oldValue) => {
    if (newValue != ''){ 
    data.value.itens = newValue
    callApi()
  }
  },
  { deep: true } // Esta opção permite que você observe mudanças profundas no objeto
);


watch(() => props.showApproval, (newValueAprov) => {
  if (newValueAprov == true){
    data.value = props.modelValue
    data.value.status_aprovacao = '05'
   
      loadEstoklusUsers();
       fetchOrcamento();
       fetchPagamentos();
       fetchServicos();
       fetchFinanceiro();
       data.value.estoklus_id = currentUser.value.estoklus_id

    }
});

watch(() => data.value.desconto, (newDesconto) => {
  callApi()
});

watch(() => porcDesconto.value, (newporcDesconto) => {
    if (newporcDesconto == false && (data.value.valor_desconto_todos == undefined || data.value.valor_desconto_todos == null || isNaN(data.value.valor_desconto_todos) )){
      data.value.valor_desconto_todos = data.value.total_bruto * (data.value.desconto /100)
    }
});
watch(() => data.value.desconto, (newDesconto) => {
    if (porcDesconto.value == true && data.value.desconto > 0){
      data.value.valor_desconto_todos = data.value.total_bruto * (newDesconto /100)
    }else     if (porcDesconto.value == true && newDesconto == 0){
      data.value.valor_desconto_todos = 0
    }
});
watch(() => data.value.valor_desconto_todos, (newValorDesconto) => {
    
 
    if (porcDesconto.value == false && newValorDesconto > 0){
      data.value.desconto = (data.value.valor_desconto_todos / data.value.total_bruto) * 100
    }
  
    else     if (porcDesconto.value == false && newValorDesconto == 0){
      data.value.desconto = 0
    }
});
watch(
  () => data.value.valor_sinal,
  (newvalor_sinal) => {

    
   if (data.value.valor_sinal == 0) {
    data.value.porc_sinal = 0

   } else {data.value.porc_sinal = ((parseFloat(data.value.valor_sinal) / parseFloat(data.value.valor_cliente)) * 100).toFixed(2);}
  } // 300ms é o tempo de espera. Ajuste conforme necessário.
);

async function calculaOrcamento() {
  // Cria um novo objeto que contém tanto o array de itens quanto o desconto.
  const dataToSubmit = {
    itens: Todos.value,
    desconto: parseFloat(data.value.desconto),
  };
  try {
    const response = await axios.post(
      `https://app.watchtime.com.br/api/service_orders/orc`,
      dataToSubmit
    );



    
    if(response.data) {
      // Aqui, atualizamos os valores no objeto 'data.value' com os dados da resposta.
      data.value.valor_liquido   = response.data.valor_liquido;
      data.value.valor_cliente  = response.data.valor_cliente;
      data.value.valor_margem = response.data.valor_margem;
      data.value.custo_total  = response.data.custo_total;
      data.value.total_bruto  = response.data.total_bruto;
      data.value.total_opcionais = response.data.total_opcionais;
      data.value.desconto_total = response.data.valor_desconto;
      data.value.valor_desconto_obrigatorios = response.data.valor_desconto_obrigatorios;
      data.value.total_obrigatorio = response.data.total_obrigatorio
      data.value.valor_liquido_obrigatorios = response.data.valor_liquido_obrigatorios
      data.value.valor_margem_obrigatorios = response.data.valor_margem_obrigatorios
      data.value.valor_restante = data.value.valor_cliente - data.value.valor_pago
    }
  } catch(error) {
    console.error("Houve um erro ao calcular o orçamento:", error);
  }
}

function edita(param) {
  if (param === "S") {
    editando.value = true;
  } else {
    
    let ok =  true
    // Percorrendo o array de itens
    for (let item of Todos.value) {
      if(item.generico === 'S'){
        ok = true
      }else if(['CA','BA','MB','OP','PI','JC','VC','PA'].includes(data.value.brand_id))
      {
        ok = true
      }else if([2,3,5,7].includes(data.value.tipo_reparo))
      {
        ok = true
      }

      else if (item.preco_custo == 0 || (item.preco_venda == 0 && !['I','SO','S'].includes(item.tipo))) {
        Notify.create({
              type: 'negative',
              message: `Produto ${item.referencia} sem preço de custo ou venda`
            });
          ok = false
        }
      
      }
    if(ok === true){
      editando.value = false;
    }
    }
    
}
const aprovarOrcamento = async () => {
  loading.value = true
  data.value.itens = Todos.value
  if (data.value.valor_desconto_todos == undefined || data.value.valor_desconto_todos == null || isNaN(data.value.valor_desconto_todos) ){
      data.value.valor_desconto_todos = data.value.total_bruto * (data.value.desconto /100)
  }
  const response = await axios.post('https://app.watchtime.com.br/api/estoklus/aprovar_os',data.value)
  if(response.status == 200){
    Notify.create({
              type: 'positive',
              message: `OS ${data.value.codigo_estoklus} aprovada - Previsão ${response.data.data_previsao} `
            });
    data.value.valor_liquido = data.value.valor_cliente

    emit("update:showApproval", false);
  
  } else {
    Notify.create({
              type: 'negative',
              message: `Erro`
            });

  }
  loading.value = false

}

const inserirFinanceiro = async () => {
  loadingFinanceiro.value = true
  let tipo = ''
  if (data.value.valor_sinal < data.value.valor_receber){
    tipo = 'ADIANTAMENTO'
  } else {
    tipo = 'RESIDUAL'
  }
  

  if (data.value.observacao_financeiro == undefined){
    data.value.observacao_financeiro = ''
  }
  let request = {
    valor: data.value.valor_sinal,
    forma_pagamento: data.value.forma_pagamento.id,
    tipo: tipo,
    usuario: data.value.estoklus_id,
    observacao: data.value.observacao_financeiro,
    loja: data.value.loja

  }
  const response = await axios.post(`https://app.watchtime.com.br/api/estoklus/financeiro/${data.value.codigo_estoklus}`,request)
  if(response.status == 200){
    Notify.create({
              type: 'positive',
              message: `Financeiro da OS ${data.value.codigo_estoklus} gravado`
            });
            let hoje = new Date();
            // Formate a data para dd/mm/yyyy
            let dia = String(hoje.getDate()).padStart(2, '0');
            let mes = String(hoje.getMonth() + 1).padStart(2, '0'); // Janeiro é 0!
            let ano = hoje.getFullYear();
            let dataFormatada = dia + '/' + mes + '/' + ano;
            data.value.data_pgto = dataFormatada
            data.value.forma_pagto = data.value.forma_pagamento.label
            data.value.valor_pagamento = data.value.valor_sinal
            openHTMLInNewTab(data.value,'recibo')
            data.value.valor_sinal = 0
            delete data.value.forma_pagamento
            data.value.observacao_financeiro = ''
            data.value.valor_pago = response.data.sucess[0].valor_pago
            data.value.valor_restante = response.data.sucess[0].valor_restante
            data.value.valor_receber = response.data.sucess[0].valor_receber
            
            
  
  } else {
    Notify.create({
              type: 'negative',
              message: `Erro`
            });

  }

  loadingFinanceiro.value = false
}

const openHTMLInNewTab = async (dados, type) => {
  try {
    const response = await axios.post(`https://app.watchtime.com.br/api/html/${type}`, dados);
    const htmlContent = response.data;
    // Abre uma nova janela e escreve o conteúdo HTML
    const newWindow = window.open('', `${type} - ${dados.id}`);
    newWindow.document.open();
    newWindow.document.write(htmlContent);
    newWindow.document.close();
   
   
  } catch (error) {
    Notify.create({
      type: 'negative',
      message: `Erro ao IMPRIMIR a OS`
    });
  }
}

const inserirOrcamento = async (val, item) => {
  loading.value = true
  codigo_item.value=codigo_item.value+1;
  if(val === 'S'){
      
      let fields = { 
          'estoque': '-', 
          'id': data.value.servico.id, 
          'index': codigo_item.value, 
          'preco_venda': data.value.servico.preco_venda,
          'quantidade': 1,
          'referencia':data.value.servico.referencia,
          'label':data.value.servico.label,
          'tipo':'S',
        'generico':'N'}
      if (fields.preco_venda == 0 || fields.preco_venda == null ){editando.value = true; fields.preco_venda = 0 }
      Obrigatorios.value.push(fields);
      codigo_item.value=codigo_item.value+1;
      delete data.value.servico;
      Todos.value.push(fields)
  } else if(val === 'SO'){
      let fields = { 
          'estoque': '-', 
          'id': data.value.servico.id, 
          'index': codigo_item.value, 
          'preco_venda': data.value.servico.preco_venda,
          'quantidade': 1,
          'referencia':data.value.servico.referencia,
          'label':data.value.servico.label,
          'tipo':'SO',
          'generico':'N'}
        if (fields.preco_venda == 0 || fields.preco_venda == null ){editando.value = true; fields.preco_venda = 0 }
      Opcionais.value.push(fields);
      codigo_item.value=codigo_item.value+1;
      delete data.value.servico;
      Todos.value.push(fields)
  } else if(val === 'GO'){

      let referencia = ''
      if(data.value.peca_generica_referencia){
        referencia = data.value.peca_generica_referencia
      }
      

      let fields = { 
          'estoque': '-', 
          'id': '0000801', 
          'index': codigo_item.value, 
          'preco_venda': data.value.peca_generica_valor,
          'preco_custo': 0,
          'quantidade': 1,
          'referencia':referencia,
          'label':data.value.peca_generica_descricao,
          'tipo':'P',
        'generico':'S'}

      Obrigatorios.value.push(fields);
      codigo_item.value=codigo_item.value+1;
      data.value.peca_generica_valor = 0;
      delete data.value.peca_generica_referencia;
      delete data.value.peca_generica_descricao;
      Todos.value.push(fields)
  } else if(val === 'GSO'){

  let referencia = ''
  if(data.value.peca_generica_referencia){
    referencia = data.value.peca_generica_referencia
  }


  let fields = { 
      'estoque': '-', 
      'id': '0000801', 
      'index': codigo_item.value, 
      'preco_venda': data.value.peca_generica_valor,
      'preco_custo': 0,
      'quantidade': 1,
      'referencia':referencia,
      'label':data.value.peca_generica_descricao,
      'tipo':'S',
        'generico':'S'}

  Obrigatorios.value.push(fields);
  codigo_item.value=codigo_item.value+1;
  delete data.value.peca_generica_valor;
  delete data.value.peca_generica_referencia;
  delete data.value.peca_generica_descricao;
  Todos.value.push(fields)
  } else if(val === 'GSOP'){

  let referencia = ''
  if(data.value.peca_generica_referencia){
    referencia = data.value.peca_generica_referencia
  }
  
  
  let fields = { 
      'estoque': '-', 
      'id': '0000801', 
      'index': codigo_item.value, 
      'preco_venda': data.value.peca_generica_valor,
      'preco_custo': 0,
      'quantidade': 1,
      'referencia':referencia,
      'label':data.value.peca_generica_descricao,
      'tipo':'SO',
        'generico':'S'}
  
  Opcionais.value.push(fields);
  codigo_item.value=codigo_item.value+1;
  delete data.value.peca_generica_valor;
  delete data.value.peca_generica_referencia;
  delete data.value.peca_generica_descricao;
  Todos.value.push(fields)
  }else if(val === 'GOP'){

  let referencia = ''
  if(data.value.peca_generica_referencia){
    referencia = data.value.peca_generica_referencia
  }


  let fields = { 
      'estoque': '-', 
      'id': '0000801', 
      'index': codigo_item.value, 
      'preco_venda': data.value.peca_generica_valor,
      'preco_custo': 0,
      'quantidade': 1,
      'referencia':referencia,
      'label':data.value.peca_generica_descricao,
      'tipo':'OP',
        'generico':'S'}

  Opcionais.value.push(fields);
  codigo_item.value=codigo_item.value+1;
  delete data.value.peca_generica_valor;
  delete data.value.peca_generica_referencia;
  delete data.value.peca_generica_descricao;
  Todos.value.push(fields)
}

  else try {
      const response = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/pecas`, 
        {
          params: {referencia: item.toUpperCase()},
        }
      );
      if(response.data.length === 0){
        Notify.create({
              type: 'negative',
              message: `Produto ${item.toUpperCase()}, inexistente ou não cadastrado no estoklus`
            });

        }
      else{

        if(val === 'OP'){
            response.data[0].index= codigo_item.value
            response.data[0].quantidade = 1
            response.data[0].tipo = 'OP'
            response.data[0].generico ='N'
            Opcionais.value.push(response.data[0]);
            codigo_item.value=codigo_item.value+1
            Todos.value.push(response.data[0])
            if(response.data[0].preco_custo == 0 || response.data[0].preco_venda == 0){
              editando.value = true
            }

        }else if(val === 'OB'){
            response.data[0].index= codigo_item.value
            response.data[0].quantidade = 1
            response.data[0].tipo = 'P'
            response.data[0].generico ='N'
            Obrigatorios.value.push(response.data[0]);
            codigo_item.value=codigo_item.value+1
            Todos.value.push(response.data[0])
            if(response.data[0].preco_custo == 0 || response.data[0].preco_venda == 0){
              editando.value = true
            }
        }else if(val === 'I'){
            response.data[0].index= codigo_item.value
            response.data[0].quantidade = 1
            response.data[0].preco_venda = 0 
            response.data[0].tipo = 'I'
            response.data[0].generico ='N'
            if(response.data[0].preco_custo === 0){
              editando.value = true
            }
            Obrigatorios.value.push(response.data[0]);
          codigo_item.value=codigo_item.value+1
          Todos.value.push(response.data[0])
        }
        
        data.value.peca = ''
      }

    
    
  } catch (err) {
    console.error("Erro ao buscar dados:", err);
  }finally{
    loading.value = false
  }

  loading.value = false
};

const fetchServicos = async (val, update) => {
  try {
      if (data.value.marca == 'BAUME E MERCIER') {
        data.value.marca ='BAUMEEMERCIER'
      }  else if (data.value.marca == 'MONT BLANC') {
        data.value.marca = 'MONTBLANC'
      }        else if (data.value.marca == 'OFFICINE PANERAI') {
        data.value.marca = 'PANERAI'
      }
      const response = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/servicos/`+data.value.marca
      );

      const options = response.data.map(item => ({
        id: item.id,
        label: item.referencia + ' - ' + item.label + ' (' + item.id+')',
        referencia: item.referencia,
        preco_venda: item.preco_venda
      }));

      Servicos.value = options;

    
  } catch (err) {
    console.error("Erro ao buscar dados:", err);
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

const callApi = debounce(() => {
  if (showApproval.value == true){
    calculaOrcamento()
  }
 
  // chamar sua API aqui
}, 500); // 300 ms de delay

function getBackgroundColor(row){
  let classe
  if (['S','SO'].includes(row.tipo) ){
  classe = 'bg-green-11'
  }else {
    classe = 'bg-yellow-11'
  }
  return classe
}
function getBackgroundColorRow(row){
  let classe
  if (row.generico == 'S'){
    classe = 'bg-red-11'
  }
  return classe
}

const updateLabelInTodos = (row, newValue) => {
  const item = Todos.value.find(item => item.index === row.index || item.id === row.id);
  if (item) {
    item.label = newValue;
    // Aqui você pode adicionar qualquer lógica adicional necessária,
    // como enviar uma atualização para uma API
  }
};
const updateValueInTodos = (row, newValue) => {
  const item = Todos.value.find(item => item.index === row.index || item.id === row.id);
  if (item) {
    item.preco_venda = newValue;
    // Aqui você pode adicionar qualquer lógica adicional necessária,
    // como enviar uma atualização para uma API
  }
};
</script>