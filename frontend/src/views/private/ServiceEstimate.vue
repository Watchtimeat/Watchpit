<template>
  <modal-form title="ORÇAMENTO" v-model:show="showEstimate">
    <q-stepper
      v-model="step"
      ref="stepper"
      color="blue"
      animated
      spaced
    >
      <q-step
        :name="1"
        title="Dados do Relógio"
        icon="watch"
        :done="step > 1"
        flat color="blue" 
        animated
        ></q-step>
        <q-step
        :name="3"
        title="Informações da OS"
        icon="home_repair_service"
        :done="step > 1"
        ></q-step>
        <template v-slot:navigation>
        <q-stepper-navigation>                  
          <q-btn v-if="step < 3" @click="onSubmit(this)" type="submit" color="blue" :label="step === 3 ? 'Finish' : 'Avançar'" />
          <q-btn v-if="step === 3" color="red" @click="inserirOS()" label="Gravar OS" class="q-ml-sm" :disable="editando || data.desconto === '' || !data.prazo === '' || !data.prazo_cx" />
          <q-btn v-if="step > 1" flat color="blue" @click="$refs.stepper.previous()" label="Voltar" class="q-ml-sm" />
          
        </q-stepper-navigation>
      </template>
      <template v-slot:message>
        <q-banner v-if="step === 1" >
          <q-card-section>
            
          <div class="full-width row inline no-wrap justify-start items-start content-start q-mt-md">
                     
            <div class="column" style="max-width: 75% ">
              <div class="text-h6">Informações Técnicas </div> 
                <q-item  @blur="onBlur" outlined v-if="showCalibre" v-for="item in calibreResults" @click="selectCalibre(item,'O')" clickable stack-label style="max-width: 400px">   
                  <q-item-section>
                    <q-item-label>{{ `${item.label}` }}</q-item-label>
                  </q-item-section>
                </q-item>      
                <div v-if="data.tipo_reparo !== 9" class="row items-center q-gutter-xs"><br/>
                  <q-input v-model="data.calibre" use-input use-chips hide-dropdown-icon @filter="fetchCalibre('O')" input-debounce="100" label="Calibre" persistent outlined :rules="[val => !!val || 'Campo obrigatório']" />
                    <br/> 
                  <q-btn color="green" @click="fetchCalibre(data.calibre,'O')" label="Pesquisar" />
                </div>
                <q-item  @blur="onBlur" outlined v-if="showCalibreMarca" v-for="item in calibreResults" @click="selectCalibre(item,'M')" clickable stack-label style="max-width: 400px">   
                  <q-item-section>
                    <q-item-label>{{ `${item.label}` }}</q-item-label>
                  </q-item-section>
                </q-item>
                <div class="row items-center q-gutter-xs" v-if="data.tipo_reparo !== 9"><br/>
                    <q-input v-model="data.calibre_marca" use-input use-chips hide-dropdown-icon @filter="fetchCalibre" input-debounce="100" label="Calibre Marca" persistent outlined :rules="[val => !!val || 'Campo obrigatório']" />
                    <br/> 
                    <q-btn color="green" @click="fetchCalibre(data.calibre_marca)" label="Pesquisar" />
                    </div>      
                <div v-if="data.tipo_reparo !== 9" style="max-width: 300px;">
                  <q-select label="Orcamentista" outlined input-debounce="0" emit-value :options="UsersFiltered" v-model="data.orcamentista" use-chips stack-label use-input color="grey-7" class="q-my-lg" @filter="filterUsers"/>
                  <q-input  v-if="data.tipo_movimento === 2" label = "Amplitude" outlined stack-label lazy-rules="ondemand" v-model="data.amplitude"  class="q-my-lg" color="grey-7"/>
                  <q-input  v-if="data.tipo_movimento === 2" label = "Variação S/D" outlined stack-label lazy-rules="ondemand"  v-model="data.variacao_sd"  class="q-my-lg" color="grey-7"/>
                  <q-input v-if="data.tipo_movimento === 1" label = "Un.Min. (V)" outlined stack-label lazy-rules="ondemand"  v-model="data.un_min"  class="q-my-lg" color="grey-7"/>
                  <q-input v-if="data.tipo_movimento === 1" label = "Variação s/m" outlined stack-label lazy-rules="ondemand"  v-model="data.variacao_sm" class="q-my-lg" color="grey-7"/>
                  <q-input v-if="data.tipo_movimento === 1" label = "Consumo µA" outlined stack-label lazy-rules="ondemand" v-model="data.consumo_ua" class="q-my-lg" color="grey-7"/>
                  <q-input label = "Diagnóstico Técnico" outlined stack-label lazy-rules="ondemand" type="textarea" v-model="data.diagnostico_tecnico" color="grey-7" />
                  <q-select label="Intervenção" outlined input-debounce="0" emit-value map-options option-label="label" option-value="id" :options="TipoIntervencao" v-model="data.intervencao" use-chips stack-label use-input color="grey-7" class="q-my-lg"/>
                  <q-select v-if="data.marca && data.marca === 'BREITLING'" outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" :options="TiposGrupo.reparo_bre" v-model="data.repair_bre" label="Repair Type (BRE)" emit-value  map-options option-label="label" option-value="id" class="q-mt-md" style ="min-width: 200px"/>
                    <q-select v-if="data.marca && data.marca === 'BVLGARI'" outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"   :options="TiposGrupo.v02_bv" v-model="data.codigo_v02_bv_1"  emit-value  map-options option-label="label" option-value="id" label="V02 - Código de Sintomas - Clientes" class="q-mt-md" style ="min-width: 200px"/>
          <q-select v-if="data.marca && data.marca === 'BVLGARI'" outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"   :options="TiposGrupo.v01_bv" v-model="data.codigo_v01_bv_1" label="V01 - Código de Sintomas - Técnicos" emit-value  map-options option-label="label" option-value="id" class="q-mt-md" style ="min-width: 200px"/>
            <q-select v-if="data.marca && data.marca === 'BVLGARI'" outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"   :options="TiposGrupo.v02_bv" v-model="data.codigo_v02_bv_2"  emit-value  map-options option-label="label" option-value="id" label="V02 - Código de Sintomas - Clientes(2)" class="q-mt-md" style ="min-width: 200px"/>
          <q-select v-if="data.marca && data.marca === 'BVLGARI'" outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"   :options="TiposGrupo.v01_bv" v-model="data.codigo_v01_bv_2" label="V01 - Código de Sintomas - Técnicos(2)" emit-value  map-options option-label="label" option-value="id" class="q-mt-md" style ="min-width: 200px"/>
                  <q-input v-if="data.marca && data.marca === 'BVLGARI'" outlined stack-label  :rules="[val => !!val || 'Campo obrigatório']"  v-model="data.codigo_sap_bv"  emit-value  map-options option-label="label" option-value="id" label="Código SAP" class="q-mt-md" style ="min-width: 200px"/>
                 
                </div>
              <q-select v-if="data.marca && data.marca === 'TAG HEUER'" outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"    :options="TiposGrupo.reparo_tag" v-model="data.repair_tag" label="Repair Type (TAG)" emit-value  map-options option-label="label" option-value="id" class="q-mt-md" style ="min-width: 200px"/>
              </div>
             
            <div class="column" style="flex: 1;" v-if="data.tipo_reparo !== 9">
              <div class="text-h6" style="align-self:center">Defeitos </div> 
                  <div  class="full-width row inline no-wrap justify-evenly items-start q-mt-mdcontent-center">
                    <q-option-group label="Tabela de Defeitos" outlined stack-label lazy-rules="ondemand"   :options="tabelaDefeitosModificada1"  type ="checkbox" v-model="defeito" />
                  </div>
              </div>
                
                  <q-option-group v-if="data.tipo_reparo !== 9" class="column q-mt-md" label="Tabela de Defeitos" outlined stack-label lazy-rules="ondemand"   :options="tabelaDefeitosModificada2"  type ="checkbox" v-model="defeito"/>
                  <q-card  v-if="step != 3" style="max-width:20%" class ="q-mt-md">
      <q-card-section>
              <div class="text-h6">{{data.id}} <br/><br/>  </div> 
              <q-card-section>
                    <q-input label="Defeito" outlined stack-label  type="textarea" v-model="data.defeito" color="grey-7" readonly/>
                    <q-input label="Nome"  v-model="data.nome" readonly/>
                    <q-input label="Série" :readonly="data.serieconfirmada" v-model="data.serie" ><q-btn v-if="!data.serieconfirmada" color="green" @click="confirma('serie')" icon="done" class="q-mt-md" style="height:5px;width:5px"/></q-input>
                    <q-input label="Referência" :readonly="data.refconfirmada" v-model="data.referencia_produto" ><q-btn v-if="!data.refconfirmada" color="green" @click="confirma('referencia')" class="q-mt-md" style="height:5px;width:5px" icon="done" /></q-input>
                    <q-input label="Marca"  v-model="data.marca" readonly/>
                    <q-input label="Modelo"  v-model="data.modelo" />            
                    <q-select label="Tipo de Movimento"  v-if="data.tipo_reparo !== 9" map-options  :options="TiposMovimento" emit-value outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" v-model="data.tipo_movimento" />
                    <q-select label="Complicação" v-if="data.tipo_reparo !== 9" map-options  :options="TiposComplicação" emit-value outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" v-model="data.complicacao"  />         
                    <q-select label="Tipo de Reparo" v-model="data.tipo_reparo" :options="TiposdeReparo" stack-label text-white option-label="label" option-value="id" emit-value map-options filter/>
               </q-card-section>        
       </q-card-section>
      </q-card>   
                </div>
          </q-card-section>
          
        </q-banner>
      <q-banner v-if="step === 2" style="height:100%">
        <div v-if="data.tipo_reparo !== 9" class="fit row wrap  items-start content-start">
          <q-card v-if="data.tipo_reparo !== 9" flat bordered class='column' style="width:40%">
              <q-select outlined stack-label lazy-rules="ondemand" multiple  :options="TiposDetalhe"  v-model="Detalhes.estado_vidro"  class="q-mt-md" />
              <q-select outlined stack-label lazy-rules="ondemand"   :options="TiposDetalhe"  type ="checkbox" v-model="Detalhes.estado_mostrador" class="q-mt-md" />
              <q-select outlined stack-label lazy-rules="ondemand"   type ="checkbox"  :options="TiposDetalhe" v-model="Detalhes.estado_ponsuares" class="q-mt-md" />
              <q-select outlined stack-label lazy-rules="ondemand"  multiple  type ="checkbox" :options="TiposDetalhe" v-model="Detalhes.estado_coroa"  class="q-mt-md" />
              <q-select outlined stack-label lazy-rules="ondemand"    type ="checkbox" :options="TiposDetalhe" v-model="Detalhes.estado_valvula" class="q-mt-md" />
              <q-select outlined stack-label lazy-rules="ondemand"    type ="checkbox" :options="TiposDetalhe" v-model="Detalhes.estado_luneta"  class="q-mt-md" />
        </q-card>
        <q-space/>
        <q-card v-if="data.tipo_reparo !== 9" flat bordered class='column' style="width:40%">
              <q-select outlined stack-label lazy-rules="ondemand" multiple  :options="TiposDetalhe"  v-model="Detalhes.estado_vidro"  class="q-mt-md" />
              <q-select outlined stack-label lazy-rules="ondemand"   :options="TiposDetalhe"  type ="checkbox" v-model="Detalhes.estado_mostrador" class="q-mt-md" />
              <q-select outlined stack-label lazy-rules="ondemand"   type ="checkbox"  :options="TiposDetalhe" v-model="Detalhes.estado_ponsuares" class="q-mt-md" />
              <q-select outlined stack-label lazy-rules="ondemand"  multiple  type ="checkbox" :options="TiposDetalhe" v-model="Detalhes.estado_coroa"  class="q-mt-md" />
              <q-select outlined stack-label lazy-rules="ondemand"    type ="checkbox" :options="TiposDetalhe" v-model="Detalhes.estado_valvula" class="q-mt-md" />
              <q-select outlined stack-label lazy-rules="ondemand"    type ="checkbox" :options="TiposDetalhe" v-model="Detalhes.estado_luneta"  class="q-mt-md" />
        </q-card>  
        </div>  
        </q-banner>
        
        <q-banner v-if="step === 3" >
          <div class = "justify-around row q-mt-md">        
              <q-card v-if="step === 3" style="max-width:80%">
                <div class="full-width row inline no-wrap justify-evenly items-end content-end  q-mt-md">
                  <q-input label="Série" v-model="data.serie" readonly></q-input>
                  <q-input label="Referência" v-model="data.referencia_produto" readonly/>
                  <q-select style="text-overflow: ellipsis !important;white-space: nowrap !important; overflow: hidden !important;width: 150px!important;align-self: center;" v-if="data.tipo_reparo !== 9" map-options  :options="TiposMovimento" emit-value  stack-label readonly v-model="data.tipo_movimento" />
                  <q-select  v-if="data.tipo_reparo !== 9" map-options style="text-overflow: ellipsis !important;white-space: nowrap !important; overflow: hidden !important;width: 200px!important;align-self: center;" readonly :options="TiposComplicação" emit-value  stack-label v-model="data.complicacao"  />   
                  <q-btn label="Intranet" color="grey-8" @click="navigateToUrl" :loading="loading"/>
                  <q-input label="OS" v-model="data.id" readonly/>
                  <q-input label="Cliente" v-model="data.nome" readonly/>      
                </div> 
                <div class = "q-mt-md" > 
                  <q-separator/> 
                </div>
                <div class="full-width row inline no-wrap justify-evenly items-end content-end  q-mt-md">
                  <q-input label="Desconto" v-if="porcDesconto" :value="formatToTwoDecimals(data.desconto)" type="number" class="q-mt-sm" outlined v-model="data.desconto"   >
      <template v-slot:append>    <q-toggle
        v-model="porcDesconto"
        checked-icon="percent"
        color="green"
        unchecked-icon="attach_money"
      /></template></q-input>
     <q-input label="Desconto" v-if="!porcDesconto" type="number" class="q-mt-sm" outlined v-model="data.valor_desconto_todos"   >
      <template v-slot:append> <q-toggle
        v-model="porcDesconto"
        checked-icon="percent"
        color="green"
        unchecked-icon="attach_money"
      /></template>
    </q-input>

                  <q-input outlined style="width: 250px;" class="q-mt-md column" v-if="[2,5,7].includes(data.tipo_reparo) && data.brand_id && ['CA','BA','MB','OP','PI','JC','VC','PA'].includes(data.brand_id)" v-model="data.contrato_richemont" label ="Valor contrato Richemont" bordered>
                    <template v-slot:append><span style="font-size: 12px;">R$</span></template>
                  </q-input>
                  <q-input outlined label="Prazo" type="number" style="width: 100px;" class="q-mt-md column" v-model.number="data.prazo">
                    <template v-slot:append><span style="font-size: 12px;">dias</span></template>
                  </q-input>
                  <q-input outlined label="Prazo" style="width: 200px;" class="q-mt-md column" v-model="data.prazo_cx">
                    <template v-slot:append><span style="font-size: 12px;">C.Aux</span></template>
                  </q-input>
                  <q-input outlined label="Prazo 2" style="width: 200px;" class="q-mt-md column" v-model="data.prazo2">
                    <template v-slot:append><span style="font-size: 12px;">C.Aux</span></template>
                  </q-input>

                  <q-input outlined label="Garantia" style="width: 400px;" class="q-mt-md column" v-model="data.garantia">
                    <template v-slot:append><span style="font-size: 12px;">Cx.Aux</span></template>
                  </q-input>
                </div>
                <div class = "q-mt-md" > 
                  <q-separator/> 
                </div>
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
      <q-card v-if="step === 3" style="min-width:80%">
      <br/> <q-separator/>
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
            <q-popup-edit v-if="editando"  @save="newValue => updateQtdInTodos(props.row, newValue)" v-model="props.row.quantidade" buttons persistent v-slot="scope">
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
            <q-popup-edit v-if="editando"  @save="newValue => updateQtdInTodos(props.row, newValue)" v-model="props.row.quantidade" buttons persistent v-slot="scope">
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
       </q-card-section>
       <q-separator/>
       <div class="full-width row inline justify-evenly items-center content-center  q-mt-md">
        <q-input label="Total Bruto" class="q-mt-md" style="align-self: center; width:300px" outlined v-model="data.total_bruto" readonly >
        <template v-slot:append><span style="font-size: 12px;">R$</span></template></q-input>
       <q-input label="Total Obrigatório" class="q-mt-md" outlined v-model="data.total_obrigatorio" readonly  >
        <template v-slot:append><span style="font-size: 12px;">R$</span></template></q-input>
       <q-input label="Total Obrigatórios + Opcional" class="q-mt-md" style="align-self: center; width:300px" outlined v-model="data.valor_cliente" readonly >
        <template v-slot:append><span style="font-size: 12px;">R$</span></template></q-input>
       <q-input label="Desconto Obrigatórios" class="q-mt-md" style="align-self: center; width:300px" outlined v-model="data.valor_desconto_obrigatorios" readonly >
        <template v-slot:append><span style="font-size: 12px;">R$</span></template></q-input>
        <q-input label="Desconto Obrigatórios + Opcional" class="q-mt-md" style="align-self: center; width:300px" outlined v-model="data.valor_desconto_todos" readonly >
        <template v-slot:append><span style="font-size: 12px;">R$</span></template></q-input>
       <q-input v-if = "currentUser.administrator" label="Custo Total" class="q-mt-md" style="align-self: center; width:300px" outlined v-model="data.custo_total" readonly >
        <template v-slot:append><span style="font-size: 12px;">R$</span></template></q-input>
       <q-input v-if = "currentUser.administrator" label="Margem Obrigatórios + Opcional" class="q-mt-md" style="align-self: center; width:300px" outlined v-model="data.valor_margem" type ="number" readonly >
        <template v-slot:append><span style="font-size: 12px;">%</span></template>
        </q-input>
        <q-input v-if = "currentUser.administrator" label="Margem Obrigatórios" class="q-mt-md" style="align-self: center; width:300px" outlined v-model="data.valor_margem_obrigatorios" type ="number" readonly >
        <template v-slot:append><span style="font-size: 12px;">%</span></template>
        </q-input>
        <q-input v-if = "currentUser.administrator" label="Valor Líquido WT" class="q-mt-md" style="align-self: center; width:300px" outlined v-model="data.valor_liquido" type ="number" readonly >
        <template v-slot:append><span style="font-size: 12px;">R$</span></template>
        </q-input>
        <q-input v-if = "currentUser.administrator" label="Valor Líquido Obrigatórios" class="q-mt-md" style="align-self: center; width:300px" outlined v-model="data.valor_liquido_obrigatorios" type ="number" readonly >
        <template v-slot:append><span style="font-size: 12px;">R$</span></template>
        </q-input>
        
      </div>
      <div class="q-mt-md"> </div>
      </q-card>
    </q-card>
    <q-card v-if="step === 3" style="width:19%"  class="column q-pa-none items-start content-start">
      <div class="full-width row q-mt-md justify-evenly ">
        <q-card-section> 
          Histórico de Orçados
         </q-card-section>
         <q-btn color="green" @click="openCancelInvoiceDialog()" icon="list"/>
      </div>
      <div class="q-pa-md items-start content-start justify-start">
  </div>
      <q-card-section> 
       </q-card-section>
       <q-table
                      style="height: 802px; max-width:100%"
                      flat bordered
                      ref="tableRef"
                      :rows="orcamentoResults"
                      :columns="columnsorc"
                      :table-colspan="2"
                      row-key="referencia"
                      virtual-scroll
                      :virtual-scroll-item-size="48"
                      :pagination="pagination"
                      :rows-per-page-options="[0]"
                      :filter="filterOrcados"
                    >
                    <template v-slot:top-left>
                        <q-input background="blue" dense debounce="300" v-model="filterOrcados" placeholder="Pesquisa">
                          <template v-slot:append>
                            <q-icon name="search" />
                          </template>
                        </q-input>
                      </template>

                      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td>

            {{ props.row.referencia }} <br/>
            <q-btn color="grey-9" :loading="loading" @click="inserirOrcamento('OP',props.row.referencia)" label="OP" class="q-mt-md" style="height:5px;width:5px"/>
            <q-btn color="grey-8" :loading="loading" label="I" class="q-mt-md" @click="inserirOrcamento('I',props.row.referencia)" style="height:5px;width:5px"/>
            <q-btn color="grey-7" :loading="loading" @click="inserirOrcamento('OB',props.row.referencia)" label="OB" class="q-mt-md" style="height:5px;width:5px"/>
          </q-td>
          <q-td>
            {{ props.row.nome }}

          </q-td>
        </q-tr>
      </template>
                    </q-table>
       <q-separator/>
       <q-card-section> 
          Histórico de OS
         </q-card-section>
       <q-item  outlined v-for="item in seriesearchResults" clickable stack-label>
              <q-item-section>
                <q-item-label>{{ `Série: ${item.serie} - ${item.nome}` }}</q-item-label>
                <q-item-label caption>{{ `${item.id} - ${item.data_os} - ${item.data_entrega_produto}` }}</q-item-label>
                <q-item-label caption>{{ `${item.tipo_reparo} - ${item.status_os}` }}</q-item-label>
              </q-item-section>
            </q-item>    
      </q-card>
  </div>
      </q-banner>
    
        </template>
    </q-stepper>   
    <error-dialog v-if="errorDialogVisible" :errors="receivedErrors" v-model="errorDialogVisible"></error-dialog>
    {{ data }}
  </modal-form>


  <modal-dialog
    title="Cancelar"
    mode
    v-model="cancelInvoiceDialog"
    :message="`Como os itens devem ser inseridos ?`"
    @confirm="inserirTodos()"
    :copiar_todos = true
    :itens = orcamentoResultsModal
  />
</template>

<script setup>
import { computed, ref,} from "@vue/reactivity";
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

const columnsorc = [ { name: 'Referência', align: 'left', label: 'Referência', field: 'referencia', sortable: true },
{ name: 'Descriçao', align: 'left', label: 'Descrição', field: 'nome', sortable: true }
]
const defeito = ref([]) 
const  filter = ref('')
const  filterOrcados = ref('')
const cancelInvoiceDialog = ref(false);
const serieConfirmada = ref(false)
const refConfirmada = ref(false)
const selectedBrand = ref('')
const errorDialogVisible = ref(false)
const receivedErrors = ref({})
const stepper = ref()
const step = ref(1)
const brands = ref(['PR','SP','RJ']);
const brandsFiltered = ref([]);
const $q = useQuasar();
const props = defineProps(["showEstimate", "modelValue"]);
const emit = defineEmits(["update:showEstimate", "update:modelValue", "confirm","modalClosed","os"]);
const Detalhes = ref({})
const data = ref({

    });
const porcDesconto = ref(true)
const refsearchResults = ref([]);
const orcamentoResults = ref([]);
const orcamentoResultsModal = ref(orcamentoResults)
const seriesearchResults = ref([]);
const serieshowResults = ref(true);
const refshowResults = ref(true);
const toggles = ref({
  sedex: false,
  // outros toggles aqui...
});
const TipoIntervencao = ref([])
const showCalibre = ref(false);
const showCalibreMarca = ref(false);
const calibreResults = ref([]);
const TiposGrupo = ref([]);
const cameraModalOpen = ref(false);
const photoType = ref('');
const currentUser = computed(() => AuthService.user);
const Obrigatorios = ref([]);
const Todos = ref([]);
const Opcionais = ref([]);
const Servicos = ref([]);
const ServicosFiltered = ref([]);
const codigo_item = ref(1);
const estoklusUsers = ref([]);
const UsersFiltered = ref([]);
const editando = ref(false) 
let editedLabel = ref('');
const TiposdeReparo = ref([
    { id: 1, label: 'Fora de Garantia' },
    { id: 2, label: 'Garantia de Venda' },
    { id: 3, label: 'Garantia de Serviço' },
    { id: 4, label: 'Análise Garantia' },
    { id: 5, label: 'Estoque' },
    { id: 6, label: 'Cortesia' },
    { id: 7, label: 'Garantia Internacional' },
    { id: 8, label: 'Garantia de 3s' },
    { id: 9, label: 'Acessórios' }
]);

const tabelaDefeitos2 = ref([{value: "11",label: "Vedação preventiva recomendada." },
{value: "12",label: "Peças danificadas."},
{value: "13",label: "Peças não originais/adaptadas."},
{value: "14",label: "Relógio acidentado."},
{value: "15",label: "Relógio sofreu impacto."},
{value: "16",label: "Defeito no módulo de programa / sensor."},
{value: "17",label: "Defeito no vidro táctil."},
{value: "18",label: "Bateria esgotada."},
{value: "19",label: "Polimento"},
{value: "1",label: "Necessidade de limpeza e lubrificação."},
{value: "2",label: "Desgaste ou defeito em peça(s)."},
{value: "3",label: "Unidade (voltagem) mínima alta."},
{value: "4",label: "Consumo alto."},
{value: "5",label: "Circuito eletrônico com defeito."},
{value: "6",label: "Funcionamento irregular."},
{value: "7",label: "Entrada de umidade -  provocou oxidação."},
{value: "8",label: "Vazamento de bateria -  provocou corrosão."},
{value: "9",label: "Revisão preventiva recomendada"},
{value: "10",label:"Vedação comprometida."},])

const tabelaDefeitos = ref([
{value: "11",label: "Vedação preventiva recomendada."},
{value: "12",label: "Peças danificadas."},
{value: "13",label: "Peças não originais/adaptadas."},
{value: "14",label: "Relógio acidentado."},
{value: "15",label: "Relógio sofreu impacto."},
{value: "16",label: "Defeito no módulo de programa / sensor."},
{value: "17",label: "Defeito no vidro táctil."},
{value: "18",label: "Bateria esgotada."},
{value: "19",label: "Polimento"},

]);
const tabelaDefeitos1 = ref([
{value: "1",label: "Necessidade de limpeza e lubrificação."},
{value: "2",label: "Desgaste ou defeito em peça(s)."},
{value: "3",label: "Unidade (voltagem) mínima alta."},
{value: "4",label: "Consumo alto."},
{value: "5",label: "Circuito eletrônico com defeito."},
{value: "6",label: "Funcionamento irregular."},
{value: "7",label: "Entrada de umidade -  provocou oxidação."},
{value: "8",label: "Vazamento de bateria -  provocou corrosão."},
{value: "9",label: "Revisão preventiva recomendada"},
{value: "10",label:"Vedação comprometida."},

]);

const tabelaDefeitosModificada1 = computed(() => {
      return tabelaDefeitos1.value.map(defeito => {
        return {
          ...defeito,
          label: `${defeito.value} - ${defeito.label}`
        }
      })
    })

const tabelaDefeitosModificada2 = computed(() => {
      return tabelaDefeitos.value.map(defeito => {
        return {
          ...defeito,
          label: `${defeito.value} - ${defeito.label}`
        }
      })
    })
const TiposMovimento = ref([
{ value: 1, label: 'Quartz' },
{ value: 2, label: 'Automático' },
{ value: 3, label: 'Corda Manual' }
]);

const TiposComplicação = ref([
{ value: 1, label: 'Três Ponteiros' },
{ value: 2, label: 'Cronógrafo' },
]);

const togglesValue = computed(() => toggles.value);
watch(() => props.showEstimate, (newValue) => {
  if (newValue) {
    Detalhes.value={
      estado_caixa: [],
      estado_coroa: [],
      estado_fundo: [],
    defeito: [""]}



      if(data.value.tipo_reparo == 4){
        delete data.value.tipo_reparo
      }

      delete data.value
    data.value = props.modelValue ;
    data.value.desconto = 0
    data.value.custo_total = 0
    data.value.desconto_total = 0
    data.value.total_bruto = 0
    data.value.valor_cliente = 0
    data.value.estoklus_id= currentUser.value.estoklus_id
    data.value.editado = 'N',
    data.value.serieconfirmada = false
    data.value.refconfirmada = false
    step.value = 1
    data.value.peca_generica_valor = 0
    delete Todos.value
    Todos.value = []
    Opcionais.value = []
    Obrigatorios.value = []
    defeito.value =[]
    serieConfirmada.value= false
    refConfirmada.value = false
      let referencia = data.value.referencia_produto
      loadEstoklusUsers();
      carregaGrupo();
      fetchOrcamento(referencia);
      fetchAnalisar()
      fetchServicos();
      loadDadosMarca();
      fetchDataserie(data.value.serie)
  }
});
loadBrands();


const showEstimate = computed({
  get: () => {

    let requested;
    
    if (props.modelValue?.requested) {
      data = toLocalISOString(new Date(props.modelValue?.requested));
    } else {
      requested = toLocalISOString(new Date())
    }

    return props.showEstimate;
  },
  set: (value) => {
    emit("update:showEstimate", value);
  },
  
});

function confirma(type){
  if(type == 'serie'){
    data.value.serieconfirmada = true
  }
  else{
    data.value.refconfirmada = true
  }
}

async function confirm() {
    emit("os",data.value)
    step.value = 1
    data.value = ''
    Todos.value = ''
    Opcionais.value = ''
    Obrigatorios.value = ''
    
    emit("update:showEstimate", false);
    emit("confirm");
    

}

const formatCPF = (cpf) => {
      if (!cpf) return '';
      return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
    };

    const formatCNPJ = (cnpj) => {
      if (!cnpj) return '';
      return cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, "$1.$2.$3/$4-$5");
    };

function formatValue(item){
  return parseFloat(item.replace(',', '.'));
}
const fetchOrcamento = async (val, update) => {
  try {
    if (val && val.length > 2){
      const response = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/orc`, 
        {
          params: {referencia: data.value.referencia_produto},
          headers: {'Content-Type': 'application/json'}
        }
      );

      const options = response.data.map(item => ({
        id: item.id,
        nome: item.label,
        referencia: item.referencia
      }));

      orcamentoResults.value = options;

    }
  } catch (err) {
    console.error("Erro ao buscar dados:", err);
  }
};

const fetchServicos = async (val, update) => {
  try {
      console.log(data.value.marca)
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



const fetchCalibre = async (val,tipo) => {

  try{
  const response = await OrdersServicesService.getServices
    ({_select:"calibre",
      _distinct:true,
      _order_a: "calibre",
      "calibre.lk": val + '%',
    _limit:3,
    _offset:0})
    

    if(tipo === 'O'){
      showCalibre.value = true;
    }else{
      showCalibreMarca.value = true;
    }

    if(response.data.length > 0){
    
    calibreResults.value = response.data?.map((l) => {
      return { label: l.calibre, value: l.calibre };
    });}else{   Notify.create({
              type: 'warning',
              message: `Calibre não encontrado`
            });
      
    }
  }
catch (err) {
    console.error("Erro ao buscar dados:", err);
  } 

};


const selectCalibre = (value,tipo) => {
  if (tipo === 'M'){
    data.value.calibre_marca = value.value;
  }else{
  data.value.calibre = value.value;
  }
  calibreResults.value = false;
};

const fetchGrupos = async (tipo) => {
  try {
    
      
    const response = await OrdersServicesService.getGrupos(tipo)
    
    return response?.map(item => ({
        id: item.id,
        label: item.label
      }))
    }
   catch (err) {
    console.error("Erro ao buscar dados:", err);
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
            console.log(response.data[0])
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

const fetchDataserie = async (val, update) => {
  try {
    
    if (val && val.length > 2){
    //const response = await axios.get(`https://sua-api.com/search?q=${val}`);
   
    const response = await OrdersServicesService.getServices({"serie.lk": val + "%",_limit:3,_offset:0,_order_d: "data_os"} )
    

    if (response.data.length == 0){
      Notify.create({
              type: 'warning',
              message: `Série ${val}, não encontrada no histórico`
            });
    }

    else {
    const options = response.data.map(item => ({
      id: item.id, // Ajuste essas propriedades conforme os dados da sua API
      nome: item.nome,
      data_os: item.data_os,
      data_entrega_produto: item.data_entrega_produto,
      documento: item.documento,
      referencia_produto: item.referencia_produto,
      serie: item.serie,
      modelo: item.modelo,
      tipo_reparo: item.tipo_reparo,
      status_os: item.status_os,
      calibre: item.calibre,
      material_caixa: item.material_caixa,
      marca: item.marca,
      codigo_tipo_pessoa: item.codigo_tipo_pessoa

    }));

      seriesearchResults.value = options;
      serieshowResults.value = true
      return seriesearchResults;
    }
  }
  } catch (err) {
    console.error("Erro ao buscar dados:", err);
  }
};



async function loadBrands() {
    const response = (
    await PurchaseOrdersService.getBrandListOsOrderAvaiable()
  ).data.map((b) => {
    return {
      label: b.brand.toUpperCase(),
      value: b.brand.toUpperCase(),
      brand_id: b.brand_id,
    };
  });
    
    brands.value = response
  };


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

  async function carregaGrupo(grupo){
    TipoIntervencao.value = await fetchGrupos('TR');

    if (data.value.marca == 'TAG HEUER'){
    TiposGrupo.value.reparo_tag = await fetchGrupos('TU');
    }else if(data.value.marca == 'BREITLING'){
      TiposGrupo.value.reparo_bre = await fetchGrupos('B01');
      TiposGrupo.value.reparo_bre = TiposGrupo.value.reparo_bre.map(item => ({
        id: item.id,
        label: item.id + ' - ' + item.label}));
    }else if(data.value.marca == 'BVLGARI'){
      TiposGrupo.value.v01_bv = await fetchGrupos('V01');
      TiposGrupo.value.v02_bv = await fetchGrupos('V02');
    }

  }

  const fetchAnalisar = async (val, update) => {
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

const updateQtdInTodos = (row, newValue) => {
  const item = Todos.value.find(item => item.index === row.index || item.id === row.id);
  if (item) {
    item.quantidade = newValue;
    // Aqui você pode adicionar qualquer lógica adicional necessária,
    // como enviar uma atualização para uma API
  }
};

  watch(() => data.value.desconto, (newDesconto) => {
  if ((data.value.tipo_pessoa === 'F' || data.value.codigo_tipo_pessoa === 'F') && newDesconto > data.value.desconto_pf) {
    data.value.desconto = data.value.desconto_pf;
  }
  callApi();
});
const updateLabel = (row, newValue) => {
  const index = Obrigatorios.findIndex(r => r === row);
  if (index !== -1) {
    Obrigatorios[index].label = newValue;
  }
};
watch(defeito, (newDefeito) => {
      data.value.diagnostico_tecnico = newDefeito
        .map(codigo => {
          const foundDefeito = tabelaDefeitos2.value.find(defeito => defeito.value === codigo);
          return foundDefeito ? ` - ${foundDefeito.label}` : '';
        })
        .join('');
    });

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

watch(
  () => editando.value,
  (newValue, oldValue) => {
    if (newValue == true){
      data.value.editado = 'S'
    }
  }
);

const callApi = debounce(() => {
  if (showEstimate.value == true){
    calculaOrcamento()
  }
 
  // chamar sua API aqui
}, 500); // 300 ms de delay


watch(
            () => selectedBrand.value,
            (newValue) => {
              data.value.marca = newValue.value;
              data.value.brand_id = newValue.brand_id;
            }
        );


watch(
            () => cameraModalOpen.value,
            (newValue) => 
            {
                if (!newValue) {
                  emit('modalClosed');
                }
            }
        );


const onSubmit = async () => {
  const validacao1 = true


      if(step.value === 1 ){
        
        let fields = {}
        if (data.value.tipo_reparo !=9) {

          const fieldsob = {
        'serieconfirmada':"Confirmar Série", 
        'refconfirmada': "Confirmar Referência", 
        'calibre': "Calibre", 
        'diagnostico_tecnico':"Diagnóstico",
        'orcamentista':"Orçamentista",
        'tipo_movimento':'Tipo de Movimento',
        'complicacao': 'Complicação',
        'tipo_reparo': 'Tipo de Reparo',
        'intervencao': 'Intervenção'
        }
        fields = {...fields, ...fieldsob}
        
        }



          if(data.value.brand_id === 'TH'){
            const fieldso = {'repair_tag': "Campo TAG"}
            fields = {...fields, ...fieldso}
          }
          if(data.value.brand_id === 'BE' && data.value.tipo_reparo != 9){
            const fieldso = {'repair_bre': "Campo Breitling"}
            fields = {...fields, ...fieldso}
          }if(data.value.brand_id === 'BV' && data.value.tipo_reparo != 9){
            const fieldso = {'codigo_v01_bv_1': "Campo Bulgari",'codigo_sap_bv': "Campo SAP Bulgari"}
            fields = {...fields, ...fieldso}
          }
        const errors = Object.keys(fields).filter(field => !data.value[field]).map(field => ({ id: fields[field], problem: "" }));
        if (errors.length > 0 && validacao1 === true ) {
          
          receivedErrors.value = errors;
          errorDialogVisible.value = true
        } else {
          stepper.value.next();
        }
      
      } else {
          stepper.value.next();
      }
    }

const inserirOS = async () => {
        if(!data.value.data_analise){
          data.value.data_analise = new Date().toISOString().split('T')[0]; }
        try {
                 const response = await OrdersServicesService.addEstimate(data.value)
                  if(response.success){
            confirm()
      Notify.create({
              type: 'positive',
              message: `Orçamento da OS ${response.success}, inserido no estoklus`
            });
    }

    else{

      Notify.create({
              type: 'negative',
              message: response
            });
    }
                } catch (error) {
                  
                }
          
};

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

const formatNumber = (value) => {
      return parseFloat(value).toFixed(2);
    };


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

function formatToTwoDecimals(value) {
    return parseFloat(value).toFixed(2);
}
async function loadEstoklusUsers() {
  const response = await OrdersServicesService.getUsersEstoklus();


  estoklusUsers.value = response?.map((b) => {
    return { label: b.label.toUpperCase(), value: b.id };
  });

}

async function inserirTodos(){
  for (let item of orcamentoResultsModal.value) {
    if (item.tipo && item.tipo != '-'){  
    inserirOrcamento(item.tipo,item.referencia)
        }
      }
}

async function loadDadosMarca() {
  loading.value = true
  try {
    const response = await axios.get(
      `https://app.watchtime.com.br/api/estoklus/marca/${data.value.brand_id}`
    );

    // Defina desconto baseado no tipo de pessoa ou código específico do cliente
    if (data.value.tipo_pessoa === 'J' || data.value.codigo_tipo_pessoa === 'J') {
      // Se o código estoklus do cliente for PADA BR100206, o desconto deve ser 25
      if (data.value.cliente_id === 'PADA BR100206') {
        data.value.desconto = 25;
        
      } else {
        data.value.desconto = response.data[0].DESCONTO_PJ;
      }
    } else {
      data.value.desconto = 0;
    }

    // Defina garantia como em branco se o tipo de reparo for 9
    if (data.value.tipo_reparo === 9) {
      data.value.garantia = ' ';
    } else {
      data.value.garantia = response.data[0].GARANTIA 
        ? `${response.data[0].GARANTIA} meses mecanismo e vedação` 
        : ' ';
    }

    // Outras atribuições
    data.value.prazo = response.data[0].PRAZO || 1;
    data.value.prazo_cx = response.data[0].PRAZO ? `${response.data[0].PRAZO} dias` : ' ';
    data.value.senha = response.data[0].SENHA || ' ';
    data.value.url = response.data[0].URL || ' ';
    data.value.usuario = response.data[0].USUARIO || ' ';
    if (data.value.cliente_id === 'PADA BR100206') {
        data.value.desconto_pj = 25;
      }
  } catch (error) {
    console.error('Erro ao carregar dados da marca:', error);
  } finally {
    loading.value = false;
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
const remove = async (val,itemToRemove) => {

try {
    if(val === 'OP'){
      Opcionais.value = Opcionais.value.filter((item) => item.index !== itemToRemove.index);
    }else{
      Obrigatorios.value = Obrigatorios.value.filter((item) => item.index !== itemToRemove.index);
    }

    Todos.value = Todos.value.filter((item) => item.index !== itemToRemove.index);
} catch (err) {
  console.error("Erro ao buscar dados:", err);
}
};


function openCancelInvoiceDialog(props) {
  cancelInvoiceDialog.value = true;
}

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
      data.value.valor_desconto_todos = response.data.valor_desconto_todos;
      data.value.total_obrigatorio = response.data.total_obrigatorio
      data.value.valor_liquido_obrigatorios = response.data.valor_liquido_obrigatorios
      data.value.valor_margem_obrigatorios = response.data.valor_margem_obrigatorios
    }
  } catch(error) {
    console.error("Houve um erro ao calcular o orçamento:", error);
  }
}


async function navigateToUrl() {
  window.open(data.value.url, '_blank');
}

function getBackgroundColor(row){
  let classe
  console.log(row)
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
