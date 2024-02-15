<template>
    <q-dialog maximized  v-model="showRepair">
     
        <q-card  style="width:90%"  class="wt-border q-pa-md">
      <q-card-section class="row items-center q-pa-none">
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>
      <q-card-section class="row q-pt-none">
        <div class="q-mb-md col-md-12">
          <q-stepper
            v-model="step"
            ref="stepper"
            color="secondary"
            flat
            animated
            done-color="green"
            active-color="red"
            inactive-color="grey"
            active-icon="pin_drop"
          >
            <q-step
              :name="1"
              title="Aberta"
              icon="miscellaneous_services"
              :caption="formatDate(data.data_aprovado)"
              :done="step > 1"
            >
  </q-step>

            <q-step
              :name="2"
              title="Orçada"
              icon="pause"
              :done="step > 2"
              :caption="formatDate(data.data_liberado_execucao)"
            />

            <q-step
              :name="3"
              title="Aprovada"
              icon="stream"
              :done="step > 3"
              :caption="formatDate(data.data_inicio_preparacao)"
            />
            <q-step
              :name="4"
              title="Laboratório"
              icon="fluorescent"
              :done="step > 4"
              :caption="formatDate(data.data_inicio_polimento)"
            />
            <q-step
              :name="5"
              title="Conserto"
              icon="build"
              :done="step > 5"
              :caption="formatDate(data.data_inicio_conserto)"
            />
            <q-step
              :name="6"
              title="Controle de Qualidade"
              icon="camera_enhance"
              :done="step > 6"
              :caption="formatDate(data.data_termino_conserto)"
            />
            <q-step
              :name="7"
              title="Liberado para Entrega"
              icon="done"
              :done="step==8"
              :caption="formatDate(data.data_liberado_entrega)"
            />
            <q-step
              :name="8"
              title="Entregue"
              icon="done"
              :done="step==8"
              :caption="formatDate(data.data_liberado_entrega)"
            />
          </q-stepper>
          <q-separator color="gray-5 q-my-sm" />
        </div>
        </q-card-section>
      <q-card-section class="row q-pt-none">
        <div class="row q-gutter-x-md">
          <div class="q-mb-sm" v-if="data.codigo_estoklus">
            <q-icon name="description" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Código OS: {{ data.codigo_estoklus}}</span
            >
          </div>
          <div class="q-mb-sm">
            <q-icon name="person" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Cliente: {{ data.nome }}</span
            >
          </div>
          <div class="q-mb-sm">
            <q-icon name="watch" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Marca: {{ data.marca }}</span
            >
          </div>
          <div class="q-mb-sm">
            <q-icon name="watch" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Modelo: {{ data.modelo }}</span
            >
          </div>
          <div class="q-mb-sm">
            <q-icon name="person" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Responsável: {{ data.nome_tecnico }}</span
            >
          </div>
          <div class="q-mb-sm">
            <q-icon name="insert_invitation" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Data prevista: {{ formatDate(data.data_prevista, 'date') }}</span
            >
          </div>


          <div class="q-mb-sm">
            <q-icon name="construction" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Fase atual:
              {{ data.nome_status}}</span
            >
          </div>
          <div class="q-mb-sm">
            <q-icon name="add_shopping_cart" class="info-container" />
            <span class="text-weight-medium text-caption"
              >Status:
              {{ data.nome_fase }}</span
            >
          </div>

        </div>  
        </q-card-section>   
        <q-separator color="gray-5 " />
      <q-card-section>
  
        <div class="q-pa-md" style="display: block; width: 100%;">
  <div class="q-gutter-y-md" style="max-width: 80%; margin: 0 auto;">
        <q-card>
            <q-card-actions>
            <q-btn size="large" v-if="tab > 1"  color="grey-8" @click="retorna()" icon="first_page"/>
            <q-space/>
            <q-btn size="large" v-if="tab < 7" color="green" @click="avanca()" icon="last_page"/>   
          </q-card-actions>
          <q-tabs
            v-model="tab"
            dense
            class="text-grey"
            active-color="green"
            indicator-color="primary"
            align="center"
            narrow-indicator
          >
          <q-tab  v-if="tab==1" name=1 :icon="iconeCons" label="Aguardando Peças" />
          <q-tab  v-if="tab==2" name=2 :icon="iconeCons" label="Laboratório" />
          <q-tab v-if="tab==3" name=3 :icon="iconePrep" label="Preparação" />
            <q-tab  v-if="tab==4" name=4 :icon="iconePol" label="Polimento" />
            <q-tab  v-if="tab==5" name=5 :icon="iconeCons" label="Conserto" />
            <q-tab  v-if="tab==6" name=6 :icon="iconeCons" label="Controle de Qualidade" />
          <q-tab  v-if="tab==7" name=7 :icon="iconeCons" label="Liberado para Entrega" />
          </q-tabs>
  
          <q-separator />

          <q-tab-panels v-model="tab" animated>
            <q-tab-panel name=1>
              <div class="row">
              <q-input @keydown.enter="consultaPeca(pesquisa)" 
                    label="Inserir Produto"  
                    style="width:20%" 
                    class="q-pa-none"
                    v-model="pesquisa"
                  >
                    <q-btn  color="yellow-7"  @click="consultaPeca(pesquisa)" icon="search" class="q-mt-md" :disabled="pesquisa == ''">
                      <q-tooltip>Opcional</q-tooltip></q-btn>
                  </q-input>
                <q-space/>
                <q-input class="q-pr-sm" outlined style="width:10%" v-model="product.quantidade" label="Quantidade"/>
                <q-input class="q-pr-sm" readonly outlined v-model="product.referencia" label="Referência"/>
                <q-input class="q-pr-sm" readonly outlined v-model="product.label" style="width:40%" label="Descrição"/>
                <q-input class="q-pr-sm" style="width:10%" readonly outlined v-model="product.id" label="Cód. Prod"/>
                <q-btn label="inserir" @click="inserePeca()" color="red" :disabled="!product.id || !product.label || !product.referencia" class="q-mt-md q-pl-lg"/>

                </div>
            <q-table
                    style="max-width:100%"
                    flat bordered
                    ref="tableRef"
                    :rows="data.itens"
                    :columns="columns"
                    :pagination="{ rowsPerPage: 0 }"
                    row-key="referencia_produto"
                    class="q-mt-md"
                    hide-bottom

                  >
                    <template v-slot:body="props">
      <q-tr v-if="props.row.servico == 'P' && props.row.codigo_produto != '0000801' && props.row.quantidade >0" :props="props">
        <q-td>
          <q-btn icon="assignment_return" @click="devolverPeca(props.row.codigo_pecas_servicos,props.row.quantidade)" size="small" v-if="props.row.quantidade_retirada > 0"></q-btn>
          <q-btn icon="do_disturb_on" @click="desativarPeca(props.row.codigo_pecas_servicos)" size="small" v-if="props.row.quantidade_retirada == 0 & props.row.tipo!='S'"></q-btn>
          <q-btn icon="delete" @click="removerPeca(props.row.codigo_pecas_servicos)" size="small" v-if="props.row.quantidade_retirada == 0 && props.row.tipo == 'S'"></q-btn>
          <q-tooltip v-if="props.row.quantidade_retirada > 0">Devolver Peça(s)</q-tooltip>
          <q-tooltip v-if="props.row.quantidade_retirada == 0 && props.row.tipo == 'S'">Excluir item</q-tooltip>
          <q-tooltip v-if="props.row.quantidade_retirada == 0 && props.row.tipo != 'S'">Desativar item</q-tooltip>
        </q-td>
        <q-td >
          <q-input :disable="(props.row.quantidade_a_retirar <= 0 && props.row.estoque <=0) || (props.row.quantidade_retirada >= props.row.quantidade)" filled style="width:100px" v-model.number="props.row.quantidade_a_retirar" default>
            <template v-if="props.row.quantidade <= props.row.quantidade_retirada" v-slot:append> <q-icon name="done" color="green" /></template>
            <template v-else="props.row.quantidade_a_retirar <= 0 && props.row.estoque <= 0" v-slot:append> <q-icon name="warning" color="primary" /></template></q-input>
            <q-tooltip v-if="props.row.quantidade_a_retirar <= 0 && props.row.estoque <= 0">Sem estoque</q-tooltip>
          </q-td>
        <q-td>
          {{ props.row.referencia_produto }}
        </q-td>
        <q-td>
          {{ props.row.quantidade }}

        </q-td>
        <q-td>
          {{ props.row.estoque }}

        </q-td>
        <q-td>
          {{ props.row.quantidade_retirada }}

        </q-td>
        <q-td>
          {{ props.row.descricao }}

        </q-td>
      </q-tr>
    
    </template>
                  </q-table>
                  <div class="row">
      <q-btn class="q-my-lg" color="green" icon="file_download" @click="baixaPecas()" > <q-tooltip>Baixar Peças</q-tooltip></q-btn>
      <q-space/>
      <q-btn class="q-my-lg" v-if="data.tipo_reparo && data.tipo_reparo == '9' && step == 1" label="Liberar OS" color="red" icon="done" @click="liberarOSAcessorio()"> </q-btn>
        <q-btn class="q-my-lg" v-if="data.tipo_reparo && data.tipo_reparo !='9' && step == 1" label="Enviar para Laboratório" color="red" icon="keyboard_tab" @click="openEnviarOficina()"> </q-btn>
      </div>
        </q-tab-panel>




        <q-tab-panel name=2>
        <div class="q-pa-md" >
          <div class="row justify-between">
            <div class="column">
    <q-list bordered padding>
      <q-item>
        <q-item-section>
          <q-item-label>Serviços</q-item-label>
        </q-item-section>

      </q-item>

      <q-separator spaced />
      
      <q-item   outlined v-for="item in data.itens.filter(item => item.servico === 'S')" stack-label style="max-width: 400px">
              <q-item-section>
                <q-item-label>{{ `${item.descricao} - ${item.referencia_produto}` }}</q-item-label>
              </q-item-section>
            </q-item>  
      </q-list>

            </div>

            <div v-if="data.polimento">
              <q-toggle label = 'Será realizado Polimento?'
      checked-icon="done"
        color="green"
        unchecked-icon="close"
        :disable="step != 2" 
        v-model="data.polimento" ></q-toggle>  
            <div class="text-h6">Data de Início Preparação</div>
                <div class="row">
              <q-input @keydown.h="() => inserirDataAtual('data_inicio_preparacao')"  :disable="step != 2" v-model="data.data_inicio_preparacao" outlined type="date"></q-input>
              <q-space/>
            </div>
            <div class="text-h6">Técnico</div>
                <div class="row">
                    <q-select v-model="data.tecnico_preparacao"   :disable="step != 2" outlined input-debounce="0" emit-value :options="UsersFiltered"  use-chips stack-label use-input color="grey-7"  @filter="filterUsers"/>
                    <q-space/>  
                </div>
            </div>
            <div v-if="!data.polimento">
              <q-toggle label = 'Será realizado Polimento?'
      checked-icon="done"
        color="green"
        unchecked-icon="close"
        v-model="data.polimento"
        :disable="step != 2" ></q-toggle>  
            <div class="text-h6">Data de Início Conserto</div>
                <div class="row">
              <q-input @keydown.h="() => inserirDataAtual('data_inicio_conserto')"  :disable="step != 2" v-model="data.data_inicio_conserto" outlined type="date"></q-input>
              <q-space/>
            </div>
            <div class="text-h6">Técnico</div>
                <div class="row">
                    <q-select v-model="data.tecnico_servico"  :disable="step != 2" outlined input-debounce="0" emit-value :options="UsersFiltered"  use-chips stack-label use-input color="grey-7"  @filter="filterUsers"/>
                    <q-space/>  
                </div>
            </div>
    </div>
      </div>
      <div class="row">

      <q-space/>
      <q-btn class="q-my-lg" v-if="data.fase == '10' && data.polimento == false" label="Iniciar Conserto" :disabled="!data.data_inicio_conserto || data.data_inicio_conserto.length < 8 || !data.tecnico_servico" color="green" icon="keyboard_tab" @click="enviarConserto()"> </q-btn>
        <q-btn class="q-my-lg" v-if="data.fase == '10' && data.polimento" :disabled="!data.data_inicio_preparacao || data.data_inicio_preparacao.length < 8 || !data.tecnico_preparacao || step != 2" label="Iniciar Preparação (Desmontagem)" color="green" icon="keyboard_tab" @click="enviarPreparacao()"> </q-btn>
      </div>
    </q-tab-panel>
      <q-separator spaced inset="item" />
            <q-tab-panel name=3>

          <div class="row justify-between q-mt-md q-mr-md q-ml-md">

            <div class="row">
              <div>
                <div class="text-h6">Data de Término Preparação</div>
                  <div class="row">
                      <q-input @keydown.h="() => inserirDataAtual('data_termino_preparacao')" :disable="!editando.tprep" v-model="data.data_termino_preparacao" outlined type="date"></q-input>
                      <q-btn v-if="!editando.tprep" :disable="step !=3"  class="q-ml-sm" size="large" color="grey-8" @click="edita('tprep')" icon="edit"/>
                      <q-btn v-if="editando.tprep" class="q-ml-sm" size="large" :disabled="data.data_termino_preparacao.length < 8" color="green" @click="editando.tprep=false" icon="save"/>            
                  </div>

                </div>
              </div>
              <div>
                            <div class="text-h6">Data de Início Polimento</div>
                <div class="row">
                  <q-input @keydown.h="() => inserirDataAtual('data_inicio_polimento')"  :disable="data.fase != '40' || data.data_termino_preparacao.length < 8 || editando.tprep " v-model="data.data_inicio_polimento" outlined type="date"></q-input>
                </div>
                <div class="text-h6">Técnico</div>
                  <div class="row">
                      <q-select v-model="data.tecnico_polimento"  :disable="data.fase != '40'  || data.data_termino_preparacao.length < 8 || editando.tprep " outlined input-debounce="0" emit-value :options="UsersFiltered"  use-chips stack-label map-options use-input color="grey-7"  @filter="filterUsers"/>
                      <q-space/>  
                  </div>
                </div>
            </div>
            <div class="row">
            <q-space/>
                  
                    <q-btn class="q-my-lg" :disable="data.fase != '40' ||!data.data_inicio_polimento || data.data_inicio_polimento.length < 8 || !data.tecnico_polimento" label="Iniciar Polimento" color="red" icon="keyboard_tab" @click="enviarPolimento()"> </q-btn>
            </div>
            </q-tab-panel>
  
            <q-tab-panel  name=4>
              <div class="row justify-between q-mt-md q-mr-md q-ml-md">

              <div class="row">
                <div>
                  <div class="text-h6">Data de Término Polimento</div>
                    <div class="row">
                        <q-input @keydown.h="() => inserirDataAtual('data_termino_polimento')" :disable="!editando.tpol" v-model="data.data_termino_polimento" outlined type="date"></q-input>
                        <q-btn v-if="!editando.tpol" :disable="step !=4"  class="q-ml-sm" size="large" color="grey-8" @click="edita('tpol')" icon="edit"/>
                        <q-btn v-if="editando.tpol" class="q-ml-sm" size="large" :disabled="data.data_termino_polimento.length < 8" color="green" @click="editando.tpol=false" icon="save"/>            
                    </div>
                  
                  </div>
                </div>
                <div>
                              <div class="text-h6">Data de Início Conserto</div>
                  <div class="row">
                    <q-input @keydown.h="() => inserirDataAtual('data_inicio_conserto')"  :disable="step != 4 || data.data_termino_polimento.length < 8 || editando.tpol " v-model="data.data_inicio_conserto" outlined type="date"></q-input>
                  </div>
                  <div class="text-h6">Técnico</div>
                    <div class="row">
                        <q-select v-model="data.tecnico_servico"  :disable="step != 4 || data.data_termino_preparacao.length < 8 || editando.tprep " outlined input-debounce="0" emit-value :options="UsersFiltered"  use-chips stack-label use-input color="grey-7"  @filter="filterUsers"/>
                        <q-space/>  
                    </div>
                  </div>
              </div>
              <div class="row">
              <q-space/>

                      <q-btn class="q-my-lg"  :disable="data.fase != '41' ||!data.data_inicio_conserto|| data.data_inicio_conserto.length < 8 || !data.tecnico_servico" label="Iniciar Conserto" color="red" icon="keyboard_tab" @click="enviarConserto()"> </q-btn>
              </div>
              
            </q-tab-panel>
  
            <q-tab-panel name=5>

                <div class="text-h6">Data de Término</div>
              <div class="row">
              <q-input @keydown.h="() => inserirDataAtual('data_termino_conserto')"  :disable="step != 5" v-model="data.data_termino_conserto" outlined type="date"></q-input>
              <q-space/>
            </div>
              <div class="row">
                <q-btn class="q-my-lg" v-if="data.fase == '06'" :disabled="step !=5" label="Retornar para Polimento" color="red" icon="keyboard_return" @click="openEnviarOficina()"> </q-btn>
              <q-space/>  
              <div class="row">
                
                <q-space/>
                  <q-btn class="q-my-lg" v-if="data.fase == '06'" :disabled="!data.data_termino_conserto || data.data_termino_conserto.length < 8 || step !=5" label="Enviar para Controle de qualidade" color="green" icon="keyboard_tab" @click="enviarQA()"> </q-btn>
                </div>

            </div>
            </q-tab-panel>
            <q-tab-panel name=6>
              <div class="text-h6">Informações da OS</div>
              <div class ="row">
              <q-input
            outlined
            stack-label
            label="Defeito"
            type="textarea"
            v-model="data.defeito"
            color="grey-7"
            readonly
          />
          <q-input
            outlined
            stack-label
            readonly
            label="Diagnóstico"
            type="textarea"
            v-model="data.diagnostico_tecnico"
            color="grey-7"
            class="q-ml-sm"
          />
          <div>
          <q-select
        v-model="data.tipo_reparo" :options="TiposdeReparo" label="Tipo de Reparo"
        outlined
        stack-label
        text-white
        :readonly="data.fase != '07'"
        option-label="label"
        option-value="id"
        emit-value
        map-options
        filter
        class="q-ml-sm"
        />

        <q-select label="Tipo de Movimento"  v-if="data.tipo_reparo !== 9" map-options  :readonly="data.fase != '07'" :options="TiposMovimento" emit-value outlined stack-label v-model="data.tipo_mecanismo" class="q-ml-sm q-mt-sm"  />         
      </div>   
        <q-list style ="max-width:40%" bordered padding class="q-ml-sm">
      
      <q-item   outlined v-for="item in data.itens.filter(item => item.servico === 'S')" stack-label style="max-width: 400px">
        <q-separator spaced />
              <q-item-section>
               
                <q-item-label>{{ `${item.descricao}` }}</q-item-label>
                
              </q-item-section>
             
            </q-item>  
            
      </q-list>
        </div>
            <div class="text-h6">Aferições</div>
            <div class="row">
                  <q-input      :readonly="data.fase != '07'" v-if="data.tipo_mecanismo == '2'" label = "Amplitude" outlined stack-label lazy-rules="ondemand"     v-model="data.amplitude"    class="q-pr-sm" color="grey-7"/>
                  <q-input  :readonly="data.fase != '07'" v-if="data.tipo_mecanismo == '2'" label = "Variação S/D" outlined stack-label lazy-rules="ondemand"  v-model="data.variacao_sd"  class="q-pr-sm" color="grey-7"/>
                  <q-input  :readonly="data.fase != '07'" v-if="data.tipo_mecanismo == '1'" label = "Un.Min. (V)" outlined stack-label lazy-rules="ondemand"   v-model="data.un_min"       class="q-pr-sm" color="grey-7"/>
                  <q-input  :readonly="data.fase != '07'" v-if="data.tipo_mecanismo == '1'" label = "Variação s/m" outlined stack-label lazy-rules="ondemand"  v-model="data.variacao_sm"  class="q-pr-sm" color="grey-7"/>
                  <q-input  :readonly="data.fase != '07'" v-if="data.tipo_mecanismo == '1'" label = "Consumo µA" outlined stack-label lazy-rules="ondemand"    v-model="data.consumo_ua"   class="q-pr-sm" color="grey-7"/>
                  <q-space/>
            <q-btn label="Tirar Fotos" icon="camera" color="green" @click="cameraModalOpen = true"></q-btn>
            </div>
            <div class = "row">
              <q-input :readonly="data.fase != '07'" outlined style="width: 250px;" class="q-mt-md column" v-if="[2,5,7].includes(data.tipo_reparo) && data.brand_id && ['CA','BA','MB','OP','PI','JC','VC','PA'].includes(data.brand_id)" v-model="data.contrato_richemont" label ="Valor contrato Richemont" bordered></q-input>
            <q-input :readonly="data.fase != '07'" v-model="data.text_qa" class="q-mt-md" style="max-width:30%" type="textarea" outlined label="Observações (histórico)"></q-input>
          <div class="q-pl-sm q-mt-md" v-if="data.brand_id && data.brand_id === 'TH'">
            <q-select :readonly="data.fase != '07'" outlined stack-label     :options="TiposGrupo.reparo_tag" v-model="data.repair_tag" label="Repair Type (TAG)" emit-value  map-options option-label="label" option-value="id" style ="min-width: 200px"/>
          <q-select :readonly="data.fase != '07'" outlined stack-label     :options="TiposGrupo.defeito_tag" v-model="data.defect_tag"  emit-value  map-options option-label="label" option-value="id" label="Defeito" class="q-mt-sm" style ="min-width: 200px"/>
          <q-select  :readonly="data.fase != '07'" v-if ="[2, 7,5].includes(data.tipo_reparo)" outlined stack-label    :options="TiposGrupo.warranty_tag" emit-value map-options  class="q-mt-sm" option-label="label" option-value="id" v-model="data.warranty_tag" label="Warranty code"  style ="min-width: 100px"/>
          <q-input :readonly="data.fase != '07'" v-if ="[2, 7].includes(data.tipo_reparo)" outlined stack-label  v-model="data.country_tag" label="País de venda" class="q-ml-md" style ="min-width: 100px"/>
          </div>
        <div v-if="data.brand_id && data.brand_id === 'BE'" class="q-ml-sm q-mt-md">
          <q-select :readonly="data.fase != '07'" outlined stack-label  :options="TiposGrupo.reparo_bre" v-model="data.repair_bre" label="Repair Type (BRE)" emit-value  map-options option-label="label" option-value="id" style ="min-width: 200px"/>
          <q-input  :readonly="data.fase != '07'" outlined stack-label   v-model="data.tracking_id_breitling"  emit-value  map-options option-label="label" option-value="id" class="q-mt-sm"  label="Tracking ID"  style ="min-width: 200px"/>
          <q-select  :readonly="data.fase != '07'" outlined stack-label   :options="TiposGrupo.defeito_bre" v-model="data.defect_bre"  emit-value  map-options option-label="label" option-value="id" label="Defeito" class="q-mt-sm" style ="min-width: 200px"/>
          <q-select :readonly="data.fase != '07'" v-if ="[2, 7].includes(data.tipo_reparo)" outlined stack-label    :options="TiposGrupo.pais_bre" emit-value map-options  option-label="label" option-value="id" v-model="data.pais_bre" label="País" class="q-mt-sm" style ="min-width: 100px"/>
          <q-input :readonly="data.fase != '07'" v-if ="[2, 7].includes(data.tipo_reparo)" outlined stack-label   v-model="data.ultimo_conserto_bre" label="último reparo" type="date" class="q-mt-sm" style ="min-width: 100px"/>
          </div>
        <div v-if="data.brand_id && data.brand_id === 'BV'" class="q-pl-sm q-mt-md">
          <q-input :readonly="data.fase != '07'" outlined stack-label   v-model="data.codigo_sap_bv"  emit-value  map-options option-label="label" option-value="id" label="Código SAP" style ="min-width: 270px"/>
          <q-select :readonly="data.fase != '07'" outlined stack-label   :options="TiposGrupo.v02_bv" v-model="data.codigo_v02_bv_1"  emit-value  map-options option-label="label" option-value="id" label="V02 - Código de Sintomas - Clientes" class="q-mt-sm" style ="min-width: 200px"/>
          <q-select :readonly="data.fase != '07'" outlined stack-label   :options="TiposGrupo.v01_bv" v-model="data.codigo_v01_bv_1" label="V01 - Código de Sintomas - Técnicos" emit-value  map-options option-label="label" option-value="id" class="q-mt-sm" style ="min-width: 200px"/>
          <q-select :readonly="data.fase != '07'" outlined stack-label   :options="TiposGrupo.v02_bv" v-model="data.codigo_v02_bv_2"  emit-value  map-options option-label="label" option-value="id" label="V02 - Código de Sintomas - Clientes" class="q-mt-sm" style ="min-width: 200px"/>
          <q-select :readonly="data.fase != '07'" outlined stack-label   :options="TiposGrupo.v01_bv" v-model="data.codigo_v01_bv_2" label="V01 - Código de Sintomas - Técnicos" emit-value  map-options option-label="label" option-value="id" class="q-mt-sm" style ="min-width: 200px"/>
        </div>
        <div class="column">
       <q-input type="date" @keydown.h="() => inserirDataAtual('data_liberado_entrega')" class="q-ml-md q-mt-md" v-model="data.data_liberado_entrega" bg-color="red-3" :readonly="data.fase !='07'" color="black" outlined label="Data Liberado"></q-input>
        <q-select :options="Status" v-model="data.status_finalizado" :readonly="data.fase !='07'" outlined class="q-ml-md q-mt-sm" emit-value map-options label ="Status"></q-select>
        </div>
      </div>
      
            <div>
              <div class="text-h6 q-mt-md">Devolução de peças não utilizadas</div>
              <q-table
                    style="max-width:100%"
                    flat bordered
                    ref="tableRef"
                    :rows="data.itens"
                    :columns="columns"
                    :pagination="{ rowsPerPage: 0 }"
                    row-key="referencia_produto"
                    hide-bottom

                  >
                    <template v-slot:body="props">
      <q-tr v-if="props.row.servico == 'P' && props.row.codigo_produto != '0000801' && props.row.quantidade >0" :props="props">
        <q-td>
          <q-btn icon="assignment_return" @click="devolverPeca(props.row.codigo_pecas_servicos,props.row.quantidade)" size="small" v-if="props.row.quantidade_retirada > 0"></q-btn>
          <q-tooltip v-if="props.row.quantidade_retirada > 0">Devolver Peça(s)</q-tooltip>
        </q-td>
        <q-td >
          <q-input :disable="(props.row.quantidade_a_retirar <= 0 && props.row.estoque <=0) || (props.row.quantidade_retirada >= props.row.quantidade)" filled style="width:100px" v-model.number="props.row.quantidade_a_retirar" default>
            <template v-if="props.row.quantidade <= props.row.quantidade_retirada" v-slot:append> <q-icon name="done" color="green" /></template>
            <template v-else="props.row.quantidade_a_retirar <= 0 && props.row.estoque <= 0" v-slot:append> <q-icon name="warning" color="primary" /></template></q-input>
            <q-tooltip v-if="props.row.quantidade_a_retirar <= 0 && props.row.estoque <= 0">Sem estoque</q-tooltip>
          </q-td>
        <q-td>
          {{ props.row.referencia_produto }}
        </q-td>
        <q-td>
          {{ props.row.quantidade }}

        </q-td>
        <q-td>
          {{ props.row.estoque }}

        </q-td>
        <q-td>
          {{ props.row.quantidade_retirada }}

        </q-td>
        <q-td>
          {{ props.row.descricao }}

        </q-td>
      </q-tr>
    
    </template>
                  </q-table>
            <div class="row">
              <q-btn class="q-my-lg" :disabled="!data.data_termino_conserto || data.data_termino_conserto.length < 8 || data.fase !='07'" label="Retornar para Conserto" color="red" icon="keyboard_return" @click="openEnviarOficina()"> </q-btn>
            <q-space/>
              <q-btn class="q-my-lg"  :disabled="!data.status_finalizado ||!data.data_liberado_entrega ||  data.data_liberado_entrega.length < 8 || data.fase !='07'" label="Liberar para entrega" color="green" icon="keyboard_tab" @click="enviarLE()"> </q-btn>
             
            </div>

            </div>
            </q-tab-panel>
            <q-tab-panel name=7>
              <div class="row justify-between q-mt-md q-mr-md q-ml-md">

                <div style="width:40%">
            <q-card class="q-mt-lg" bordered >
              
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
    <q-input outlined label="Total a Receber" style="width:30%" readonly v-model="data.valor_cliente"></q-input>
  </q-card-section>
  <q-card-section class="flex flex-center flex-column">
  <q-btn color="green" label="inserir" :loading="loadingFinanceiro" @click="inserirFinanceiro()" :disable="!data.forma_pagamento ||  !data.valor_sinal || data.valor_sinal== 0"/>
</q-card-section>
</q-card>
</div >
<div  style="width:30%" class="column q-mt-lg">


<q-btn icon="attach_email" @click="openEnviarEmail()" allign="left" label="e-mail de relógio pronto"></q-btn>
<q-btn icon="security_update_warning" allign="left" class="q-mt-sm" label="Whatsapp de relógio pronto"></q-btn>
<q-btn v-if="data.tipo_reparo !='9'" :disable="data.nf_devolucao" @click="fetchDadosDevolucao()" icon="local_shipping" allign="left" class="q-mt-sm btn-fixed-width" label="NF Devolução"> 
  <q-badge v-if="!data.nf_devolucao" floating icon="warning" color="red" ><q-icon name="warning" color="white" allign="left" /></q-badge>
  <q-badge v-else floating icon="done" color="green" ><q-icon name="done" color="white" allign="left" /></q-badge>
</q-btn>
<div class="row">
<q-btn v-if="data.tipo_reparo=='9' && !data.nf_venda || (data.tipo_pessoa=='F' && data.uf == data.loja) && data.valor_cliente !=0" icon="article" :disabled="data.valor_faltando >0" class="q-mt-sm" label="NF Produto" @click="gerarNFICMS = true" allign="left">
  <q-tooltip color="red" v-if="data.valor_faltando >0">Ainda existem valores à receber</q-tooltip>
</q-btn>

<q-chip v-if="!data.nf_venda && data.valor_cliente >0" square icon="error" class="q-mt-sm" color="red" text-color="white">Sem NF serviço/produto</q-chip>
<q-chip v-else square icon="done" class="q-mt-sm" color="green" text-color="white">NF produto / serviço emitida </q-chip>
<q-banner v-if="!data.nf_venda && data.valor_cliente >0 && data.uf != data.loja || data.tipo_pessoa== 'J' && !data.nf_venda && data.valor_cliente >0" class="bg-primary text-white" style="width:80%">
      Emitir a NF de serviço no estoklus e mandar sincronizar.
</q-banner>
<q-btn v-if="!data.nf_venda && data.valor_cliente >0 && data.uf != data.loja || data.tipo_pessoa== 'J' && !data.nf_venda && data.valor_cliente >0" @click="fetchDadosEntrega()" size="small" icon="sync"></q-btn>
</div>

</div>

<div class="q-mt-md" style="width:20%">
<div class="text-h6">Data de entrega</div>
                  <q-input @keydown.h="() => inserirDataAtual('data_entrega_produto')" :disable="!['6','3'].includes(data.status_os)" v-model="data.data_entrega_produto" outlined type="date"></q-input>
                  <q-input label="Observação (Entrega)" :disable="!['6','3'].includes(data.status_os)" v-model="data.observacao_entrega" class="q-mt-sm" outlined type="text"></q-input>
                  <q-input label="Código de rastreio" :disable="!['6','3'].includes(data.status_os)" v-model="data.codigo_rastreio_saida" class="q-mt-sm" outlined type="text"></q-input>
                  <q-select :options="Status" v-model="data.status_finalizado" :disable="!['6','3'].includes(data.status_os)" outlined class="q-mt-sm" emit-value map-options label ="Status"></q-select>
                  <q-btn class="q-mt-sm" label="Enviar notificação de envio" :disable="step != 7 || !data.codigo_rastreio_saida"></q-btn>
                </div>

                </div>

                <div class="row">
                <q-space/>
                  <q-btn class="q-my-lg" :disable="!['6','3'].includes(data.status_os) || data.valor_restante != 0 && data.status_os != '3' || !data.nf_venda  && (data.valor_cliente > 0 && data.status_os != '3') || !data.nf_devolucao && data.tipo_reparo != '9' || !data.data_entrega_produto || !data.status_finalizado" label="Entregar OS" color="green" icon="keyboard_tab" @click="EntregarOS()"> 
                    <q-tooltip v-if="(!data.nf_devolucao && data.tipo_reparo != '9')">Sem nf de devolução</q-tooltip>
                    <q-tooltip v-if="!data.nf_venda && data.valor_cliente > 0 ">Sem NF de  Produto ou Serviço </q-tooltip>
                    <q-tooltip v-if=" data.valor_restante != 0">OS com Valores à receber</q-tooltip>
                    
                  </q-btn>

                </div>


</q-tab-panel>

          </q-tab-panels>

        </q-card>
      </div>
    </div>
</q-card-section>
{{ data }}
</q-card>



<modal-dialog-mail
  v-model="showEnviarEmail"
  :imagesBase64="imagesBase64"
  :OS="data"
/>


<service-devolution
    v-model:showDevolution="showDevolution"
    v-model:cabecalho="data"
    v-model:itens="itens"
    persistent
    />


<modal-dialog
  :requireInput="true"
  v-model="enviarOficina"
  :message="`Texto do Histórico da OS`"
  @confirm="handleEnviarOficina"
  :text="`Subiu para oficina - Previsão de conclusão `"
/>

<modal-dialog
    title="Cancelar"
    v-model="gerarNFICMS"
    :message="`Tem certeza que deseja gerar a NF da OS ${data.codigo_estoklus}?`"
    @confirm="handleGerarNFICMS"
  />

<q-dialog v-model="cameraModalOpen" maximized>
          <q-card class="custom-dialog-size">
            <div class="title-style flex q-mt-md row items-center justify-center">{{ data.codigo_estoklus }}</div>
            <q-card-section>
              <div class="flex full-height row items-end justify-end q-mt-md">
    <q-btn color="grey" label="Fechar" @click="stopCameraAndCloseModal"></q-btn>
  </div>
          </q-card-section>
            <q-card-section >
            <camera-modal v-if="cameraModalOpen" :photoType="photoType" :data="data" @modalClosed="stopCameraAndCloseModal"></camera-modal>
            </q-card-section>

          

        </q-card>
</q-dialog>

</q-dialog>
  </template>


  
  <script setup>
  import { computed,ref,watch } from "vue";
  import { useQuasar } from "quasar";
  import OrdersServicesService from "../../services/Services";
  import { format } from "../../functions";
  import axios from "axios";
  import { Notify } from 'quasar';
  import ModalDialog from "../../components/modal-dialog.vue";
  import CameraModal from "../../components/CameraModal.vue";
  import ServiceDevolution from "./ServiceDevolution.vue";
  import ModalDialogMail from "../../components/modal-dialog-mail.vue";
  import AuthService from "../../services/AuthService";


  const currentUser = computed(() => AuthService.user);
  const imagesBase64 = ref([])
  const loading = ref(false)
  const showDevolution = ref(false)
  const gerarNFICMS = ref(false)
  const loadingFinanceiro = ref(false)
  const FormasPagamento = ref([])
  const pagamentosFiltered = ref([])
  const TiposGrupo = ref([]);
  const cameraModalOpen = ref(false)
  const product = ref([])
  const pesquisa = ref('')
  const tab = ref("1")
  const step = ref(1)
  const date = ref('21/11/2023')
  const props = defineProps([
    "OS","ShowServiceRepair"]);
  const emit = defineEmits(["confirm", "close", "update:dialog",]);
  const toogleRepair = ref(false)
  const motivosReprovacao = ref([])
  const estoklusUsers = ref([]);
  const UsersFiltered = ref([]);
  const dadosConserto = ref([]);
  const iconeCons =  ref('');
  const iconePol =  ref('');
  const iconePrep =  ref('');  
  const showEnviarEmail = ref(false);
  const data = ref([]);
  const enviarOficina=ref(false)
  const itens = ref([])
  const photoType= ref('')
  const columns = [{name: 'Actions', align: 'left', label: ' '},
    {name: 'Descrição', align: 'right', label: 'Quantidade à retirar'},
  { name: 'Referência', align: 'left', label: 'Referência', field: 'referencia_produto', sortable: true },
{name: 'Quantidade', align: 'left', label: 'Quantidade', field: 'quantidade', sortable: true},
{name: 'Estoque', align: 'left', label: 'Estoque', field: 'estoque', sortable: true},
{name: 'Quantidade Baixada', align: 'left', label: 'Baixado', field: 'quantidade_retirada', sortable: true},
{name: 'Descrição', align: 'left', label: 'Descrição', field: 'descricao', sortable: true},
]

const TiposMovimento = ref([
{ value: "1", label: 'Quartz' },
{ value: "2", label: 'Automático' },
{ value: "3", label: 'Corda Manual' }
]);

const TiposComplicação = ref([
{ value: 1, label: 'Três Ponteiros' },
{ value: 2, label: 'Cronógrafo' },
]);

const Status = ref([{value:"20",label:"Conserto Total"},
{value:"33",label:"CP - Manutenção"},
{value:"32",label:"CP - Troca de Bateria"},
{value:"30",label:"Troca de Bateria Simples"},
{value:"36",label:"Troca de Relógio"},
{value:"42",label:"CP - Sem Garantia"},
{value:"38",label:"Em transito - outra unidade"},
])
const TiposdeReparo = ref([
    { id: "1", label: 'Fora de Garantia' },
    { id: "2", label: 'Garantia de Venda' },
    { id: "3", label: 'Garantia de Serviço' },
    { id: "4", label: 'Análise Garantia' },
    { id: "5", label: 'Estoque' },
    { id: "6", label: 'Cortesia' },
    { id: "7", label: 'Garantia Internacional' },
    { id: "8", label: 'Garantia de 3s' },
    { id: "9", label: 'Acessórios' }
]);
  const editando = ref({
    "iprep":false,
    "fprep":false,
    "ipol":false,
    "fpol":false,
    "iser":false,
    "fser":false,
  })
  const inserirDataAtual = (inputRef) => {
    
    const hoje = new Date();
  const dataFormatada = `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}-${String(hoje.getDate()).padStart(2, '0')}`;
  data.value[inputRef] = dataFormatada;
  }
  const showRepair = computed({
  get: () => {
   
    if(props.ShowServiceRepair == true){
      
        loadEstoklusUsers();  
        if (data.value.fase == '05'){
      tab.value = '1'
      step.value = 1
    }
    else if(data.value.fase == '10'){
     
      tab.value = '2'
      step.value= 2
    }
    else if(data.value.fase == '10'){
     
     tab.value = '2'
     step.value= 2
   }
    else if(data.value.status_os == '5'){
        if(data.value.fase == '40'){
          tab.value = '3'
          step.value =3
        }else if(data.value.fase == '41'){
          tab.value = '4'
          step.value= 4
        }else if(data.value.fase == '06'){
          tab.value = '5'
          step.value= 5
        }else if(data.value.fase == '07'){
          tab.value = '6'
          step.value= 6
        }

    }
    else if(['6','7','3','8'].includes(data.value.status_os)){
      tab.value = '7'
      step.value = 7
      fetchFinanceiro();
      fetchPagamentos();
      fetchDadosEntrega();

    }
  }
    
  } ,set: (value) => {

  },
  
});

watch(
            () => cameraModalOpen.value,
            (newValue) => 
            {
                if (!newValue) {
                  emit('modalClosed');
                }
            }
        );

const stopCameraAndCloseModal = () => {
            cameraModalOpen.value = false;
        };

    const openCamera = (type) => {
      data.value = type.row;
      photoType.value = type;
      cameraModalOpen.value = true;
    };

function edita(param) {
    editando.value[param]= true
}function salvar(param) {
    editando.value[param]= false
}function avanca() {
    if (data.value.tipo_reparo == '9'){
        tab.value = '7'
      }
     else{

    
    tab.value = Number(tab.value) + 1;
    tab.value = tab.value.toString();
  }

}function retorna(param) {
  if (data.value.tipo_reparo == '9'){
        tab.value = '1'
      }
     else{
    tab.value = Number(tab.value) - 1;
    tab.value = tab.value.toString();
     }
}


const formatDate = (dateInput) => {
  if (!dateInput) return null;

  // Tenta criar um objeto Date a partir do input.
  // Assumimos que o input é uma string ou um timestamp.
  const date = new Date(dateInput);

  // Verifica se a data é válida
  if (isNaN(date.getTime())) {
    return "Data inválida";
  }

  const [year, month, day] = [date.getFullYear(), date.getMonth() + 1, date.getDate()+1];

  // Retorna a data formatada como DD/MM/YYYY
  return `${day.toString().padStart(2, '0')}/${month.toString().padStart(2, '0')}/${year}`;
};

const handleGerarNFICMS = async (val, update) => {
  try {
      data.value.id = `${data.value.loja}${data.value.codigo_estoklus}`
      const response = await axios.post(
        `https://app.watchtime.com.br/api/estoklus/nf_icms`,data.value
      );      
      if(response.data.success != undefined){
        Notify.create({
              type: 'positive',
              message: `NF ${response.data.success} gerada no Estoklus`
            });
            data.value.nf_venda = true

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
async function loadEstoklusUsers() {
  const response = await OrdersServicesService.getUsersEstoklus();


  estoklusUsers.value = response?.map((b) => {
    return { label: `${b.label.toUpperCase()} - ${b.id}`, value: b.id };
  });

}
  async function confirm() {
      emit("confirm");
    }
  
  
  function close() {
    emit("close");
    
  }

  async function removerPeca(value){
    const response = await axios.post(
        `https://app.watchtime.com.br/api/estoklus/exclui_peca/${value}`
      );
      if (response.data == 'OK'){

      
Notify.create({
        type: 'warning',
        message: `Produto removido com sucesso`
      });
    }


      reloadOS()

  }
  async function devolverPeca(value,qty){

    const response = await axios.post(
        `https://app.watchtime.com.br/api/estoklus/devolve_peca`,{"item": {"codigo_pecas_servicos": value,"quantidade": qty}}
      );
      if (response.data == 'OK'){

      
Notify.create({
        type: 'warning',
        message: `Produto removido com sucesso`
      });
    }


      reloadOS()

  }
  async function desativarPeca(value){
    const response = await axios.post(
        `https://app.watchtime.com.br/api/estoklus/desativa_peca/${value}`
      );
      if (response.data == 'OK'){

      
Notify.create({
        type: 'warning',
        message: `Produto desativado com sucesso`
      });
    }
      reloadOS()
}  

  async function inserePeca(){
    console.log(product.value)
    let request ={
      "item": {"id":product.value.id,"label":product.value.label,"referencia":product.value.referencia,"quantidade":product.value.quantidade,"preco_venda": 0},
      "loja": data.value.loja
    }

    try {
      const response = await axios.post(
        `https://app.watchtime.com.br/api/estoklus/peca_extra/${data.value.codigo_estoklus}`,request 
      );

      if (response.data == 'OK'){

      
      Notify.create({
              type: 'negative',
              message: `Produto inserido com sucesso`
            });
          }
      reloadOS()
}
catch{

}}

function openEnviarOficina() {
  enviarOficina.value=true;
}

async function reloadOS(){
  try{
  const  responseData = await axios.get(
`https://app.watchtime.com.br/api/estoklus/get_os_completa/`+data.value.codigo_estoklus
) 
data.value = responseData.data


data.value.itens.forEach(item => {
// Calcula a quantidade a retirar somente se tiver estoque disponível
if (item.estoque > 0) {
item.quantidade_a_retirar = item.quantidade - item.quantidade_retirada;
}else if(item.estoque < item.quantidade){
item.quantidade_a_retirar = item.estoque
} else {
item.quantidade_a_retirar = 0; // Define como 0 se não houver estoque
}
});
  }catch{

  }
}


async function baixaPecas(){
  const items = {items: data.value.itens.filter((item) => item.quantidade_a_retirar > 0)}
  if (items == []){
    Notify.create({
              type: 'negative',
              message: `Nenhum produto para baixar`
            });
  } else{
    const response = await axios.post(`https://app.watchtime.com.br/api/estoklus/baixa_pecas_os`,items)
    console.log(response)
  }
  reloadOS()
}
  
  async function consultaPeca(referencia){
    try {
      const response = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/pecas`, 
        {
          params: {referencia: referencia.toUpperCase()},
        }
      );
      if(response.data[0] == undefined){
        Notify.create({
              type: 'negative',
              message: `Produto ${referencia.toUpperCase()}, inexistente ou não cadastrado no estoklus`
            });

            product.value = []
          }
        else{
          product.value.id = response.data[0].id
          product.value.label = response.data[0].label
          product.value.referencia = response.data[0].referencia
          product.value.quantidade = 1
          
        }
       
        
  }
  catch{

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
const openEnviarEmail = async () => {
  let dado = await getCustomerData(data.value.cliente_id,'EMAIL')
  if(dado == ''){
    Notify.create({
              type: 'negative',
              message: `E-mail em branco`
            });
  }

  else {
    const dataOs = data.value.data_os;
    
let partesData = dataOs.split('/');
if(partesData.length !=3){
  partesData = dataOs.split('-');
}

const ano = partesData[2]; // Assume que a data está no formato DD/MM/AAAA
const mes = partesData[1]; // Mesmo aqui, assume-se que a data está no formato DD/MM/AAAA
    const dataToSubmit = {
  "codigo_estoklus": data.value.codigo_estoklus,
  "ano": parseInt(ano, 10),
  "mes": parseInt(mes, 10)
};
    const response = await axios.post(
      `https://app.watchtime.com.br/api/mail/listar_fotos`,
      dataToSubmit
    );
    data.value.texto_email = '' 
    imagesBase64.value = response.data
    data.value.status = data.value.status_os
    if(data.value.status_os == '6'){
      data.value.titulo_email = `Ordem de serviço Liberada para Entrega - ${data.value.codigo_estoklus}${data.value.brand_id} `
      data.value.texto_email = `Olá, ${data.value.nome}!

Este e-mail foi enviado para documentar que sua ordem de serviço de número ${data.value.codigo_estoklus}${data.value.brand_id} está pronta para entrega.


Qualquer dúvida, estamos a disposição!

Atenciosamente,

${currentUser.value.name}
`   

    
  }
}
showEnviarEmail.value = true
}




const handleEnviarOficina = async (value) => {
  try {
    
    data.value.texto_laboratorio = value
    data.value.sistema = 'NOVO'
      const response = await axios.post(`https://app.watchtime.com.br/api/estoklus/liberado_execucao`,data.value)
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
              message: `Erro ao atualizar OS`
            });
    }
    reloadOS()
  };


  async function liberarOSAcessorio(){

    try{
    const response = await axios.post(`https://app.watchtime.com.br/api/estoklus/libera_acessorio/${data.value.codigo_estoklus}`)
      if(response.data == 'OK'){
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
              message: `Erro ao atualizar OS`
            });
    }
    reloadOS()
  }

  watch(tab, async (newStep) => {
    if (newStep == '6'){
      const response = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/cx/${data.value.codigo_estoklus}`
      );
      if (response){
        data.value.contrato_richemont = response.data[0].contrato_richemont
        data.value.repair_tag = response.data[0].repair_tag
        data.value.defect_tag = response.data[0].defect_tag
        data.value.warranty_tag = response.data[0].warranty_tag
        data.value.country_tag = response.data[0].country_tag
        data.value.repair_bre = response.data[0].repair_bre
        data.value.tracking_id_breitling = response.data[0].tracking_id_breitling
        data.value.defect_bre = response.data[0].defect_bre
        data.value.ultimo_conserto_bre = response.data[0].ultimo_conserto_bre
        data.value.pais_bre = response.data[0].pais_bre
        data.value.codigo_v02_bv = response.data[0].codigo_v02_bv
        data.value.codigo_v01_bv = response.data[0].codigo_v01_bv
        data.value.codigo_sap_bv = response.data[0].codigo_sap_bv
      }
    }
  if (newStep === '6' && data.value.brand_id === 'TH' && !TiposGrupo.value.defeito_tag) {
    try {
      TiposGrupo.value.defeito_tag = await fetchGrupos('AB');
      TiposGrupo.value.reparo_tag = await fetchGrupos('TU');
      TiposGrupo.value.warranty_tag = await fetchGrupos('WX');
      
    } catch (error) {
    }
  }
    else if (newStep === '6' && data.value.brand_id === 'BE' && !TiposGrupo.value.defeito_bre) {
    try {
      TiposGrupo.value.defeito_bre = await fetchGrupos('B04');
      TiposGrupo.value.reparo_bre = await fetchGrupos('B01');
      TiposGrupo.value.reparo_bre = TiposGrupo.value.reparo_bre.map(item => ({
        id: item.id,
        label: item.id + ' - ' + item.label}));

      TiposGrupo.value.pais_bre = await fetchGrupos('B05');
      
    } catch (error) {
    }
  }    else if (newStep === '6' && data.value.brand_id === 'BV' && !TiposGrupo.value.v01_bv) {
    try {
      TiposGrupo.value.v01_bv = await fetchGrupos('V01');
      TiposGrupo.value.v02_bv = await fetchGrupos('V02');
    } catch (error) {
    }
  }
  else if (newStep === '7') {
    try {
      fetchFinanceiro();
      fetchPagamentos();
      fetchDadosEntrega();
    } catch (error) {
    }
  }
  

});
watch(
            () => props.ShowServiceRepair,
            (newValue) => 
            { 
              console.log(newValue)
                if (newValue) {
                  data.value = props.OS
                  data.value.polimento = true
                }
            }
        );

watch(showDevolution, (newStatus) => {
  console.log(newStatus)

  if (newStatus == false){
  
    fetchDadosEntrega()
  }
})


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

async function fetchDadosEntrega(){
  try {
    const response = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/dados_entrega/${data.value.codigo_estoklus}`, 
      );
      
      if (response.data.nf_devolucao == 'false'){
        data.value.nf_devolucao = false
      } else {
        data.value.nf_devolucao = true
      }
      
      if(response.data.nf_produto == 'true' || response.data.nf_servico == 'true' || ['047685','206620','210129','S042591','043471','F00001','062560','208516'].includes(data.value.cliente_id)){
        data.value.nf_venda = true
      }else{
        response.data.nf_venda = false
      }
      if(response.data.nf_entrada == 'false' && data.value.nf_entrada == ''){
        data.value.nf_devolucao = true
      }
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
        data.value.valor_cliente = response.data[0].valor_receber
        data.value.valor_receber = response.data[0].valor_receber
  
  
  }
  catch{

  }
}


  async function enviarQA(){
    try {

      step.value = 6
      data.fase = '07'
      tab.value = '6'
      const responseQA = await axios.post(`https://app.watchtime.com.br/api/estoklus/fluxo_conserto/qa`,data.value);
      await reloadOS()
      if (data.value.brand_id === 'TH') {
    try {
      TiposGrupo.value.defeito_tag = await fetchGrupos('AB');
      TiposGrupo.value.reparo_tag = await fetchGrupos('TU');
      TiposGrupo.value.warranty_tag = await fetchGrupos('WX');
      
    } catch (error) {
    }
  }
    else if (data.value.brand_id === 'BE') {
    try {
      TiposGrupo.value.defeito_bre = await fetchGrupos('B04');
      TiposGrupo.value.reparo_bre = await fetchGrupos('B01');
      TiposGrupo.value.reparo_bre = TiposGrupo.value.reparo_bre.map(item => ({
        id: item.id,
        label: item.id + ' - ' + item.label}));

      TiposGrupo.value.pais_bre = await fetchGrupos('B05');
      
    } catch (error) {
    }
  }    else if (data.value.brand_id === 'BV') {
    try {
      TiposGrupo.value.v01_bv = await fetchGrupos('V01');
      TiposGrupo.value.v02_bv = await fetchGrupos('V02');
    } catch (error) {
    }
  }
  const response = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/cx/${data.value.codigo_estoklus}`
      );
      if (response){
        data.value.contrato_richemont = response.data[0].contrato_richemont
        data.value.repair_tag = response.data[0].repair_tag
        data.value.defect_tag = response.data[0].defect_tag
        data.value.warranty_tag = response.data[0].warranty_tag
        data.value.country_tag = response.data[0].country_tag
        data.value.repair_bre = response.data[0].repair_bre
        data.value.tracking_id_breitling = response.data[0].tracking_id_breitling
        data.value.defect_bre = response.data[0].defect_bre
        data.value.ultimo_conserto_bre = response.data[0].ultimo_conserto_bre
        data.value.pais_bre = response.data[0].pais_bre
        data.value.codigo_v02_bv = response.data[0].codigo_v02_bv
        data.value.codigo_v01_bv = response.data[0].codigo_v01_bv
        data.value.codigo_sap_bv = response.data[0].codigo_sap_bv
      }
      
    } catch (error) {
      Notify.create({
      type: 'negative',
      message: `Erro ao atualizar a OS`
    });
    }


  }

  async function enviarPolimento(){
    try {
      
      step.value=4
      tab.value='4'
      data.fase = 5
      const response = await axios.post(`https://app.watchtime.com.br/api/estoklus/fluxo_conserto/pol`,data.value);
     await reloadOS()
      

      
    } catch (error) {
      Notify.create({
      type: 'negative',
      message: `Erro ao atualizar a OS`
    })
    }


  }
  async function enviarConserto(){
    try {
      step.value=5
      tab.value='5'
      data.fase = 5
      const response = await axios.post(`https://app.watchtime.com.br/api/estoklus/fluxo_conserto/conserto`,data.value);
      await reloadOS()
      
      
    } catch (error) {
      Notify.create({
      type: 'negative',
      message: `Erro ao atualizar a OS`
    })
    }


  }
  async function enviarLE(){
    try {

      step.value = 7
      data.status = '06'
      tab.value='7'
      const response = await axios.post(`https://app.watchtime.com.br/api/estoklus/fluxo_conserto/le`,data.value);
      await reloadOS()
      
    } catch (error) {
      Notify.create({
      type: 'negative',
      message: `Erro ao atualizar a OS`
    })
    }


  }
  async function EntregarOS(){
    try {

      step.value = 8
      const response = await axios.post(`https://app.watchtime.com.br/api/estoklus/fluxo_conserto/entregue`,data.value);
      await reloadOS()
    } catch (error) {
      Notify.create({
      type: 'negative',
      message: `Erro ao atualizar a OS`
    })
    }


  }
  async function enviarPreparacao(){
    try {

      const response = await axios.post(`https://app.watchtime.com.br/api/estoklus/fluxo_conserto/prep`,data.value);
            step.value = 3
      data.status = '06'
      tab.value='3'
      
      
    } catch (error) {
      Notify.create({
      type: 'negative',
      message: `Erro ao atualizar a OS`
    })
    }

    await reloadOS()
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
            data.value.id = `${data.value.loja}${data.value.codigo_estoklus}`
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

  const fetchDadosDevolucao = async (val, update) => {
  loading.value = true;
  data.value.id = `${data.value.loja}${data.value.codigo_estoklus}`

  try {
      const response = await axios.get(
        `https://app.watchtime.com.br/api/estoklus/nf_saida/`+data.value.cliente_id
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
  showDevolution.value = true

};


  
  </script>
  <style>
  .custom-captions {
    text-align: center;
    margin-top: 20px; /* Ajuste conforme necessário */
  }
  
  .caption {
    margin-bottom: 5px; /* Espaço entre as legendas */
    /* Estilize conforme necessário */
  }
  </style>