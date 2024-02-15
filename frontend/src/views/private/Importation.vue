<template>
  <div class="background-page wt-border">
    <div class="q-pl-lg q-pb-xl q-pt-lg ">
  <q-page padding>
    <q-form @submit.prevent="handleSubmit">
      <h5>Dados Pedido de Compra</h5>
      <q-row>
        <q-col>
          <q-input outlined label="Comprador:" name=comprador v-model="comprador" required />
        </q-col>
        <q-col>
          <q-select
            outlined
            label="Fornecedor:"
            name=fornecedor
            v-model="fornecedor"
            :options="[
              { label: 'Audemars Piguet', value: '237311' },
              { label: 'Breitling', value: 'BRE' },
              { label: 'Bulgari', value: '253968' },
              { label: 'Chopard', value: '286304' },
              { label: 'Frederique Constant', value: '253719' },
              { label: 'Hamilton', value: '252464' },
              { label: 'Hublot', value: '253969' },
              { label: 'H Moser & Cie', value: '051462' },
              { label: 'Longines', value: '250712' },
              { label: 'MIDO', value: '210862' },
              { label: 'Omega', value: 'OMEGA' },
              { label: 'Rado', value: '286316' },
              { label: 'Swatch', value: '283899' },
              { label: 'TAG Heuer', value: '210860' },
              { label: 'TISSOT', value: '238333' },
              { label: 'Ulysse Nardin', value: '253717' },
              { label: 'Zenith', value: 'ZENITH' },
            ]"
          />
        </q-col>
        <q-col>
          <q-input outlined label="Referência:" name=ref v-model="ref" maxlength="50" required />
        </q-col>
      </q-row>
      <q-row>
        <q-col>
          <q-select outlined label="Loja:" name=loja v-model="loja" :options="['PR', 'SP', 'RJ']" />
        </q-col>
        <q-col>
          <q-input outlined label="Número DI:" name=dir v-model="dir" maxlength="12" required />
        </q-col>
        <q-col>
          <q-input outlined label="Data do DI:" name="dataDir" v-model="dataDir" type="date" required />
        </q-col>
        <q-col>
          <q-input outlined label="Desembaraço - UF:" name=desembaracoUF v-model="desembaracoUF" maxlength="2" required />
        </q-col>
      </q-row>
      <q-row>
        <q-col>
          <q-input outlined label="Desembaraço - Local:" name=desembaracoLocal v-model="desembaracoLocal" required />
        </q-col>
        <q-col>
          <q-input outlined label="Data do Desembaraço:" name="dataDesenbaraco" v-model="datadesembaraco" type="date" required />
        </q-col>
        <q-col>
          <q-input outlined label="CFOP:" name=cfop v-model="cfop" maxlength="4" required />
        </q-col>
        <q-col>
          <q-input outlined label="Aliquota ICMS:" name=aliquota v-model="aliquota" maxlength="3" required />
        </q-col>
      </q-row>

      <h5>Calculo de Câmbio</h5>

      <q-row>
       <q-col>
       <q-input outlined type="number" step="0.01" label="Valor Declarado em R$:" name="valorDeclarado" v-model="valorDeclarado" maxlength="10" required />
        </q-col>
      <q-col>
      <q-input outlined type="number" step="0.01" label="Valor Frete em R$:" name="valorFrete" v-model="valorFrete" maxlength="10" required />
      </q-col>
      <q-col>
       <q-input outlined type="number" step="0.01" label="Valor Total dos Itens em CHF:" name="valorItens" v-model="valorItens" maxlength="10" required />
      </q-col>
      </q-row>
      <q-col>
        <br>
        <q-uploader
        :extensions="['xlsx']"
        :max-size="1000000"
        :max-files="1"
        @input="handleFileUpload"
        label="Selecione um arquivo"
      />
      </q-col>
      <q-col>
        <br>
      <q-btn label="enviar" type="submit" color="primary" :loading="isLoading"/>
      </q-col>
    </q-form>
  </q-page>
</div>
</div>
<error-dialog v-if="errorDialogVisible" :errors="receivedErrors" v-model="errorDialogVisible"></error-dialog>
<q-spinner-gears
  v-if="isLoading"
  color="primary"
  size="40px"
  class="q-mt-md"
/>
</template>


<script>
import axios from 'axios';
import { Notify } from 'quasar';
import ErrorDialog from '../../types/ErrorDialog.vue';

export default {
  components: {
    ErrorDialog,
    QSpinnerGears,
  },
  data() {
    return {
      errorDialogVisible: false,
      isLoading: false,
      receivedErrors: [],
      showErrorDialog: false,
      errorList: [],
      comprador: '',
      fornecedor: '',
      ref: '',
      loja: '',
      dir: '',
      dataDir: '',
      desembaracoUF: '',
      desembaracoLocal: '',
      datadesembaraco: '',
      cfop: '',
      aliquota: '',
      valorDeclarado: '',
      valorFrete: '',
      valorItens: '',
      file: null,
    };
  },
  methods: {
    showErrors(errors) {
      this.receivedErrors = errors.error;
      this.errorDialogVisible = true;
    },
    async handleSubmit() {
      const jsonData = {
        comprador: this.comprador,
        fornecedor: this.fornecedor.value,
        ref: this.ref,
        loja: this.loja,
        dir: this.dir,
        dataDir: this.dataDir,
        desembaracoUF: this.desembaracoUF,
        desembaracoLocal: this.desembaracoLocal,
        datadesembaraco: this.datadesembaraco,
        cfop: this.cfop,
        aliquota: parseInt(this.aliquota),
        valorDeclarado: parseFloat(this.valorDeclarado),
        valorFrete: parseFloat(this.valorFrete),
        valorItens: parseFloat(this.valorItens),
      };

      const formData = new FormData();
      formData.append('data', JSON.stringify(jsonData));
      formData.append('file', this.file);

      this.isLoading = true;
      try {
        const response = await axios.post('https://app.watchtime.com.br/api/estoklus/importation', formData);

        if (response.status === 200) {
          if (response.data.success) {
            // Show success notification
            Notify.create({
              type: 'positive',
              message: response.data.success,
            });
          } else if (response.data.error && Array.isArray(response.data.error)) {
            // Show error modal
            this.showErrors(response.data);
          } else if (response.data.error) {
            // Show error notification
            Notify.create({
              type: 'negative',
              message: response.data.error,
            });
          }
        } else {
          // Handle non-200 response status
          Notify.create({
            type: 'negative',
            message: 'An unexpected error occurred.',
          });
        }
      } catch (error) {
        // Handle network or other errors
        Notify.create({
          type: 'negative',
          message: 'An error occurred while processing the request.',
        });
      }   finally {
    this.isLoading = false;
  }
      
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
  },
};
</script>

<style lang="scss" scoped>
img {
  filter: grayscale(100%) blur(7px);
}

h4 {
  font-size: 16px;
}

.background-page {
  background: white;
}

q-col{
  padding: 5px;
}

.botao{
  padding-top: 5px;
}
</style>
