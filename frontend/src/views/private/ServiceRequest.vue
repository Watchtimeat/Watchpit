<template>
  <modal-form title="Nova OS" v-model:show="showRequest" @submit="onSubmit">
    
    <q-stepper
      v-model="step"
      ref="stepper"
      color="blue"
      animated
      spaced
      class="q-ml-sm"
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
        :name="2"
        title="Dados do Cliente"
        icon="contacts"
        :done="step > 2"
        ></q-step>
        <q-step
        :name="3"
        title="Informações da OS"
        icon="home_repair_service"
        :done="step > 3"
        ></q-step>
        <template v-slot:navigation>
        <q-stepper-navigation>                  
          <q-btn v-if="step < 3" @click="onSubmit(this)" type="submit" color="blue" :label="step === 3 ? 'Finish' : 'Avançar'" />
          <q-btn v-if="step === 3" color="red" @click="inserirOS()" label="Gravar OS" class="q-ml-sm" :loading="loading"/>
          <q-btn v-if="step > 1" flat color="blue" @click="$refs.stepper.previous()" label="Voltar" class="q-ml-sm" />
          <q-btn v-if="step === 2 && data.cliente_id" @click="atualizarCliente()" class="q-ml-sm" :disable=data.cliente_atualizado :disabled="!data.tipo_pessoa" type="submit" color="primary" label = 'Atualizar Dados' :loading="loading">   
            <q-tooltip v-if="!data.tipo_pessoa">
               Tipo de pessoa não selecionado
             </q-tooltip>
          </q-btn>
          <q-btn v-if="step === 2 && !data.cliente_id" @click="inserirCliente()" class="q-ml-sm" type="submit" color="red" :disabled="!data.tipo_pessoa" label = 'Inserir no Estoklus' :loading="loading" >
          <q-tooltip v-if="!data.tipo_pessoa">
               Tipo de pessoa não selecionado
             </q-tooltip>
             </q-btn>
          
        </q-stepper-navigation>
      </template>
      <template v-slot:message>
        <q-banner v-if="step === 3" class="q-px-lg">
          <div class="q-gutter-md row items-start">
          <q-card flat bordered style="max-width: 500px">

          <q-badge align="top">Detalhes OS </q-badge>
          
          <q-input 
          outlined 
          stack-label 
          label="Última OS"  
          lazy-rules="ondemand" 
          :rules="[(value) => !!value || 'A data da solicitação é obrigatória']"
           filled
          v-model="data.ultima_os" 
          color="grey-7" 
          v-if="data.tipo_reparo !== 9"
          disable 
          readonly />
         
          <q-input
            outlined
            stack-label
            label="Defeito"
            type="textarea"
            v-model="data.defeito"
            color="grey-7"
            :rules="[val => !!val || 'Campo obrigatório']" 
          />
          <q-input
            outlined
            stack-label
            label="Acessórios"
            lazy-rules="ondemand"
            type="text"
            v-model="data.acessorios"
            color="grey-7"
            :rules="[(value) => !!value || 'A data da solicitação é obrigatória']"
          />
          <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="data.observacao"
            color="grey-7"
          />
          </q-card>

          <q-card flat bordered style="max-width: 400px">
          <q-badge align="top">Outros dados</q-badge><br/>
          <q-toggle v-model="toggles.sedex" 
            label="Sedex" 
            color="grey-7"
            outlined
            style="min-width: 200px"
            v-if="data.tipo_reparo !== 9"
            type="text"
          />

          <q-input
            v-if="toggles.sedex"
            outlined
            stack-label
            label="Código Rastreio"
            lazy-rules="ondemand"
            type="text"
            v-model="data.codigo_rastreio"
            color="grey-7"
            :rules="[(value) => !!value || 'A data da solicitação é obrigatória']"
          />

          <q-input outlined stack-label lazy-rules="ondemand"  v-model="data.os_loja" label="OS da Loja" class="q-mt-md" />
          <q-input outlined stack-label lazy-rules="ondemand"  v-model="data.os_loja" label="OS da Loja (Anterior)" class="q-mt-md" disable readonly />  
          <div class="q-mt-md">
          <q-toggle v-model="toggles.envia_whatsapp" 
            label="OS por Whatsapp" 
            color="grey-7"
            outlined
            style="max-width: 200px"
            type="text"
            icon="phone"
          />
          <q-toggle v-model="toggles.envia_email" 
            label="OS por E-mail" 
            color="grey-7"
            outlined
            icon="mail"
            style="max-width: 200px"
            type="text"
          />  
        </div>
          
          <q-item  class="q-mt-md" tag="label" v-ripple>
            <q-item-section>
              <q-item-label>NF de entrada</q-item-label>
              <q-item-label color="red" v-if="!toggles.nf_entrada" caption>Será emitida uma NF de entrada</q-item-label>
              <q-item-label v-if="toggles.nf_entrada" caption>Se não tiver nota, desabilitar</q-item-label>
            </q-item-section>
            <q-item-section avatar>
              <q-toggle color="green" v-model="toggles.nf_entrada" />
            </q-item-section>
          </q-item>  
          <q-input outlined stack-label lazy-rules="ondemand" v-if="toggles.nf_entrada" v-model="data.nf_entrada" label="Número NF" class="q-mt-md" />
          <q-input outlined stack-label lazy-rules="ondemand"  v-if="toggles.nf_entrada" v-model="data.valor_produto_nf" label="Valor do Produto (NF)" class="q-mt-md" />
          <q-input outlined stack-label lazy-rules="ondemand"  v-if="toggles.nf_entrada" v-model="data.codigo_produto_nf" label="Código do Produto (NF)" class="q-mt-md" />
          <q-input outlined stack-label lazy-rules="ondemand"  v-if="toggles.nf_entrada" v-model="data.data_nf" label="Data da NF" type=date class="q-mt-md" />
          <q-input outlined stack-label lazy-rules="ondemand"  v-if="[2, 7].includes(data.tipo_reparo)" v-model="data.data_venda" label="Data de venda" type=date class="q-mt-md" />
          <q-input outlined stack-label lazy-rules="ondemand"  v-if="[2, 7].includes(data.tipo_reparo)" v-model="data.codigo_garantia" label="Código da Garantia" class="q-mt-md" />
          <q-space/>

        </q-card>
        <q-card v-if="data.tipo_reparo !== 9" flat bordered style="max-width: 400px">
          <q-badge align="top">Condições do Relógio</q-badge>
          <q-list bordered>
            <q-expansion-item group="somegroup" icon="watch" label="Caixa">
              <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="Detalhes.descricao_caixa"
            color="grey-7"
            />
              <q-option-group outlined stack-label lazy-rules="ondemand"   :options="TiposDetalhe"  type ="checkbox" v-model="Detalhes.estado_caixa" class="q-mt-md"/>
            </q-expansion-item>
            <q-expansion-item group="somegroup" icon="watch" label="Vidro">
              <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="Detalhes.descricao_vidro"
            color="grey-7"
          />
              <q-option-group outlined stack-label lazy-rules="ondemand"   :options="TiposDetalhe"  type ="checkbox" v-model="Detalhes.estado_vidro"  class="q-mt-md" />

            </q-expansion-item>
            <q-expansion-item group="somegroup" icon="watch"  label="Mostrador"  style="max-width: 400px">
              <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="Detalhes.descricao_mostrador"
            color="grey-7"
          />
              <q-option-group outlined stack-label lazy-rules="ondemand"   :options="TiposDetalhe"  type ="checkbox" v-model="Detalhes.estado_mostrador" class="q-mt-md" />
            </q-expansion-item>
            <q-expansion-item v-if="data.complicacao && data.complicacao === 2" group="somegroup" icon="watch" label="Ponsuares"   >
              <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="Detalhes.descricao_ponsuares"
            color="grey-7"
          />
              <q-option-group outlined stack-label lazy-rules="ondemand"   type ="checkbox"  :options="TiposDetalhe" v-model="Detalhes.estado_ponsuares" class="q-mt-md" />
            </q-expansion-item>
            <q-expansion-item group="somegroup" icon="watch" label="Coroa"  >
              <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="Detalhes.descricao_coroa"
            color="grey-7"
          />
              <q-option-group outlined stack-label lazy-rules="ondemand"    type ="checkbox" :options="TiposDetalhe" v-model="Detalhes.estado_coroa"  class="q-mt-md" />

            </q-expansion-item>
            <q-expansion-item group="somegroup" icon="watch" label="Válvula" >
              <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="Detalhes.descricao_valvula"
            color="grey-7"
          />
              <q-option-group outlined stack-label lazy-rules="ondemand"    type ="checkbox" :options="TiposDetalhe" v-model="Detalhes.estado_valvula" class="q-mt-md" />

            </q-expansion-item>
            <q-expansion-item group="somegroup" icon="donut_large" label="Luneta"  >
              <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="Detalhes.descricao_luneta"
            color="grey-7"
          />
              <q-option-group outlined stack-label lazy-rules="ondemand"    type ="checkbox" :options="TiposDetalhe" v-model="Detalhes.estado_luneta"  class="q-mt-md" />
            </q-expansion-item>
            <q-expansion-item group="somegroup" icon="watch" label="Indexes"   >
              <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="Detalhes.descricao_indexes"
            color="grey-7"
          />
              <q-option-group outlined stack-label lazy-rules="ondemand" :options="TiposDetalhe"   type ="checkbox" v-model="Detalhes.estado_indexes" class="q-mt-md" />
            </q-expansion-item>
            </q-list> 
        </q-card>
        
       
          <q-card v-if="data.tipo_reparo !== 9" flat bordered style="max-width: 400px">
            <q-badge align="top">Condições do Relógio </q-badge>

            <q-expansion-item group="somegroup" icon="watch" label="Ponteiros"  >
              <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="Detalhes.descricao_ponteiros"
            color="grey-7"
          />
              <q-option-group outlined stack-label lazy-rules="ondemand" :options="TiposDetalhe"   type ="checkbox" v-model="Detalhes.estado_ponteiros"  class="q-mt-md" />
            </q-expansion-item>
            <q-expansion-item group="somegroup" icon="watch" label="Pulseira"   >
              <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="Detalhes.descricao_pulseira"
            color="grey-7"
          />
              <q-option-group outlined stack-label lazy-rules="ondemand" :options="TiposDetalhe"   type ="checkbox" v-model="Detalhes.estado_pulseira" class="q-mt-md" />
            </q-expansion-item>
            <q-expansion-item group="somegroup" icon="watch" label="Tampa do fundo"  >
              <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="Detalhes.descricao_tampa_fundo"
            color="grey-7"
          />
              <q-option-group outlined stack-label lazy-rules="ondemand" :options="TiposDetalhe"   type ="checkbox" v-model="Detalhes.estado_tampa_fundo"  class="q-mt-md" />
            </q-expansion-item>
            <q-expansion-item group="somegroup" icon="watch" label="Fecho"  >
              <q-input
            outlined
            stack-label
            label="Observações"
            lazy-rules="ondemand"
            type="textarea"
            v-model="Detalhes.descricao_fecho"
            color="grey-7"
          />
              <q-option-group outlined stack-label lazy-rules="ondemand" :options="TiposDetalhe"   type ="checkbox" v-model="Detalhes.estado_fecho"  class="q-mt-md" />
            </q-expansion-item>
            <q-input outlined stack-label lazy-rules="ondemand" default="0" v-model="Detalhes.quantidade_elos" label="Quantidade de elos" class="q-mt-md" />
            <q-input outlined stack-label lazy-rules="ondemand" default="0" v-model="Detalhes.quantidade_meio_elos" label="Quantidade de 1/2 elos" class="q-mt-md" />
            <q-input outlined stack-label lazy-rules="ondemand" default="0" v-model="Detalhes.detalhes_adicionais" type="textarea" label="Detalhes Adicionais" class="q-mt-md" />
            </q-card>

        <q-card v-if="data.brand_id && data.brand_id === 'TH'" flat bordered style="max-width: 400px">
          <q-badge align="top">TAG Heuer </q-badge>
          <q-select outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"    :options="TiposGrupo.defeito_tag" v-model="data.defect_tag"  emit-value  map-options option-label="label" option-value="id" label="Defeito" class="q-mt-md" style ="min-width: 200px"/>
          <q-select v-if ="[2, 7,5].includes(data.tipo_reparo)" outlined stack-label  :rules="[val => !!val || 'Campo obrigatório']"   :options="TiposGrupo.warranty_tag" emit-value map-options  option-label="label" option-value="id" v-model="data.warranty_tag" label="Warranty code" class="q-mt-md" style ="min-width: 100px"/>
          <q-input v-if ="[2, 7].includes(data.tipo_reparo)" outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"  v-model="data.country_tag" label="País de venda" class="q-mt-md" style ="min-width: 100px"/>
        </q-card>
        <q-card v-if="data.brand_id && data.brand_id === 'BE'" flat bordered style="max-width: 400px">
          <q-badge align="top">Breitling</q-badge>
          <q-input outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"   v-model="data.tracking_id_breitling"  emit-value  map-options option-label="label" option-value="id" label="Tracking ID" class="q-mt-md" style ="min-width: 200px"/>
          <q-select outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"    :options="TiposGrupo.defeito_bre" v-model="data.defect_bre"  emit-value  map-options option-label="label" option-value="id" label="Defeito" class="q-mt-md" style ="min-width: 200px"/>
          <q-select v-if ="[2, 7].includes(data.tipo_reparo)" outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"   :options="TiposGrupo.pais_bre" emit-value map-options  option-label="label" option-value="id" v-model="data.pais_bre" label="País" class="q-mt-md" style ="min-width: 100px"/>
          <q-input v-if ="[2, 7].includes(data.tipo_reparo)" outlined stack-label  :rules="[val => !!val || 'Campo obrigatório']" v-model="data.ultimo_conserto_bre" label="último reparo" type="date" class="q-mt-md" style ="min-width: 100px"/>
            <q-input v-if ="[2, 7].includes(data.tipo_reparo)" outlined stack-label  :rules="[val => !!val || 'Campo obrigatório']" v-model="data.data_compra_bre" label="Data de compra***" class="q-mt-md" style ="min-width: 100px"/>
          </q-card>
        <q-card v-if="data.brand_id && data.brand_id === 'BV'" flat bordered>
          <q-badge align="top">Bulgari</q-badge>
          <q-input outlined stack-label  :rules="[val => !!val || 'Campo obrigatório']"  v-model="data.codigo_sap_bv"  emit-value  map-options option-label="label" option-value="id" label="Código SAP" class="q-mt-md" style ="min-width: 270px"/>
          <q-select outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"   :options="TiposGrupo.v02_bv" v-model="data.codigo_v02_bv_1"  emit-value  map-options option-label="label" option-value="id" label="V02 - Código de Sintomas - Clientes" class="q-mt-md" style ="min-width: 200px"/>
          <q-select outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"   :options="TiposGrupo.v01_bv" v-model="data.codigo_v01_bv_1" label="V01 - Código de Sintomas - Técnicos" emit-value  map-options option-label="label" option-value="id" class="q-mt-md" style ="min-width: 200px"/>
            <q-select outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"   :options="TiposGrupo.v02_bv" v-model="data.codigo_v02_bv_2"  emit-value  map-options option-label="label" option-value="id" label="V02 - Código de Sintomas - Clientes(2)" class="q-mt-md" style ="min-width: 200px"/>
          <q-select outlined stack-label :rules="[val => !!val || 'Campo obrigatório']"   :options="TiposGrupo.v01_bv" v-model="data.codigo_v01_bv_2" label="V01 - Código de Sintomas - Técnicos(2)" emit-value  map-options option-label="label" option-value="id" class="q-mt-md" style ="min-width: 200px"/>
          </q-card>
        <q-card v-if="data.brand_id && ['CA','BA','MB','OP','PI','JC','VC','PA'].includes(data.brand_id)" flat bordered>
          <q-badge align="top">RICHEMONT</q-badge>
          <div class="q-gutter-md row items-start">
            <q-toggle v-model="data.campanha_richemont" label="Campanha" color="grey-7" outlined style="min-width: 200px" v-if="data.tipo_reparo !== 9" type="text" />
          </div>
        </q-card>
          <q-dialog v-model="cameraModalOpen" maximized>
          <q-card class="custom-dialog-size">
            <q-card-section >
            <camera-modal v-if="cameraModalOpen" :photoType="photoType" :data="data" @modalClosed="stopCameraAndCloseModal"></camera-modal>
            </q-card-section>
          <q-card-section>
          <q-btn flat label="Close" @click="stopCameraAndCloseModal"></q-btn>
          </q-card-section>
        </q-card>
        </q-dialog>
    </div>
        </q-banner>
        <q-banner v-if="step === 1" class="q-px-lg" >
          <q-card flat bordered outlined margin align="around" >
            <q-card-actions>
            <q-card-section>
              <div class="text-h6">Dados do Relógio <br/><br/>  </div> 
            <q-item  @blur="onBlur" outlined v-if="serieshowResults" v-for="item in seriesearchResults" @click="selectItem(item)" clickable stack-label style="max-width: 400px">
              <q-item-section>
                <q-item-label>{{ `Série: ${item.serie} - ${item.nome}` }}</q-item-label>
                <q-item-label caption>{{ `${item.id} - ${item.data_os} - ${item.data_entrega_produto}` }}</q-item-label>
                <q-item-label caption>{{ `${item.tipo_reparo} - ${item.status_os}` }}</q-item-label>
              </q-item-section>
            </q-item>      
            <div v-if="data.tipo_reparo !== 9" class="row items-center q-gutter-xs"><br/>
            <q-input
            v-model="data.serie"
            use-input
            :rules="[val => !!val || 'Campo obrigatório']"
            use-chips
            hide-dropdown-icon
            @filter="fetchDataserie"
            input-debounce="100"
            label="Série"
            persistent
            outlined
            :disable="isSerieDisabled"
            >
          </q-input>
          <q-btn color="green" @click="fetchDataserie(data.serie)" label="Pesquisar" class="q-ml-sm" />
          <q-btn color="red" @click="semSerie()" label="Não possui Série" class="q-ml-sm" />
          <q-btn color="blue" @click="internaSerie()" label="Referência Interna" class="q-ml-sm" />
          
        </div> <br/>
       
          <q-item  @blur="onBlur" v-if="refshowResults" v-for="item in refsearchResults" @click="selectItemref(item)" clickable stack-label style="max-width: 400px">
              <q-item-section>
                <q-item-label>{{ `${item.referencia_produto} - ${item.modelo}` }}</q-item-label>
                <q-item-label caption>{{ `${item.marca} - ${item.calibre}` }}</q-item-label>
              </q-item-section>
            </q-item>
            <div class="row items-center q-gutter-xs">
            <q-input
            v-model="data.referencia_produto"
            use-input
            use-chips
            hide-dropdown-icon
            @filter="fetchDataref"
            input-debounce="100"
            label="Referência"
            outlined
            style="max-width: 400px"
            :rules="[val => !!val || 'Campo obrigatório']"
          >
          </q-input>
          <q-btn color="green" @click="fetchDataref(data.referencia_produto)" label="Pesquisar" class="q-ml-sm" />
        </div> <br/>
          <q-select
            label="Marca"
            input-debounce="0"
            :options="brandsFiltered"
            v-model="selectedBrand"
            @filter="filterBrand"
            stack-label
            use-input
            outlined
            option-label="label"
            option-value="value"
            map-options
            color="grey-7"
            style="max-width: 400px"
            :rules="[val => !!val || 'Campo obrigatório']"
          />
          <div class="row items-center q-gutter-xs">
            <q-input  outlined stack-label v-model="data.modelo" label="Modelo" :rules="[val => !!val || 'Campo obrigatório']" />
            <q-input v-if="data.tipo_reparo !== 9" outlined stack-label v-model="data.valor_produto" :rules="[val => !!val || 'Campo obrigatório']"  label="Valor Estimado" type="number" />
            
            

          </div>
          <q-select v-if="data.tipo_reparo !== 9" map-options :options="TiposMovimento" outlined stack-label use-input option-label="label" option-value="value" emit-value :rules="[val => !!val || 'Campo obrigatório']" v-model="data.tipo_movimento" label="Tipo de Movimento"   style="max-width: 200px"/>
          <q-select v-if="data.tipo_reparo !== 9" map-options  :options="TiposComplicação" emit-value outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" v-model="data.complicacao" label="Complicação"   style="max-width: 200px" />         
        </q-card-section>
        <q-space/>
        <q-card-section>
          <q-space/>
        <q-select
        v-model="data.tipo_reparo" :options="TiposdeReparo" label="Tipo de Reparo"
        outlined
        stack-label
        text-white
        option-label="label"
        option-value="id"
        emit-value
        map-options
        filter
        style="min-width:400px"
        class="q-ml-sm"
        :rules="[val => !!val || 'Campo obrigatório']"
        />
            <br/>
        <q-select
        v-model="data.loja" :options="Lojas" label="Loja"
        outlined
        stack-label
        text-white
        option-label="label"
        option-value="id"
        emit-value
        map-options
        filter
        style="min-width:400px"
        class="q-ml-sm"
        :rules="[val => !!val || 'Campo obrigatório']"
        /> 
    </q-card-section>
    <q-space/>

</q-card-actions>
        
        </q-card>
     
        </q-banner>
        <q-banner v-if="step === 2" class="q-px-lg">
          
          <div class="text-h6">Pesquisa Cliente </div> 
          <br/>
          <div class="row items-center q-gutter-xs">
            <q-select
        label="Pesquisa"
        outlined
        stack-label
        use-input
        hide-selected
        fill-input
        input-debounce="0"
        :options="ClienteResults"
        @filter="getProductsBySearch"
        type="find"
        v-model="data.product"
        color="grey-7"
        class="q-mt-md"
      >
        <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey">Sem opções</q-item-section>
          </q-item>
        </template>
      </q-select>
          <q-select :options="TipoPessoa"  class ="q-mt-md" outlined stack-label map-options lazy-rules="ondemand" v-model="data.tipo_pessoa" label = "Tipo de Pessoa" style="min-width: 200px"  option-label="label" option-value="id" emit-value/>
          <q-space/>
          <q-btn v-if="data.cliente_id" @click="limparDados()" type="submit" color="blue" label = 'Limpar Dados' />
          <q-btn
            icon="sync"
            color="green"
            class="q-mr-md wt-border"
            @click="sincronizarClientes()"
            :loading="loading"
            >
              <q-tooltip>Sincronizar clientes já cadastrados no Estoklus</q-tooltip>
          </q-btn>
          <q-btn :disable="!data.tem_hist" icon="timeline" label="Quick View" @click="openClickView()">
            <q-badge color="red" v-if="data.tem_hist">!</q-badge>
            </q-btn>
          <q-space/>
          <q-input outlined filled stack-label lazy-rules="ondemand"  v-model="data.cliente_id" label="Codigo Estoklus" class ="col" color="grey-7"  disabled readonly style="max-width: 200px"/>
          
          
          </div>
          <div class="row items-left justify-left   q-gutter-xs q-mt-md">
          <q-input   :rules="[val => !!val || 'Campo obrigatório']" outlined stack-label style="min-width: 80%" maxlength="60" v-model="data.nome" label="Nome" class ="row q-mt-md" color="grey-7"/>
          <q-input  :rules="[val => !!val || 'Campo obrigatório']" outlined stack-label lazy-rules="ondemand" v-if="data.tipo_pessoa && data.tipo_pessoa === 'F'" maxlength="11" v-model="data.cpf" label="CPF" class ="row q-mt-md" color="grey-7" style="max-width: 300px"/>
          <q-input   :rules="[val => !!val || 'Campo obrigatório']" outlined stack-label lazy-rules="ondemand"  v-if="data.tipo_pessoa && data.tipo_pessoa === 'J'" maxlength="14"  v-model="data.cnpj" label="CNPJ" class ="row q-mt-md" color="grey-7" style="max-width: 300px"/>
        </div>
        <br/>
        <div class="text-h6">Endereço </div> 
        
           <q-input
           use-input
           outlined
           hide-dropdown-icon
           @input="fetchEndereco"
           label="CEP"
           style="max-width: 400px "
           maxlength="8"
           v-model="selectedEndereco"
           
           />
           <br/>
          <div class="row items-center q-gutter-xs">
          
          <q-input outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" v-model="data.logradouro" label="Endereço" class ="col" color="grey-7" maxlength="45" style="max-width: 600px"/> 
          <q-input outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" v-model="data.numero" maxlength="10" label="Número" class ="col" color="grey-7" style="max-width: 300px"/>
          <q-input outlined stack-label :rules="[ 'Campo obrigatório']" v-model="data.complemento" maxlength="25" label="Complemento" class ="col" color="grey-7" style="max-width: 300px"/>
        </div>
        <br />
        <div class="row items-center q-gutter-xs">
          
          <q-input outlined stack-label :rules="[ 'Campo obrigatório']" v-model="data.bairro" label="Bairro" maxlength="30" class ="col" color="grey-7" style="max-width: 300px"/>
          <q-input outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" v-model="data.cidade" maxlength="30" label="Cidade" class ="col" color="grey-7" style="max-width: 300px"/>
          <q-input outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" v-model="data.uf" maxlength="2" label="UF" class ="col" color="grey-7" style="max-width: 300px"/>
          <q-input outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" maxlength="8" v-model="data.cep" readonly label="CEP" class ="col" color="grey-7" style="max-width: 300px"/>
        </div>
        <br />

        <div class="text-h6">Contatos </div> 
        <div class="row items-center q-gutter-xs">
          
          <q-input outlined stack-label lazy-rules="ondemand" v-model="data.tel_residencial" label="Residencial" class ="col" color="grey-7" maxlength="25" style="max-width: 300px"/>
          <q-input outlined stack-label lazy-rules="ondemand" v-model="data.tel_trabalho" label="Comercial" class ="col" color="grey-7" maxlength="25" style="max-width: 300px"/>
          <q-input outlined stack-label lazy-rules="ondemand" v-model="data.tel_celular" label="Celular" class ="col" color="grey-7" maxlength="25" style="max-width: 300px"/>
          <q-input outlined stack-label lazy-rules="ondemand" v-model="data.tel_outros" label="Outro" class ="col" color="grey-7" maxlength="25" style="max-width: 300px"/>
          
        </div>
        <br />
        <div class="row items-center q-gutter-xs">
          
          <q-input outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" v-model="data.email" label="E-mail" class ="col" color="grey-7" style="max-width: 300px"/>
          <q-input outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" v-model="data.nascimento" label="Data de nascimento"  type=date class ="col" color="grey-7" style="max-width: 300px"/>
        </div>
        <q-select :options="PreferenciaContato" :rules="[val => !!val || 'Campo obrigatório']" outlined stack-label v-model="data.tipo_contato" label="Forma desejada de contato" map-options emit-value class="q-mt-md" style="max-width: 300px" />
        
          
        
        </q-banner>

        </template>
    </q-stepper>   
    <error-dialog v-if="errorDialogVisible" :errors="receivedErrors" v-model="errorDialogVisible"></error-dialog>
    <QuickView :itens="history" v-model="quickviewvisible"></QuickView>
  </modal-form>
</template>

<script setup>
import { computed, ref,} from "@vue/reactivity";
import {watchEffect,watch,onMounted} from "vue"
import { toLocalISOString } from "../../functions";
import { useQuasar } from "quasar";
import OrdersServicesService from "../../services/Services";
import PurchaseOrdersService from "../../services/PurchaseOrdersService";
import ModalForm from "../../components/modal-os-form.vue";
import QuickView from "../../components/QuickView.vue";
import CameraModal from "../../components/CameraModal.vue";
import axios from "axios";
import ErrorDialog from '../../types/ErrorDialog.vue';
import { Notify } from 'quasar';
import AuthService from "../../services/AuthService";

const history = ref([])
const quickviewvisible = ref(false)
const selectedEndereco =  ref('')
const loading= ref(false)
const inputRef = ref(false)
const selectedBrand = ref('')
const errorDialogVisible = ref(false)
const receivedErrors = ref({})
const stepper = ref()
const step = ref(1)
const done1 = ref(false)
const done2 = ref(false)
const done3 = ref(false)
const brands = ref(['PR','SP','RJ']);
const brandsFiltered = ref([]);
const ClientesFiltered = ref([]);
const pesquisa = ref ('')
const TipoPessoa = ref([{id:'F',label:"Física"},{id:'J',label:"Jurídica"}])
const $q = useQuasar();
const props = defineProps(["showRequest", "modelValue","selectedService"]);
const emit = defineEmits(["update:showRequest", "update:modelValue", "confirm","modalClosed","os"]);
const Detalhes = ref({})
const data = ref({

    });
const selectedItemserie = ref(null);
const selectedItemref= ref(null);
const refsearchResults = ref([])
const seriesearchResults = ref([]);
const serieshowResults = ref(true);
const refshowResults = ref(true);
const selectedCliente = ref(null)
const formValue = ref("");
const text = ref("")
const toggles = ref({
  sedex: false,
  nf_entrada: true,
  envia_email:false,
  envia_whatsapp:false
  // outros toggles aqui...
});
const showCalibre = ref(false);
const showClientes = ref(false);
const calibreResults = ref([]);
const ClienteResults = ref([]);
const files = ref([]);
const uploader = ref(null);
const TiposGrupo = ref([]);
const video = ref(null);
const canvas = ref(null);
const webcam = ref(false);
const imageUrl = ref(false);
const cameraModalOpen = ref(false);
const photoType = ref('');
const currentUser = computed(() => AuthService.user);
const isSerieDisabled = ref(false)

const toggleFieldMap = {
  sedex: 'codigo_rastreio',
  // mapeamento para outros toggles aqui...
};
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

const Lojas = ref([
    { id: 'PR', label: 'Curitiba' },
    { id: 'SP', label: 'São Paulo' },
    { id: 'RJ', label: 'Rio de Janeiro' },
]);

const TiposMaterial = ref([
    { id: 1, label: 'Aço' },
    { id: 2, label: 'Prata' },
    { id: 3, label: 'Dourada' },
    { id: 4, label: 'Ouro' },
    { id: 5, label: 'PVD Rosa' },
    { id: 6, label: 'Titanium' },
    { id: 7, label: 'PVD Preto' },
    { id: 8, label: 'PVD Amarelo' },
    { id: 9, label: 'Ouro Branco' }
]);

const TiposMaterialVidro = ref([
    { id: 1, label: 'Saphira' },
    { id: 2, label: 'Mineral' },
    { id: 3, label: 'Acrílico' }
]);

const TiposCalendario = ref([
{ id: 1, label: 'Sem calendário' },
{ id: 2, label: '3 horas' },
{ id: 3, label: '6 horas' },
{ id: 4, label: '9 horas' },
{ id: 5, label: '12 horas'},
{ id: 6, label: 'Entre 4 e 5 horas'},
{ id: 7, label: 'Entre 5 e 6 horas'}
])

const TiposDetalhe = ref([
    { value: 1, label: 'riscada' },
    { value: 2, label: 'piques' },
    { value: 3, label: 'impactos' },
    { value: 4, label: 'Solta' },
    { value: 5, label: 'Faltando' },
    { value: 6, label: 'Sinais de impacto' },
    { value: 7, label: 'Quebrado' },
    { value: 8, label: 'Trincado' },
    { value: 9, label: 'Lascas na borda' },
    { value: 10, label: 'Oxidado' },
    { value: 11, label: 'Sinal de umidade' },
    { value: 12, label: 'Torto' },
    { value: 13, label: 'Marcas de ferramenta' },
    { value: 14, label: 'Faltando parafusos' },
    { value: 15 , label: 'Gasta'},
    { value: 16 , label: 'Arrebentada'},
    { value: 17 , label: 'Usada'},
    { value: 18 , label: 'Marcada'}, 
    { value: 19 , label: 'Manchada'}, 
    { value: 20 , label: 'Faltando Fivela'}, 
    { value: 21 , label: 'Passador arrebentado'}, 
    { value: 22 , label: 'Costura solta'}, 
    { value: 23 , label: 'Ressecada'}
]);

const TiposMovimento = ref([
{ value: 1, label: 'Quartz' },
{ value: 2, label: 'Automático' },
{ value: 3, label: 'Corda Manual' },
{ value: 4, label: 'Connected' }
]);

const TiposComplicação = ref([
{ value: 1, label: 'Três Ponteiros' },
{ value: 2, label: 'Cronógrafo' },
{ value: 3, label: 'Digital' },
]);

const PreferenciaContato = ref([
{ value: 1, label: 'E-mail' },
{ value: 2, label: 'Telefone' },
{ value: 3, label: 'Whatsapp' }
]);

const togglesValue = computed(() => toggles.value);

loadBrands();






watchEffect(() => {
  const newToggles = togglesValue.value;
  for (let toggle in newToggles) {
    if (!newToggles[toggle] && toggleFieldMap[toggle]) {
      delete data.value[toggleFieldMap[toggle]];
    }
  }
});

const showRequest = computed({
  get: () => {
    let requested;
    if (props.modelValue?.requested) {
      requested = toLocalISOString(new Date(props.modelValue?.requested));
    } else {
      requested = toLocalISOString(new Date());
    }
    data.value = {
      code: props.modelValue?.code,
      data_os: requested ? requested.slice(0, 10) : null,
      time: requested ? requested.slice(11) : "00:00",
      status: 1,
      username: currentUser.value.name,
      loja: currentUser.value.loja,
      estoklus_id: currentUser.value.estoklus_id,
      emite_nf: 'N'
    };
    Detalhes.value={
      estado_caixa: [],
      estado_coroa: [],
      estado_fundo: [],
      estado_indexes: [],
      estado_luneta: [],
      estado_mostrador: [],
      estado_ponsuares: [],
      estado_ponteiros: [],
      estado_pulseira: [],
      estado_tampa_fundo: [],
      estado_valvula: [],
      estado_vidro: [],
      estado_fecho: [],

    }

    if(props.showRequest == false){
      delete data.value
      delete Detalhes.value
      delete brandsFiltered.value
      selectedBrand.value = ''
      isSerieDisabled.value = false
    }

    return props.showRequest;
  },
  set: (value) => {
    emit("update:showRequest", value);
  },
});


async function confirm() {

    emit("update:showRequest", false);
    emit("confirm");
    emit("os",data.value)
    data.value = {}
    isSerieDisabled.value = false
    step.value = 1
}

const formatCPF = (cpf) => {
      if (!cpf) return '';
      return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
    };

    const formatCNPJ = (cnpj) => {
      if (!cnpj) return '';
      return cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, "$1.$2.$3/$4-$5");
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




const fetchDataref = async (val, update) => {
  try {
    
    if (val && val.length > 2){
    //const response = await axios.get(`https://sua-api.com/search?q=${val}`);
    const response = await OrdersServicesService.getServices({"referencia_produto.lk": val + "%",_limit:3,_offset:0,_order_d: "data_os"} )
    if (response.data.length == 0){
      Notify.create({
              type: 'warning',
              message: `Referência ${val}, não encontrada no histórico`
            });
    }
    else{
    const options = response.data.map(item => ({
      id: item.id, // Ajuste essas propriedades conforme os dados da sua API
      nome: item.nome,
      data_os: item.data_os,
      data_entrega: item.data_entrega_produto,
      documento: item.documento,
      referencia_produto: item.referencia_produto,
      serie: item.serie,
      modelo: item.modelo,
      tipo_reparo: item.tipo_reparo,
      status_os: item.status_os,
      calibre: item.calibre,
      material_caixa: item.material_caixa,
      material_caixa: item.material_caixa,
      marca: item.marca

    }));
    

    refsearchResults.value = options;
      refshowResults.value = true
      return refsearchResults;
    }
  }
  } catch (err) {
    console.error("Erro ao buscar dados:", err);
  }
};


const fetchCalibre = async (val,update) => {

  try{
  const response = await OrdersServicesService.getServices
    ({_select:"calibre",
      _distinct:true,
      _order_a: "calibre",
      "calibre.lk": val + '%',
    _limit:3,
    _offset:0})
    showCalibre.value = true;
    
    calibreResults.value = response.data?.map((l) => {
      return { label: l.calibre, value: l.calibre };
    });
  }
catch (err) {
    console.error("Erro ao buscar dados:", err);
  } 

};

function filterClientes(val, update) {


    fetchClientes(val)

      ClientesFiltered.value = ClienteResults.value;
    return;
}


async function getProductsBySearch(value, update, abort) {
  setTimeout(() => {
    update(async () => {
      if (value && value.length > 2) {      
        ClienteResults.value = [];
        const response = (await OrdersServicesService.getCustomers({
        "nome.lk,cnpj.lk,cpf.lk": '%'+value+'%',
        _limit: 10,
        _offset: 0,
        _order_a: "nome",
      })).data;

        for (let item of response) {
          ClienteResults.value.push({
            label: `${item.nome} (${item.id})`,
            bairro: item.bairro,
            cep: item.cep,
            cidade: item.cidade,
            cnpj: item.cnpj,
            codigo_tipo_pessoa: item.codigo_tipo_pessoa,
            complemento: item.complemento,
            cpf: item.cpf,
            email: item.email,
            id: item.id,
            logradouro: item.logradouro,
            nome: item.nome,
            numero: item.numero,
            tel_celular:item.tel_celular,
            tel_outros:item.tel_outros,
            tel_trabalho: item.tel_trabalho,
            uf: item.uf,
            codigo_ibge:item.codigo_ibge,
            nascimento:item.nascimento
   
          });
        }
      } else {
        ClienteResults.value = [];
      }
    });
  }, 2000);
}

const fetchClientes = async (val,update) => {
  if (val && val.length > 2){

try{
      const response = await OrdersServicesService.getCustomers({
        "nome.lk,cnpj.lk,cpf.lk": '%'+val+'%',
        _limit: 3,
        _offset: 0,
        _order_d: "nome",
      });
  
  ClienteResults.value = response.data?.map(item => ({
    label: item.nome,
    bairro: item.bairro,
    cep: item.cep,
    cidade: item.cidade,
    cnpj: item.cnpj,
    codigo_tipo_pessoa: item.codigo_tipo_pessoa,
    complemento: item.complemento,
    cpf: item.cpf,
    email: item.email,
    id: item.id,
    logradouro: item.logradouro,
    nome: item.nome,
    numero: item.numero,
    tel_celular:item.tel_celular,
    tel_outros:item.tel_outros,
    tel_trabalho: item.tel_trabalho,
    uf: item.uf,
    codigo_ibge:item.codigo_ibge,
    nascimento:item.nascimento
    }));

    showClientes.value = true;
}
catch (err) {
  console.error("Erro ao buscar dados:", err);
} 

}};

const fetchEndereco = async (val, update) => {

      
      if (val.length === 8) {
        try {
          const response = await axios.get(`https://viacep.com.br/ws/${val}/json/`);
          
          if (response.data.erro){
            Notify.create({
              type: 'warning',
              message: `CEP ${val} não localizado`
            });
          }

          else{
          
          const endereco = response.data;

          data.value.logradouro = endereco.logradouro.toUpperCase();
          data.value.bairro = endereco.bairro.toUpperCase();
          data.value.cidade = endereco.localidade.toUpperCase();
          data.value.uf = endereco.uf.toUpperCase();
          data.value.cep = val;
          data.value.codigo_ibge = endereco.ibge;

        }
        } catch (error) {
          console.error("Erro ao buscar CEP:", error);
        }
      }
    };


const selectCalibre = (value) => {

  data.value.calibre = value.value;
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

function convertDate(dateStr) {
      // Verifique se a data está no formato correto
      if (dateStr.match(/^\d{4}\-\d{2}\-\d{2}$/)) {
        return dateStr;
      }
      
      // Tente converter de DD/MM/AAAA para AAAA/MM/DD
      const parts = dateStr.split('/');
      if (parts.length === 3) {
        return `${parts[2]}-${parts[1]}-${parts[0]}`;
      }
      // Retorne a data original se não for possível converter
      return dateStr;
    }

const carregaCliente = (value)  => {

  if (value != undefined && value.id != undefined){
    const aniversario = convertDate(value.nascimento)
    data.value.bairro= value.bairro,
    data.value.cep= value.cep,
    data.value.cidade= value.cidade,
    data.value.cnpj= value.cnpj,
    data.value.tipo_pessoa= value.codigo_tipo_pessoa,
    data.value.complemento= value.complemento,
    data.value.cpf= value.cpf,
    data.value.email= value.email,
    data.value.cliente_id= value.id,
    data.value.logradouro= value.logradouro,
    data.value.nome= value.nome,
    data.value.numero= value.numero,
    data.value.tel_celular=value.tel_celular,
    data.value.tel_outros=value.tel_outros,
    data.value.tel_trabalho= value.tel_trabalho,
    data.value.uf= value.uf
    data.value.codigo_ibge = value.codigo_ibge,
    data.value.nascimento = aniversario
    showClientes.value = false
  }
}

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





const selectItem = (value) => {
 // Ajuste essas propriedades conforme os dados da sua API
  if (value.estoklus_id != ''){
    data.value.tipo_pessoa = value.codigo_tipo_pessoa;
    data.value.nome =  value.nome;
    data.value.cnpj =  value.documento;
    data.value.cpf =  value.documento;
    data.value.modelo =  value.modelo;
    data.value.modelo =  value.modelo;
    data.value.modelo =  value.modelo;
    data.value.ultima_os =  value.id;
    data.value.marca = value.marca;
    data.value.referencia_produto = value.referencia_produto;
    data.value.serie = value.serie;
    data.value.observacao = `Última OS - ${value.id}`
    }
  selectedBrand.value = value.marca;
  serieshowResults.value = false;
  const brand = brands.value.find(brand => brand.value === value.marca);


  
  if (brand) {

    selectedBrand.value = {
      label: brand.value,
      value: brand.value,
      brand_id: brand.brand_id
    };
  }


  Dados_cliente(value.documento);


};

const selectItemref = (value) => {
  // Ajuste essas propriedades conforme os dados da sua API
   data.value.referencia_produto =  value.referencia_produto;
  data.value.modelo =  value.modelo;
  data.value.calibre =  value.calibre;
  data.value.marca = value.marca;
  refshowResults.value = false;
  const brand = brands.value.find(brand => brand.value === value.marca);
  
  if (brand) {
    // Se a marca for encontrada, atribua ao selectedBrand
    selectedBrand.value = {
      label: brand.value,
      value: brand.value,
      brand_id: brand.brand_id
    };
  }

};

const register = () => {
  serieshowResults.value = false;
  // Lógica de cadastro aqui
};

const cancel = () => {
  // Lógica de cancelamento aqui
};

function onBlur() {
      // Esconda os resultados quando o componente perde o foco
      

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

  watch(step, async (newStep) => {
    if (newStep === 3){
      data.value.cliente_atualizado = false
    }
  if (newStep === 3 && data.value.marca === 'TAG HEUER' && !TiposGrupo.value.defeito_tag) {
    try {
      TiposGrupo.value.defeito_tag = await fetchGrupos('AB');
      TiposGrupo.value.reparo_tag = await fetchGrupos('TU');
      TiposGrupo.value.warranty_tag = await fetchGrupos('WX');
      
    } catch (error) {
    }
  }
    else if (newStep === 3 && data.value.marca === 'BREITLING' && !TiposGrupo.value.defeito_bre) {
    try {
      TiposGrupo.value.defeito_bre = await fetchGrupos('B04');
      TiposGrupo.value.reparo_bre = await fetchGrupos('B01');
      TiposGrupo.value.reparo_bre = TiposGrupo.value.reparo_bre.map(item => ({
        id: item.id,
        label: item.id + ' - ' + item.label}));

      TiposGrupo.value.pais_bre = await fetchGrupos('B05');
      
    } catch (error) {
    }
  }    else if (newStep === 3 && data.value.brand_id === 'BV' && !TiposGrupo.value.v01_bv) {
    try {
      TiposGrupo.value.v01_bv = await fetchGrupos('V01');
      TiposGrupo.value.v02_bv = await fetchGrupos('V02');
    } catch (error) {
    }
  }
});

watch(
  () => toggles.value.nf_entrada,
  (newValue) => {
    
    if (newValue === true) {

        data.value.emite_nf = 'N'
    }
    else{
      data.value.emite_nf = 'S'
    }
  }
);


watch(
  () => toggles.value.envia_whatsapp,
  (newValue) => {
    
    if (newValue === true) {
      const telefoneFormatado = validarTelefone(data.value.tel_celular);
      console.log(telefoneFormatado)
      if (telefoneFormatado) {
        data.value.enviar_wpp = 'S'
      } else {
        Notify.create({
              type: 'negative',
              message: `Telefone inválido ou em branco`
            });
            
            toggles.value.envia_whatsapp = false
            data.value.enviar_wpp = 'N'
      }
    }
    else{
      data.value.enviar_wpp = 'N'
    }
  }
);
watch(
  () => toggles.value.envia_email,
  (newValue) => {
    
    if (newValue === true) {
      const emailValido = validarEmail(data.value.email);
      console.log(emailValido)
      if (emailValido) {
        data.value.envia_email = 'S'
      } else {
        Notify.create({
              type: 'negative',
              message: `E-mail inválido ou em branco`
            });
            
            toggles.value.envia_email = false
            data.value.envia_email = 'N'
      }
    }
    else{
      data.value.envia_email = 'N'
    }
  }
);

watch(
            ()  => data.value.cpf,
           async (newValue) => { if (newValue && newValue.length == 11){
            history.value= []
              const response =  await axios.get(`https://app.watchtime.com.br/api/service_orders/quickview/${data.value.cpf}`)

const options = response.data.map(item => ({marca: item.marca  , 
  modelo:item.modelo,
  serie:item.serie    ,
  data_entrega: item.data_entrega,
  valor: item.valor ,
  unidade:item.unidade  ,
  tipo_servico: item.tipo_servico,id:item.id}));

  history.value = options
  console.log(history.value)
  if(history.value.length > 0){
  data.value.tem_hist = true
  console.log('tem_hist')
  }else data.value.tem_hist = false

            }
             
            }
        );

watch(
            () => selectedBrand.value,
            (newValue) => {
              data.value.marca = newValue.value;
              data.value.brand_id = newValue.brand_id;
            }
        );

watch(
      () => data.value.product,
      (newValue) => {
      carregaCliente(newValue)
      }
    );


    watch(
      () => selectedEndereco.value,
      (newValue) => {
      fetchEndereco(newValue)
      }
    );

  const validarEmail = (email) => {
    const regexEmail = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;

    if (regexEmail.test(email)) {
      return email; // retorna o e-mail caso seja válido
    }

    return null; // retorna null caso o e-mail não seja válido
  }

const validarTelefone = (numero) => {
  const numeroLimpo = numero.replace(/\D/g, '');

  // Verifica se o número tem o DDD e se ele tem 10 ou 11 dígitos (sem ou com o nono dígito)
  if (/^\d{10,11}$/.test(numeroLimpo)) {
    // Verifica se o número tem 11 dígitos (com o nono dígito)
    if (numeroLimpo.length === 11) {
      return numeroLimpo.replace(/^(\d{2})(\d{1})(\d{4})(\d{4})$/, '($1) $2 $3-$4');
    }
    // Verifica se o número tem 10 dígitos (sem o nono dígito)
    else if (numeroLimpo.length === 10) {
      return numeroLimpo.replace(/^(\d{2})(\d{4})(\d{4})$/, '($1) $2-$3');
    }
  }
  
  return null; // retorna null caso o número não seja válido ou não tenha DDD
}

const onFilesAdded = (newFiles) => {
      
    const file = newFiles[0];
      // Aqui você pode manipular o arquivo selecionado

    }

    const stopCameraAndCloseModal = () => {
            cameraModalOpen.value = false;
        };

    const openCamera = (type) => {
      photoType.value = type;
      cameraModalOpen.value = true;
    };

    function criarDescricao(obs,estado, mapeamento, item) {

      if (obs == null){
        obs = ''
      }

   const descricao = estado.map(value => {
    const tipoDetalhe = mapeamento.find(mapeamentoItem => mapeamentoItem.value === value);
    return tipoDetalhe ? tipoDetalhe.label : '';
  }).join(', ');

  // Retorna a string com o nome do item e as descrições

  return `${item}: ${obs} ${descricao}`;
}

function Descritivo() {
  const parts = [
    { texto: Detalhes.value.descricao_caixa,  estado: Detalhes.value.estado_caixa, nome: 'Caixa' },
    { texto: Detalhes.value.descricao_vidro,  estado: Detalhes.value.estado_vidro, nome: 'Vidro' },
    { texto: Detalhes.value.descricao_mostrador, estado: Detalhes.value.estado_mostrador, nome: 'Mostrador' },
    { texto: Detalhes.value.descricao_coroa,  estado: Detalhes.value.estado_coroa, nome: 'Coroa' },
    { texto: Detalhes.value.descricao_valvula, estado: Detalhes.value.estado_valvula, nome: 'Válvula' },
    { texto: Detalhes.value.descricao_fundo,  estado: Detalhes.value.estado_fundo, nome: 'Fundo' },
    { texto: Detalhes.value.descricao_indexes, estado: Detalhes.value.estado_indexes, nome: 'Índices' },
    { texto: Detalhes.value.descricao_luneta, estado: Detalhes.value.estado_luneta, nome: 'Luneta' },
    { texto: Detalhes.value.descricao_ponsuares, estado: Detalhes.value.estado_ponsuares, nome: 'Ponsuares' },
    { texto: Detalhes.value.descricao_tampa_fundo, estado: Detalhes.value.estado_tampa_fundo, nome: 'Tampa do Fundo' },
    { texto: Detalhes.value.descricao_pulseira, estado: Detalhes.value.estado_pulseira, nome: 'Pulseira' },
    { texto: Detalhes.value.descricao_ponteiros, estado: Detalhes.value.estado_ponteiros, nome: 'Ponteiros' },
    { texto: Detalhes.value.descricao_fecho,  estado: Detalhes.value.estado_fecho, nome: 'Fecho'} 
  ];

  data.value.descricao = '';



  parts.forEach(part => {
    if (part.estado.length > 0 || part.texto) {

      const descricao = criarDescricao(part.texto,part.estado, TiposDetalhe.value, part.nome);
      data.value.descricao += descricao + '. ';
    }
  

  });
  if (Detalhes.value.quantidade_elos != undefined && Detalhes.value.quantidade_elos != ''){
    data.value.descricao += ' Quantidade de elos: '+Detalhes.value.quantidade_elos;
  }
  if (Detalhes.value.quantidade_meio_elos != undefined && Detalhes.value.quantidade_meio_elos != ''){
    data.value.descricao += ' Quantidade de 1/2 elos: '+Detalhes.value.quantidade_meio_elos;
  }
  if (Detalhes.value.detalhes_adicionais != undefined){
    data.value.descricao += ' ' + Detalhes.value.detalhes_adicionais;
  }
  


}

 

const onSubmit = async () => {
  const validacao1 = true
  const validacao2 = true
  const validacao3 = true

      if(step.value === 1 ){
        let fields = { 
        'marca': "Marca", 
        'modelo': "Modelo", 
        'tipo_reparo':"Tipo de Reparo",
        'loja': "Loja"}
        if(data.value.tipo_reparo != 9){
          const fieldso = {'valor_produto': "Valor Estimado",'tipo_movimento':"Movimento",'complicacao':"Complicação",'serie': "Série",'referencia_produto':"Referência"}
          fields = {...fields, ...fieldso}
      
      }

        const errors = Object.keys(fields).filter(field => !data.value[field]).map(field => ({ id: fields[field], problem: "" }));
        if (errors.length > 0 && validacao1 === true) {
          receivedErrors.value = errors;
          errorDialogVisible.value = true
        } else {
          stepper.value.next();
        }
      }
      else if(step.value === 2 ){
        const fields = {'nome': "Nome", 
        'tipo_pessoa':"Tipo de Pessoa", 
        'cep': "CEP", 
        'logradouro': "Rua", 
        'numero': "Número", 
        'cidade':"Cidade", 
        'uf':"UF",
        'cliente_id':"Cliente não selecionado na pesquisa / ou não incluído"
        }
        const fieldsPF = {
        'cpf': "CPF",
        'cliente_atualizado': 'Atualização no Estoklus',
        'tipo_contato': 'Forma de Contato',
        'nascimento': 'Data de Nascimento',
        }

        let allFields = {...fields};
        if(data.value['tipo_pessoa'] === 'F') {
          allFields = {...allFields, ...fieldsPF}
            if(!data.value.tel_celular && !data.value.tel_outros && !data.value.tel_trabalho){
              const contato = {'contato':"Dados de contato"}
              allFields = {...allFields, ...contato}
            }
          }
        const errors = Object.keys(allFields).filter(field => !data.value[field]).map(field => ({ id: allFields[field], problem: "" }));

        if (errors.length > 0 || (data.value.tipo_pessoa === 'F' &&  !validaCPF(data.value.cpf)) ) {
          if(data.value.tipo_pessoa === 'F' &&  !validaCPF(data.value.cpf)){
            errors.push({id: 'CPF Inválido', problem: ""});
        }
          receivedErrors.value = errors;
          errorDialogVisible.value = true
        } 
        else {

          if(data.value.brand_id === 'BE'){

            if(data.value.tipo_pessoa === 'J'){

                const retorno = await OrdersServicesService.getTrackingID(data.value.cliente_id)
  
                if (retorno.data === ''){

                }else
                {
                  data.value.tracking_id_breitling = retorno.data
                }
            }
            else {
              if(data.value.loja === 'PR'){ data.value.tracking_id_breitling = 'BR100223' }
              if(data.value.loja === 'SP'){ data.value.tracking_id_breitling = 'BR100217' }
              if(data.value.loja === 'RJ'){ data.value.tracking_id_breitling = 'BR100218' }
            
            }

          }  
          stepper.value.next();
        }  
      }

  }


  function brand_id(val,update){
    data.value.brand_id = val.brand_id

  }


  const Dados_cliente = async (val) => {
  if (val && val.length > 1){

try{
const response = await OrdersServicesService.getCustomers
({"cnpj,cpf":val,_limit:1,_offset:0,_order_d: "nome"})

    carregaCliente(response.data[0])
}
catch (err) {
  console.error("Erro ao buscar dados:", err);
} 

}};



const inserirOS = async () => {
  loading.value = true
  try {
    
    Descritivo()

    if(step.value === 3 ){
        const fields = {'defeito': "Defeito"}
        let allFields =  {...fields};
        if(toggles.value.sedex === true){
          const fieldsedex = {'codigo_rastreio':"Código de Rastreio"}

          allFields = {...allFields,...fieldsedex}  

        }
        
        if(data.value.tipo_pessoa === 'J'){
          const fieldsloja ={"os_loja":"Os da Loja"}
          allFields = {...allFields,...fieldsloja}  
        }
        if(data.value.brand_id === 'TH'){
          const fieldsTAG ={"defect_tag":"Defeitos TAG"}
          allFields = {...allFields,...fieldsTAG} 
          if(data.value.tipo_reparo === '2'){
            const fieldsTAGG ={"warranty_tag":"Tipo de Garantia","country_tag":"País de Venda"}
            allFields = {...allFields,...fieldsTAGG} 
          }
        }
        if(data.value.brand_id === 'BV'){
          const fieldsBV ={"codigo_sap_bv":"Código SAP","codigo_v01_bv_1":"V01 - Defeitos","codigo_v02_bv_1":"V02 - Defeitos"}
          allFields = {...allFields,...fieldsBV}
        }
        if(data.value.brand_id === 'BE'){
          const fieldsBE ={"tracking_id_breitling":"Tracking ID(BR da loja)"}
          allFields = {...allFields,...fieldsBE}
          if(data.value.tipo_reparo === '2'){
            const fieldsBEG ={"ultimo_conserto_bre":"Data do último Conserto","pais_bre":"País de Venda"}
            allFields = {...allFields,...fieldsBEG} 
          }
        }if(toggles.nf_entrada){
          const fieldNF ={"nf_entrada":"NF de Entrada (se não tiver - desativar o botão)"}
          allFields = {...allFields,...fieldsBE}
        }

        

        const errors = Object.keys(allFields).filter(field => !data.value[field]).map(field => ({ id: allFields[field], problem: "" }));
        if (errors.length > 0) {
          receivedErrors.value = errors;
          errorDialogVisible.value = true
        } else {
         const response = await OrdersServicesService.addOS(data.value)

          if(response.success){
            data.value.codigo_estoklus = parseInt(response.success.substring(2), 10);
            data.value.id = `${data.value.loja}${data.value.codigo_estoklus}`
                    if(data.value.enviar_wpp && data.value.enviar_wpp == 'S'){
                      const responseWPP = await axios.post(
        `https://app.watchtime.com.br/api/wpp/envia_OS`,data.value
      );      
      if(responseWPP.data == null){
        Notify.create({
              type: 'positive',
              message: `Whatsapp enviado`
            });

      }
                    }
                    if(data.value.envia_email && data.value.envia_email == 'S'){
                    const responseMail  =  await axios.post(
        `https://app.watchtime.com.br/api/mail/via_abertura`,data.value
      );  
      if(responseMail.data == 'OK'){
        Notify.create({
              type: 'positive',
              message: `E-mail enviado`
            });

      } 
      }   
      
            confirm()
      Notify.create({
              type: 'positive',
              message: `OS ${response.success}, criada no estoklus`
            });

    }

    else{

      Notify.create({
              type: 'negative',
              message: response.error
            });
    }
        }
        }
    
    

    }
 catch (err) {
    console.error("Erro ao buscar dados:", err);
  }
  loading.value = false
};

const inserirCliente = async () => {

  const fields = {'nome': "Nome", 
        'tipo_pessoa':"Tipo de Pessoa", 
        'cep': "CEP", 
        'logradouro': "Rua", 
        'numero': "Número", 
        'cidade':"Cidade", 
        'uf':"UF"
        }
        const fieldsPF = {
        'cpf': "CPF",
        'tipo_contato': 'Forma de Contato',
        'nascimento': 'Data de Nascimento',
        }

        let allFields = {...fields};
        if(data.value['tipo_pessoa'] === 'F') {
          allFields = {...allFields, ...fieldsPF}
            if(!data.value.tel_celular && !data.value.tel_outros && !data.value.tel_trabalho){
              const contato = {'contato':"Dados de contato"}
              allFields = {...allFields, ...contato}
            }
          }
        const errors = Object.keys(allFields).filter(field => !data.value[field]).map(field => ({ id: allFields[field], problem: "" }));

        if (errors.length > 0 || (data.value.tipo_pessoa === 'F' &&  !validaCPF(data.value.cpf)) ) {
          if(data.value.tipo_pessoa === 'F' &&  !validaCPF(data.value.cpf)){
            errors.push({id: 'CPF Inválido', problem: ""});
        }
          receivedErrors.value = errors;
          console.log(receivedErrors)
          errorDialogVisible.value = true
        } 
        else {


  loading.value = true
  try {
   
    const response = await OrdersServicesService.addCustomer(data.value)
    if(response.success){
      data.value.cliente_atualizado = true
      Notify.create({
              type: 'positive',
              message: `Cliente Código ${response.success}, criado no estoklus`
            });

        data.value.cliente_id = response.success

    }

    else{

      Notify.create({
              type: 'warning',
              message:  'Cliente já cadastrado no estoklus'
            });
    }

    }
 catch (err) {
    console.error("Erro ao buscar dados:", err);
  }
}
  loading.value = false
};

function limparDados(){
  data.value.bairro= '',
  data.value.cep= '',
  data.value.cidade= '',
  data.value.cnpj= '',
  data.value.tipo_pessoa= '',
  data.value.complemento= '',
  data.value.cpf= '',
  data.value.email= '',
  data.value.cliente_id= '',
  data.value.logradouro= '',
  data.value.nome= '',
  data.value.numero= '',
  data.value.tel_celular='',
  data.value.tel_outros='',
  data.value.tel_trabalho= '',
  data.value.uf= ''
  data.value.nascimento= ''
  data.value.product= ''

}

const semSerie = () => {
  data.value.serie = ' ';
  isSerieDisabled.value = true

}

const internaSerie = () => {
  data.value.serie = 'NA';
  isSerieDisabled.value = true

}

const openClickView = async () => {
  quickviewvisible.value = true

  const response =  await axios.get(`https://app.watchtime.com.br/api/service_orders/quickview/${data.value.cpf}`)

  const options = response.data.map(item => ({marca: item.marca  , 
    modelo:item.modelo,
    serie:item.serie    ,
    data_entrega: item.data_entrega,
    valor: item.valor ,
    unidade:item.unidade  ,
    tipo_servico: item.tipo_servico,
  id:item.id}));

    history.value = options
    

}


const atualizarCliente = async () => {

  const fields = {'nome': "Nome", 
        'tipo_pessoa':"Tipo de Pessoa", 
        'cep': "CEP", 
        'logradouro': "Rua", 
        'numero': "Número", 
        'cidade':"Cidade", 
        'uf':"UF"
        }
        const fieldsPF = {
        'cpf': "CPF",
        'tipo_contato': 'Forma de Contato',
        'nascimento': 'Data de Nascimento',
        }

        let allFields = {...fields};
        if(data.value['tipo_pessoa'] === 'F') {
          allFields = {...allFields, ...fieldsPF}
            if(!data.value.tel_celular && !data.value.tel_outros && !data.value.tel_trabalho){
              const contato = {'contato':"Dados de contato"}
              allFields = {...allFields, ...contato}
            }
          }
        const errors = Object.keys(allFields).filter(field => !data.value[field]).map(field => ({ id: allFields[field], problem: "" }));

        if (errors.length > 0 || (data.value.tipo_pessoa === 'F' &&  !validaCPF(data.value.cpf)) ) {
          if(data.value.tipo_pessoa === 'F' &&  !validaCPF(data.value.cpf)){
            errors.push({id: 'CPF Inválido', problem: ""});
        }
          receivedErrors.value = errors;
          console.log(receivedErrors)
          errorDialogVisible.value = true
        } 
        else {



  loading.value = true
  try {
   
    const response = await OrdersServicesService.updateCustomer(data.value)
    if(response.success){
      data.value.cliente_atualizado = true
      Notify.create({
              type: 'positive',
              message: `Cliente Código ${response.success}, atualizado no estoklus`
            });
    }

    else{

      Notify.create({
              type: 'negative',
              message: response
            });
    }

    }
 catch (err) {
    console.error("Erro ao buscar dados:", err);
  }
  loading.value = false
}
};

const sincronizarClientes = async () => {
  loading.value = true
  try {
   
    const response = await axios.get('https://app.watchtime.com.br/api/service_orders/clientes')
    if(response.data == 'OK'){
      Notify.create({
              type: 'positive',
              message: `Clientes Importados`
            });
          }
    else{
      Notify.create({
              type: 'yellow',
              message: `Sem novos clientes para importar`
            });
    }
    }
 catch (err) {
    console.error("Erro ao buscar dados:", err);
  }
  loading.value = false
};

function validaCPF(cpf) {
  if(typeof cpf !== "string") return false
  cpf = cpf.replace(/[\s.-]*/gim, '')
  if (
      !cpf ||
      cpf.length != 11 ||
      cpf == "00000000000" ||
      cpf == "11111111111" ||
      cpf == "22222222222" ||
      cpf == "33333333333" ||
      cpf == "44444444444" ||
      cpf == "55555555555" ||
      cpf == "66666666666" ||
      cpf == "77777777777" ||
      cpf == "88888888888" ||
      cpf == "99999999999"
  ) return false
  var soma = 0
  var resto
  for (var i = 1; i <= 9; i++)
    soma = soma + parseInt(cpf.substring(i - 1, i)) * (11 - i)
  resto = (soma * 10) % 11
  if (resto == 10 || resto == 11) resto = 0
  if (resto != parseInt(cpf.substring(9, 10))) return false
  soma = 0
  for (var i = 1; i <= 10; i++)
    soma = soma + parseInt(cpf.substring(i - 1, i)) * (12 - i)
  resto = (soma * 10) % 11
  if (resto == 10 || resto == 11) resto = 0
  if (resto != parseInt(cpf.substring(10, 11))) return false
  return true
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
</style>
