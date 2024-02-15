<template>
  <q-table
    ref="tableRef"
    virtual-scroll
    no-data-label="Não há dados disponíveis"
    row-key="id"
    :rows="rows"
    :columns="columns"
    :loading="loading"
    v-model:pagination="_pagination"
    @request="request"
    :rows-per-page-options="[10, 25, 50]"
    :dense="dense"
  >
    <template v-slot:top>
      <slot name="top"></slot>
      <div class="total-value row items-center justify-end" v-if="totalCost">
    <div class="text-caption q-pr-md">Valor total dos pedidos:</div>
    <div class="text-caption">{{ format(totalCost,"number")}}</div>
    </div>
    </template>
    <template v-slot:header="props">
      <q-tr :props="props">
        <q-th v-for="col in props.cols" :key="col.name" :props="props">
          <span class="text-weight-medium">
            {{ col.label }}
          </span>
        </q-th>
      </q-tr>
    </template>
    <template v-slot:body-cell="props">
      <q-td :props="props">
        <template v-if="props.col.type == 'actions'">
          <template v-for="(action, index) in props.col.actions" :key="index">
            <q-btn
              flat
              round
              padding="xs"
              size="sm"
              :color="action.color"
              :icon="
                action.icon
                  ? action.icon
                  : handleIcon(
                      props.col.options.find(
                        (o) => o.value == props.row[props.col.field]
                      )?.value
                    )
              "
              @click="action.action(props)"
            >
              <q-tooltip>{{ action.toolTip }}</q-tooltip>
            </q-btn>
          </template>
        </template>
        <template v-else-if="props.col.type == 'enabled'">
          <q-avatar
            size="sm"
            :color="props.row.enabled ? 'secondary' : 'danger'"
            :icon="props.row[props.col.field] ? 'check' : 'clear'"
            text-color="white"
          />
        </template>
        <template v-else-if="props.col.type == 'check'">
          <q-icon
            v-if="props.row[props.col.field]"
            name="check"
            size="sm"
            color="secondary"
          />
        </template>
        <template v-else-if="props.col.type == 'datetime'">
          {{ format(props.row[props.col.field], "datetime") }}
        </template>
        <template v-else-if="props.col.type == 'number'">
          {{ format(props.row[props.col.field], "number") }}
        </template>
        <template v-else-if="props.col.type == 'chips'">
          <template v-if="props.row.roles">
            <q-chip
              v-for="(role, index) in props.row[props.col.field]"
              dense
              :color="props.col.color"
              :text-color="props.col.textColor"
              :key="index"
            >
              {{ role }}
            </q-chip>
          </template>
        </template>
        <template v-else-if="props.col.type == 'label'">
          <q-chip
            :color="
              props.col.color
                ? getLabelColor(
                    props.col.options.find(
                      (o) => o.value == props.row[props.col.field]
                    )?.value
                  )
                : 'secondary'
            "
            text-color="white"
            square
            dense
          >
            {{
              props.col.options.find(
                (o) => o.value == props.row[props.col.field]
              )?.label
            }}
          </q-chip>
        </template>
        <template v-else-if="props.col.type == 'info'">
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
        <template v-else>
          {{ props.row[props.col.field] ? props.row[props.col.field] : "-" }}
        </template>
      </q-td>
    </template>
  </q-table>
</template>

<script setup>
import { computed, ref } from "vue";
import { format } from "../functions";

const props = defineProps([
  "columns",
  "rows",
  "rowKey",
  "loading",
  "pagination",
  "height",
  "dense",
  "totalCost",
]);
const emit = defineEmits(["update:pagination", "request"]);
defineExpose({ requestServerInteraction });

const tableRef = ref();
const _pagination = computed({
  get() {
    return props.pagination;
  },
  set(value) {
    emit("update:pagination", value);
  },
});

function handleIcon(status) {
  const icons = {
    confirmed: "visibility",
    receiving: "visibility",
    finished: "visibility",
    default: "edit",
  };

  return icons[status] || icons.default;
}

function getLabelColor(status) {
  const colors = {
    draft: "grey",
    approved: "green",
    requested: "purple-12",
    confirmed: "blue",
    receiving: "teal",
    finished: "green",
    cancelled: "red",
  };
  return colors[status];
}

function requestServerInteraction() {
  tableRef.value.requestServerInteraction();
}

function request(props) {
  emit("request", props);
}
</script>
