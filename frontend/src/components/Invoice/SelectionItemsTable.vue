<template>
  <div>
    <q-table
      flat
      bordered
      ref="tableRef"
      :rows="itemsList"
      :columns="propColumns"
      class="wt-border no-shadow"
      row-key="id"
      :selection="selection"
      v-model:selected="itemsSelectedComputed"
      :rows-per-page-options="[10, 25, 50]"
      :pagination="pagination"
      :filter="filter"
      dense
    >
    <template v-slot:top>
      <q-input
            v-model="filter"
            dense
            outlined
            stack-label
            color="grey-7"
            type="search"
            label="Código ou nome"
            debounce="300"
            class="q-pr-md wt-border"
          >
          
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
    </template>
      <template v-slot:body-cell="props">
        <q-td :props="props">
          <template v-if="props.col.type === 'actions'">
            <q-btn
              flat
              round
              padding="xs"
              size="sm"
              v-for="action in props.col.action"
              :key="action.icon"
              :icon="action.icon"
              :color="action.color"
              @click="action.action(props)"
            />
          </template>
          <template v-if="props.col.type === 'info'">
            <q-icon name="info" color="grey" size="18px" />
            <q-tooltip>
              <div v-if="props.row[props.col.field]">
                <div
                  v-for="(item, index) of props.row[props.col.field]"
                  :key="index"
                >
                  - {{ item.code }}
                </div>
              </div>
              <div v-else>Nenhuma OS relacionada</div>
            </q-tooltip>
          </template>
          <template v-if="props.col.type === 'currency'">
            {{ format(props.row[props.col.field], "currency") }}
          </template>
          <template
            v-if="!['currency', 'actions', 'info'].includes(props.col.type)"
          >
            {{ props.row[props.col.field] }}
          </template>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<script>
import { computed,ref } from "vue";
import { format } from "@/functions";

export default {
  props: ["itemsList", "selection", "itemsSelected", "columns", "pagination"],
  emits: ["update:itemsSelected"],

  setup(props, { emit }) {
    const propColumns = props.columns;
    const  filter = ref('')
    const itemsSelectedComputed = computed({
      get() {
        return props.itemsSelected;
      },
      set(newValue) {
        emit("update:itemsSelected", newValue);
      },
    })


    return {
      propColumns,
      itemsSelectedComputed,
      format,
      filter,
    };
  },
};
</script>
