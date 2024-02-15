<template>
  <q-dialog v-model="toggleDialog">
    <q-card class="wt-border q-pa-md" style="min-width:70%">
      <q-card-section class="row items-center q-pa-none">
        <div class="title-style q-pa-none">{{ title }}</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>

      <q-card-section class="q-px-none"> {{ message }} </q-card-section>

      <q-card-section v-if="copiar_todos" class="q-mt-md" > 
        <q-option-group
          v-model="todos"
          :options="geral"
          color="primary"
          inline
          dense
          style="align-self:center"
        />

  <div class="q-pa-md">
    <q-table
      style="height: 400px"
      flat bordered
      ref="tableRef"
      title="Itens"
      :rows="itens"
      :columns="columns"
      :table-colspan="9"
      row-key="index"
      virtual-scroll
      :virtual-scroll-item-size="48"
      :pagination="pagination"
      :rows-per-page-options="[0]"
      :filter="filter"
    >
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

          <q-th
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props" :key="`m_${itens.referencia}`">
          <q-td>
            <q-option-group
          v-model="props.row.tipo"
          :options="options_todos"
          color="primary"
          inline
          dense
        />
          </q-td>

          <q-td
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.value }}
          </q-td>
        </q-tr>
      </template>

    </q-table>
  </div>


       
        
      
        <div>Itens: {{itens }}</div> 
      
      </q-card-section>

      <q-card-actions align="right" class="q-pa-none q-mt-sm">
        <q-btn
          flat
          :label="cancelText ? cancelText : `Cancelar`"
          color="grey"
          v-close-popup
          @click="close"
          class="wt-border"
        />
        <q-btn
          unelevated
          :label="confirmationText ? confirmationText : `Confirmar`"
          color="secondary"
          @click="confirm"
          v-close-popup
          class="wt-border"
        />
      </q-card-actions>
    </q-card>
   
  </q-dialog>
 
</template>

<script setup>
import { computed, ref, watch } from "vue";
const props = defineProps([
  "title",
  "confirmationText",
  "dialog",
  "cancelText",
  "message",
  "copiar_todos",
  "itens"
]);
const selected = ref([])
const       pagination = {
        rowsPerPage: 0
      }
const columns = [{ name: 'Referência', align: 'left', label: 'Referência', field: 'referencia', sortable: true },
{name: 'Descrição', align: 'left', label: 'Descrição', field: 'nome', sortable: true}]

const  filter = ref('')

const todos = ref('op1')
const options_todos = [
        {
          label: 'OB',
          value: 'OB',
          color: 'grey-7'
        },
        {
          label: 'OP',
          value: 'OP',
          color: 'grey-9'
        },
        {
          label: 'I',
          value: 'I',
          color: 'grey-8'
        },
        {
          label: '-',
          value: '-',
          color: 'red'
        }
      ];
      const geral = [
      {
          label: 'Obrigatórios',
          value: 'OB',
          color: 'grey-7'
        },
        {
          label: 'Opcionais',
          value: 'OP',
          color: 'grey-9'
        },
        {
          label: 'Incuídos no serviço',
          value: 'I',
          color: 'grey-8'
        }
      ];
const emit = defineEmits(["confirm", "close", "update:dialog","valores"]);

const toggleDialog = computed({
  get() {
    return props.toggleDialog;
  },
  set(value) {
    emit("update:dialog", value);
  },
});

function       getSelectedString () {
        return selected.value.length === 0 ? '' : `${selected.value.length} record${selected.value.length > 1 ? 's' : ''} selected of ${props.itens.length}`
      }

async function confirm() {
  emit("confirm");
}

function close() {
  emit("close");
}


watch(() => todos.value, (newValue) => {
  for (let item of props.itens) {
      console.log((item))
      item.tipo = todos.value
      }
  console.log(todos.value)

});
</script>
