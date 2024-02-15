<template>
  <q-dialog v-model="toggleDialog">
    <q-card style="width: 500px; max-width: 80vw" class="wt-border q-pa-md">
      <q-card-section class="row items-center q-pa-none">
        <div class="title-style q-pa-none">Reprovação</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>

      <q-card-section class="q-px-none"> Tem certeza que deseja reprovar a OS {{ props.os.codigo_estoklus }}?</q-card-section>


      <q-card-section  class="q-px-none">
        <q-select outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" :options="motivosReprovacao" v-model="props.os.motivo_reprovacao" label="Motivo da Reprovação" emit-value  map-options option-label="label" option-value="id" class="q-mt-md" style ="min-width: 200px"/>
          <q-select v-if="props.os.brand_id == 'BE'" outlined stack-label :rules="[val => !!val || 'Campo obrigatório']" :options="repairBreitling" v-model="props.os.repair_bre" label="Campo Breitling" emit-value  map-options option-label="label" option-value="id" class="q-mt-md" style ="min-width: 200px"/>
        </q-card-section>
      <div class="title-style q-pa-none">Histórico da OS</div>
      <q-card-section  class="q-px-none">
      <q-input v-model="props.os.titulo_historico" label="Título" class="q-mt-md" outlined placeholder="Digite o título aqui..." />
        <q-input v-model="props.os.texto_historico" label="Texto" class="q-mt-md"  outlined placeholder="Digite o texto aqui..." />
      </q-card-section>
      <q-card-actions align="right" class="q-pa-none q-mt-sm">
        <q-btn
          flat
          :label="`Cancelar`"
          color="grey"
          v-close-popup
          @click="close"
          class="wt-border"
        />
        <q-btn
          unelevated
          :label="`Confirmar`"
          color="secondary"
          @click="confirm"
          v-close-popup
          class="wt-border"
          :disabled="!props.os.texto_historico || !props.os.titulo_historico || !props.os.motivo_reprovacao"
        />
      </q-card-actions>
    </q-card>
    {{ props.os }}
  </q-dialog>
</template>

<script setup>
import { computed,ref } from "vue";
import OrdersServicesService from "../services/Services";
const userTitle = ref('Reprovado')
const userText =  ref('')
const props = defineProps([
  "os"]);
const emit = defineEmits(["confirm", "close", "update:dialog",]);

const motivosReprovacao = ref([])
const repairBreitling = ref([])


const toggleDialog = computed({
  get() {

    fetchGrupos('MR')
    fetchGrupos('B01')

    return props.toggleDialog;
  },
  set(value) {

    emit("update:dialog", value);
  },
});

async function confirm() {
    emit("confirm");
  }


function close() {
  emit("close");
  
}

const fetchGrupos = async (tipo) => {
  try {
    
      
    const response = await OrdersServicesService.getGrupos(tipo)
    if (tipo =='MR'){
    motivosReprovacao.value = response?.map(item => ({
        id: item.id,
        label: item.label
      }))}
    else {
      repairBreitling.value = response?.map(item => ({
        id: item.id,
        label: item.label
      }))
    }
    
    }
   catch (err) {
    console.error("Erro ao buscar dados:", err);
  }
}


</script>
