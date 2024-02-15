<template>
  <div class="row reset-passwod-wrapper q-mt-xl">
    <q-card flat bordered style="width: 500px">
      <q-card-section>
        <q-form @submit.prevent="login" class="q-gutter-y-md">
          <q-input
            outlined
            label="Redefinir senha"
            lazy-rules="ondemand"
            :type="showPassword ? 'text' : 'password'"
            v-model="user.password"
            color="grey-7"
          >
            <template v-slot:append>
              <q-icon
                :name="showPassword ? 'visibility' : 'visibility_off'"
                class="cursor-pointer"
                @click="showPassword = !showPassword"
              />
            </template>
            <template v-slot:prepend>
              <q-icon name="lock_outline" />
            </template>
          </q-input>

          <div class="row">
            <q-space />
            <q-btn
              label="Entrar"
              type="submit"
              class="full-width wt-border"
              color="dark"
              :loading="working"
              :disable="!user.password"
            />
          </div>
        </q-form>
      </q-card-section>
      <q-card-section>
        <div class="row justify-center">
          <router-link class="text-dark remove-underline" to="/login">
            Voltar
          </router-link>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const user = ref({});
const router = useRouter();
const working = ref(false);
const showPassword = ref(false);

async function login() {
  working.value = true;
  try {
    console.log("mudar senha");
  } catch (error) {}
  working.value = false;
}
</script>

<style scoped>
.reset-passwod-wrapper {
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.remove-underline {
  text-decoration: none;
}
</style>
