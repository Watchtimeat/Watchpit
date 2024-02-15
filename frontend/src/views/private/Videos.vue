<template>
    <q-card class="wt-border q-pa-md" style="min-width:70%">
  
      <q-card-section class="row items-center q-pa-none">
  
        <div class="title-style q-pa-none">{{ title }}</div>
  
        <q-space />
  
        <q-btn icon="close" flat round dense v-close-popup />
  
      </q-card-section>
  
      <div class="q-pa-md">
  
        <q-table style="height: 400px" flat ref="tableRef" title="Suporte:" :rows="itens" :columns="columns"
          :table-colspan="9" row-key="index" virtual-scroll :virtual-scroll-item-size="48" :pagination="pagination"
          :rows-per-page-options="[0]" :filter="filter">
  
          <template v-slot:top-right>
  
            <q-input background="blue" dense debounce="300" v-model="filter" placeholder="Pesquisa">
  
              <template v-slot:append>
  
                <q-icon name="search" />
  
              </template>
  
            </q-input>
  
          </template>
  
          <template v-slot:header="props">
  
            <q-tr :props="props">
  
              <q-th />
  
              <q-th v-for="col in props.cols" :key="col.name" :props="props">
  
                {{ col.label }}
  
              </q-th>
  
            </q-tr>
  
          </template>
  
          <template v-slot:body="props">
  
            <q-tr :props="props" :key="`m_${itens.referencia}`">
  
              <q-td>
  
                <q-btn unelevated label="Assistir" color="secondary" @click="confirm(props.row)" v-close-popup
                  class="wt-border" />
  
              </q-td>
  
              <q-td v-for="col in props.cols" :key="col.name" :props="props">
  
                {{ col.value }}
  
              </q-td>
              
  
            </q-tr>
            
  
          </template>
  
        </q-table>
  
      </div>
  
    </q-card>
  
     <VideoModal v-if="ModalVideoVisible" :data="url" v-model="ModalVideoVisible" />
  </template>
  
  <script setup>
  
  import { computed, ref, watch } from "vue";
  
  import VideoModal from '../../types/VideoModal.vue';
  
  //PAGINAÇÃO
  
  const pagination = {
  
    rowsPerPage: 0
  
  }
  
  //COLUNAS DA TABELA
  
  const columns = [{ name: 'Nome do Vídeo', align: 'left', label: 'Nome', field: 'nome', sortable: true },
  
  { name: 'Tipo', align: 'left', label: 'Tipo', field: 'tipo', sortable: true }]
  
  //ITENS DA TABELA
  
  const itens = ref([{ "id": "https://watchtimepr.cddyndns.com:8888/index.php/s/QMXWraK6To4mD2n/download", "nome": "ABERTURA DE OS", "tipo": "OS", "descricao": "" },
  
  { "id": "watchtime.com.br", "nome": "Fechamento DE OS", "tipo": "OS" }])
  
  //PADRÃO
  
  const filter = ref('')
  
  const url = ref('')
  
  //VARIAVEL QUE ABRE O MODAL
  
  const ModalVideoVisible = ref(false)
  
  async function confirm(video) {
    console.log(video);
    url.value = video.id;
  
    // Set up the error message
    const errorMessage = {
      id: video.id,
      nome: video.nome,
      tipo: video.tipo,
      descricao: video.descricao,
    };
  
    // Show the ErrorDialog
    ModalVideoVisible.value = true;
    url.value = errorMessage;
  }
  
  </script>
  