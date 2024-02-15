<template>
  <div class="container q-gutter-md cursor-pointer" v-if="summaryStatus">
    <div class="counter-wrapper text-center draft">
      <q-tooltip v-if="Object.keys(orderDetails.draft).length">
        <div
          v-for="[key, value] of Object.entries(orderDetails.draft)"
          :key="key"
        >
          {{ key }} : {{ value }}
        </div>
      </q-tooltip>
      <div>
        <q-icon name="edit_square" />
        <span class="counter-header">Rascunho</span>
        <q-separator color="white" class="q-my-sm" />
      </div>

      <vue3-autocounter
        class="text-h3"
        ref="counter-draft"
        :startAmount="0"
        :endAmount="summaryStatus.draft"
        :duration="1"
        separator=","
        decimalSeparator="."
        :autoinit="true"
      />
    </div>
    <div class="counter-wrapper text-center approved">
      <q-tooltip v-if="Object.keys(orderDetails.approved).length">
        <div
          v-for="[key, value] of Object.entries(orderDetails.approved)"
          :key="key"
        >
          {{ key }} : {{ value }}
        </div>
      </q-tooltip>
      <div>
        <q-icon name="verified" />
        <span class="counter-header">Aprovado</span>
        <q-separator color="white" class="q-my-sm" />
      </div>

      <vue3-autocounter
        class="text-h3"
        ref="counter-approved"
        :startAmount="0"
        :endAmount="summaryStatus.approved"
        :duration="0.7"
        separator=","
        decimalSeparator="."
        :autoinit="true"
      />
    </div>
    <div class="counter-wrapper text-center requested">
      <q-tooltip v-if="Object.keys(orderDetails.requested).length">
        <div
          v-for="[key, value] of Object.entries(orderDetails.requested)"
          :key="key"
        >
          {{ key }} : {{ value }}
        </div>
      </q-tooltip>
      <div>
        <q-icon name="shopping_cart_checkout" />
        <span class="counter-header">Pago</span>
        <q-separator color="white" class="q-my-sm" />
      </div>

      <vue3-autocounter
        class="text-h3"
        ref="counter-requested"
        :startAmount="0"
        :endAmount="summaryStatus.requested"
        :duration="0.7"
        separator=","
        decimalSeparator="."
        :autoinit="true"
      />
    </div>
    <div class="counter-wrapper text-center confirmed">
      <q-tooltip v-if="Object.keys(orderDetails.confirmed).length">
        <div
          v-for="[key, value] of Object.entries(orderDetails.confirmed)"
          :key="key"
        >
          {{ key }} : {{ value }}
        </div></q-tooltip
      >
      <div>
        <q-icon name="currency_exchange" />
        <span class="counter-header">Confirmado</span>
        <q-separator color="white" class="q-my-sm" />
      </div>

      <vue3-autocounter
        class="text-h3"
        ref="counter-confirmed"
        :startAmount="0"
        :endAmount="summaryStatus.confirmed"
        :duration="0.7"
        separator=","
        decimalSeparator="."
        :autoinit="true"
      />
    </div>
    <div class="counter-wrapper text-center receiving">
      <q-tooltip v-if="Object.keys(orderDetails.receiving).length">
        <div
          v-for="[key, value] of Object.entries(orderDetails.receiving)"
          :key="key"
        >
          {{ key }} : {{ value }}
        </div></q-tooltip
      >
      <div>
        <q-icon name="local_shipping" />
        <span class="counter-header">Recebendo</span>
        <q-separator color="white" class="q-my-sm" />
      </div>

      <vue3-autocounter
        class="text-h3"
        ref="counter-receiving"
        :startAmount="0"
        :endAmount="summaryStatus.receiving"
        :duration="0.7"
        separator=","
        decimalSeparator="."
        :autoinit="true"
      />
    </div>
    <div class="counter-wrapper text-center finished">
      <q-tooltip v-if="Object.keys(orderDetails.finished).length">
        <div
          v-for="[key, value] of Object.entries(orderDetails.finished)"
          :key="key"
        >
          {{ key }} : {{ value }}
        </div></q-tooltip
      >
      <div>
        <q-icon name="check_circle" />
        <span class="counter-header">Finalizado</span>
        <q-separator color="white" class="q-my-sm" />
      </div>

      <vue3-autocounter
        class="text-h3"
        ref="counter-finished"
        :startAmount="0"
        :endAmount="summaryStatus.finished"
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
  props: ["summaryStatus", "orderDetails"],
  data() {},
};
</script>

<style lang="scss" scoped>
.container {
  display: grid;
  grid-template-columns: repeat(3, auto);
  justify-content: space-around;
}

.counter-wrapper {
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

.draft {
  background-color: grey;
  i {
    color: white;
  }
}

.approved {
  background-color: $green-6;
  i {
    color: white;
  }
}

.requested {
  background-color: $purple-5;
  i {
    color: white;
  }
}

.confirmed {
  background-color: $primary;
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

.finished {
  background-color: $blue-grey-8;
  i {
    color: white;
  }
}
</style>
