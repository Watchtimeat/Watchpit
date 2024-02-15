<template>
  <div class="row justify-around q-gutter-md cursor-pointer">
    <div class="counter-wrapper text-center requested">
      <q-tooltip v-if="Object.keys(invoicingDetails.requested).length">
        <div
          v-for="[key, value] of Object.entries(invoicingDetails.requested)"
          :key="key"
        >
          {{ key }} : {{ value }}
        </div>
      </q-tooltip>
      <div>
        <q-icon name="currency_exchange" />
        <span class="counter-header">Pago</span>
        <q-separator color="white" class="q-my-sm" />
      </div>

      <vue3-autocounter
        class="text-h3"
        ref="counter-requested"
        :startAmount="0"
        :endAmount="invoiceSummary?.requested || 0"
        :duration="0.7"
        separator=","
        decimalSeparator="."
        :autoinit="true"
      />
    </div>

    <div class="counter-wrapper text-center receiving">
      <div>
        <q-icon name="local_shipping" />
        <span class="counter-header">Recebendo</span>
        <q-separator color="white" class="q-my-sm" />
      </div>

      <vue3-autocounter
        class="text-h3"
        ref="counter-receiving"
        :startAmount="0"
        :endAmount="invoiceSummary?.receiving || 0"
        :duration="0.7"
        separator=","
        decimalSeparator="."
        :autoinit="true"
      />
    </div>

    <div class="counter-wrapper text-center received">
      <div>
        <q-icon name="check_circle" />
        <span class="counter-header">Recebido</span>
        <q-separator color="white" class="q-my-sm" />
      </div>

      <vue3-autocounter
        class="text-h3"
        ref="counter-receiving"
        :startAmount="0"
        :endAmount="invoiceSummary?.received || 0"
        :duration="0.7"
        separator=","
        decimalSeparator="."
        :autoinit="true"
      />
    </div>
    <div class="counter-wrapper text-center canceled">
      <div>
        <q-icon name="cancel" />
        <span class="counter-header">Cancelado</span>
        <q-separator color="white" class="q-my-sm" />
      </div>

      <vue3-autocounter
        class="text-h3"
        ref="counter-canceled"
        :startAmount="0"
        :endAmount="invoiceSummary?.cancelled || 0"
        :duration="0.7"
        separator=","
        decimalSeparator="."
        :autoinit="true"
      />
    </div>
  </div>
</template>
<script>
export default {
  props: ["invoiceSummary", "invoicingDetails"],
  data() {
    return {};
  },
};
</script>

<style lang="scss" scoped>
.counter-wrapper {
  background: $secondary;
  color: white;
  border-radius: 8px;
  padding: 8px;
  width: 145px;
  height: 105px;
}

.counter-header {
  margin-left: 5px;
  font-size: 14px;
  font-weight: 500;
}

.requested {
  background-color: $primary;
  i {
    color: white;
  }
}

.canceled {
  background-color: $negative;
  i {
    color: white;
  }
}

.receiving {
  background-color: teal;
  i {
    color: white;
  }
}
.received {
  background-color: $green-6;
  i {
    color: white;
  }
}
</style>
