<template>
  <div class="row login-wrapper q-mt-xl">
    <q-card flat bordered class="login-card">
      <q-card-section
        class="text-h6 text-black row justify-center logo-container"
      >
        <q-img
          src="../../assets/logo-watchtime-preto.png"
          height="50%"
          width="50%"
          class="q-mr-md"
        />
      </q-card-section>
      <q-card-section class="q-gutter-y-md">
        <q-form @submit.prevent="login" class="q-gutter-y-md">
          <q-input
            outlined
            label="Email"
            lazy-rules="ondemand"
            type="email"
            v-model="user.email"
            color="grey-7"
          >
            <template v-slot:prepend>
              <q-icon name="alternate_email" />
            </template>
          </q-input>

          <q-input
            outlined
            label="Senha"
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
            />
          </div>
        </q-form>
      </q-card-section>
      <q-card-section>
        <div class="row justify-center">
          Esqueceu a senha?
          <router-link class="text-dark remove-underline" to="/reset_password">
            <strong>Clique aqui</strong>
          </router-link>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import AuthService from "../../services/AuthService";

const showPassword = ref(false);
const user = ref({});
const router = useRouter();
const working = ref(false);

async function login() {
  working.value = true;
  try {
    await AuthService.login(user.value.email, user.value.password);
    router.push({ path: "/services" });
  } catch (error) {}
  working.value = false;
}
</script>

<style scoped>
.login-wrapper {
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.login-card {
  width: 500px;
  border-radius: 8px;
}

.logo-container {
  background-color: #1976d2;
}

.remove-underline {
  text-decoration: none;
}
</style>
