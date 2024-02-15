<template>
  <q-dialog full-width position="top" v-model="_show" @hide="$emit('close')">
    <q-card class="q-py-md q-px-md">
      <div class="row">
        <div class="title-style">Detalhes da invoice</div>
        <q-space />
        <q-btn icon="close" flat round dense @click="$emit('close')" />
      </div>
      <div class="row q-gutter-x-md q-pt-lg">
        <div class="q-mb-sm">
          <q-icon name="watch" class="info-container" />
          <span class="text-weight-medium text-caption"
            >Marca: {{ props.data?.brand || "-" }}</span
          >
        </div>

        <div class="q-mb-sm" v-if="props.data?.code">
          <q-icon name="code" class="info-container" />
          <span class="text-weight-medium text-caption"
            >Código da invoice: {{ props.data?.code || "-" }}</span
          >
        </div>

        <div class="q-mb-sm" v-if="props.data?.proforma_code">
          <q-icon name="code" class="info-container" />
          <span class="text-weight-medium text-caption"
            >Código da Proforma: {{ props.data?.proforma_code || "-" }}</span
          >
        </div>

        <div class="q-mb-sm">
          <q-icon name="person" class="info-container" />
          <span class="text-weight-medium text-caption"
            >Responsável: {{ props.data?.owner || "-" }}</span
          >
        </div>

        <div class="q-mb-sm">
          <q-icon name="description" class="info-container" />
          <span class="text-weight-medium text-caption"
            >Tracking: {{ props.data?.tracking || "-" }}</span
          >
        </div>

        <div class="q-mb-sm">
          <q-icon name="timer" class="info-container" />
          <span class="text-weight-medium text-caption"
            >Criada em:
            {{ format(props.data?.createdAt, "datetime") || "-" }}</span
          >
        </div>
        <div class="q-mb-sm">
          <q-icon name="timer" class="info-container" />
          <span class="text-weight-medium text-caption"
            >Pago em:
            {{ format(props.data?.payment_date, "date") || "-" }}</span
          >
        </div>

        <div class="q-mb-sm">
          <q-icon name="savings" class="info-container" />
          <span class="text-weight-medium text-caption"
            >Custo da invoice:
            {{ format(props.data?.total_cost || 0, "currency") }}</span
          >
        </div>
        <div class="q-mb-sm" v-if="props.data?.nf_date">
          <q-icon name="timer" class="info-container" />
          <span class="text-weight-medium text-caption"
            >Data da NF:
            {{ format(props.data?.nf_date, "datetime") || "-" }}</span
          >
        </div>
        <div class="q-mb-sm" v-if="props.data?.nf_value">
          <q-icon name="savings" class="info-container" />
          <span class="text-weight-medium text-caption"
            >Valor da NF:
            {{ format(props.data?.nf_value || 0, "currency") }}</span
          >
        </div>
        <div class="q-mb-sm" v-if="props.data?.nf_number">
          <q-icon name="description" class="info-container" />
          <span class="text-weight-medium text-caption"
            >NF: {{ props.data?.nf_number || "-" }}</span
          >
        </div>
        <div class="q-mb-sm" v-if="props.data?.customs_number">
          <q-icon name="description" class="info-container" />
          <span class="text-weight-medium text-caption"
            >DI/DIR: {{ props.data?.customs_number || "-" }}</span
          >
        </div>
      </div>

      <div class="q-pt-lg">
        <q-list bordered separator class="wt-border">
          <q-expansion-item
            default-opened
            expand-separator
            v-for="order in props.data?.order"
            :key="order.id"
            :label="'Pedido: #' + order.code"
            header-class="bg-grey-2"
            ><q-card>
              <q-table
                flat
                bordered
                :rows="order.items"
                :columns="columns"
                class="wt-border no-shadow"
                row-key="id"
                :selection="selection"
                v-model:selected="itemsSelectedComputed"
                :rows-per-page-options="[10, 25, 50]"
                :pagination="pagination"
                dense
              >
                <template v-slot:body-cell="props">
                  <q-td :props="props">
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
                      v-if="
                        !['currency', 'actions', 'info'].includes(
                          props.col.type
                        )
                      "
                    >
                      {{ props.row[props.col.field] }}
                    </template>
                  </q-td>
                </template>
              </q-table>
            </q-card></q-expansion-item
          >
        </q-list>
      </div>
      <div class="q-mt-md row">
        <q-space />
        <q-btn
          v-if="props?.data?.invoice_files"
          color="primary"
          icon="file_download"
          label="Todos"
          unelevated
          class="wt-border"
          download
          @click="
            getUploadedFile(props?.data?.invoice_files, 'zip', 'invoice_files')
          "
        >
          <q-tooltip>Baixar todos os arquivos da invoice</q-tooltip>
        </q-btn>
        <q-btn
          v-if="props?.data?.importation_files"
          color="secondary"
          icon="file_download"
          label="XLS"
          unelevated
          class="wt-border q-ml-sm"
          download
          @click="
            getUploadedFile(
              props?.data?.importation_files,
              'xls',
              'importation_files'
            )
          "
        >
          <q-tooltip>Baixar XLS</q-tooltip>
        </q-btn>
        <q-btn
          v-if="props?.data?.proforma_file_id"
          color="secondary"
          icon="file_download"
          label="Proforma"
          unelevated
          class="wt-border q-ml-sm"
          download
          @click="getUploadedFile(props?.data?.proforma_file_id, 'pdf', 'proforma')"
        >
          <q-tooltip>Baixar Proforma</q-tooltip>
        </q-btn>
        <q-btn
          v-if="props?.data?.cambio_file_id"
          color="secondary"
          icon="file_download"
          label="Contrato Câmbio"
          unelevated
          class="wt-border q-ml-sm"
          download
          @click="getUploadedFile(props?.data?.cambio_file_id, 'pdf', 'contrato')"
        >
          <q-tooltip>Baixar Contrato Cambio</q-tooltip>
        </q-btn>

        <q-btn
          color="secondary"
          v-if="props?.data?.invoice_file_id"
          icon="file_download"
          label="Invoice"
          unelevated
          class="wt-border q-ml-sm"
          download
          @click="
            getUploadedFile(props?.data?.invoice_file_id, 'pdf', 'invoice')
          "
        >
          <q-tooltip>Baixar Invoice</q-tooltip>
        </q-btn>
        <q-btn
          v-if="props?.data?.awb_file_id"
          color="secondary"
          icon="file_download"
          label="AWB"
          unelevated
          class="wt-border q-ml-sm"
          download
          @click="getUploadedFile(props?.data?.awb_file_id, 'pdf', 'awb')"
        >
          <q-tooltip>Baixar Awb</q-tooltip>
        </q-btn>
        <q-btn
          v-if="props?.data?.fatura_file_id"
          color="secondary"
          icon="file_download"
          label="Fatura"
          unelevated
          class="wt-border q-ml-sm"
          download
          @click="getUploadedFile(props?.data?.fatura_file_id, 'pdf', 'fatura')"
        >
          <q-tooltip>Baixar Fatura</q-tooltip>
        </q-btn>
        <q-btn
          v-if="props?.data?.nota_fiscal_file_id"
          color="secondary"
          icon="file_download"
          label="Nota Fiscal"
          unelevated
          class="wt-border q-ml-sm"
          download
          @click="
            getUploadedFile(props?.data?.nota_fiscal_file_id, 'pdf', 'nf')
          "
        >
          <q-tooltip>Baixar Nota Fiscal</q-tooltip>
        </q-btn>
      </div>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { computed, ref } from "vue";
import { format } from "@/functions";
import { columns } from "./constants";
import axios from "axios";
import { useQuasar } from "quasar";

const props = defineProps(["show", "id", "data"]);
const emit = defineEmits(["update:show", "close"]);
const $q = useQuasar();
const pagination = ref({ rowsPerPage: 50 });

const _show = computed({
  get: () => {
    return props.show;
  },
  set: (value) => emit("update:show", value),
});

async function getUploadedFile(fileId, fileType, fileName) {
  const url = `https://app.watchtime.com.br/api/resources/${fileId}/stream`;
  axios
    .get(url, {
      responseType: "blob",
    })
    .then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      if (fileType === "xls") {
        link.setAttribute("download", `${fileName}.xlsx`);
      }
      if (fileType === "zip") {
        link.setAttribute("download", `${fileName}.zip`);
      }
      if (fileType === "pdf") {
        link.setAttribute("download", `${fileName}.pdf`);
      }

      document.body.appendChild(link);
      link.click();
    });
  $q.notify({
    message: `Download ${fileName} efetuado com sucesso`,
    type: "positive",
    color: "green",
  });
}
</script>

<style>
.info-container {
  background: #e6e6f091;
  padding: 8px;
  border-radius: 8px;
  margin-right: 8px;
}
</style>
