<template>
    
    <div class="background-page wt-border">
    <div class="q-pl-lg q-pb-xl q-pt-lg ">
    <q-page padding>
      <div class="row justify-center">
        <div class="col-md-8">
          <h2 class="text-h6 q-my-md">Configurações - Geral</h2>
          <h3 class="text-h6 q-my-md">Atualização de Produtos</h3>
          <q-btn
            :loading="isLoading"
            color="primary"
            label="Atualizar Produtos"
            @click="updateProducts"
          />
        </div>
      </div>
      </q-page>
</div>
</div>
  </template>

<script>
import axios from "axios";
import { QSpinnerGears } from 'quasar';

export default {
    components: {
    QSpinnerGears,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  methods: {
    async updateProducts() {
      this.isLoading = true;
      try {
        const response = await axios.get(
          "https://app.watchtime.com.br/api/estoklus/products_importation"
        );
        if (response.data === "sem itens para criar") {
          this.$q.notify({
            color: "warning",
            message: "Não existem produtos para importar.",
          });
        } else {
          this.$q.notify({
            color: "positive",
            message: "Produtos importados com sucesso.",
          });
        }
      } catch (error) {
        console.error("Erro na atualização dos produtos:", error);
      } finally {
        this.isLoading = false;
      }
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