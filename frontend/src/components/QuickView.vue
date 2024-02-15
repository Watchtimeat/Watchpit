<template>
    <q-dialog v-model="toggleDialog">
      <q-card style="min-width:70%">
        <q-card-section class="row items-center q-pa-none">
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
  
        <q-card-section> 
  
    <div >
      <q-table
        style="max-height: 500px"
        flat bordered
        ref="tableRef"
        title="Quick View"
        :rows="itens"
        :columns="columns"
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
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
            >
            <template v-if="col && col.type == 'date'">
  {{ formatDate(col.value) }}
</template>
<template v-else-if="col">
  {{ col.value }}
</template>
            </q-td>
          </q-tr>
        </template>
  
      </q-table>
    </div>
  
  
         
          
        
      
        
        </q-card-section>
  
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
  const columns = [{ name: 'Marca', align: 'left', label: 'Marca', field: 'marca', sortable: true },
                    {name: 'Modelo', align: 'center', label: 'Modelo', field: 'modelo', sortable: true},
                    {name: 'Série', align: 'center', label: 'Série', field: 'serie', sortable: true },
                    {name: 'Data Entrega', type: 'date',align: 'center', label: 'Data Entrega', field: 'data_entrega', sortable: true },
                    {name: 'Valor', align: 'center', label: 'Valor', field: 'valor', sortable: true },
                    {name: 'Unidade', align: 'center', label: 'Loja', field: 'unidade', sortable: true },
                    {name: 'Serviço', align: 'center', label: 'Tipo de Serviço', field: 'tipo_servico', sortable: true },
                    {name: 'OS', align: 'center', label: 'OS', field: 'id', sortable: true }]
  
  const  filter = ref('')
  

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
  
  const formatDate = (dateInput) => {
  // Verifica se a entrada já está no formato DD/MM/YYYY
  const regex = /^\d{2}\/\d{2}\/\d{4}$/;
  if (regex.test(dateInput)) {
    return dateInput;
  }

  if (!dateInput) return null;

  // Tenta criar um objeto Date a partir do input
  const date = new Date(dateInput);

  // Verifica se a data é válida
  if (isNaN(date.getTime())) {
    return "Data inválida";
  }

  const [year, month, day] = [date.getFullYear(), date.getMonth() + 1, date.getDate()];

  // Retorna a data formatada como DD/MM/YYYY
  return `${day.toString().padStart(2, '0')}/${month.toString().padStart(2, '0')}/${year}`;
};
  
    </script>
  