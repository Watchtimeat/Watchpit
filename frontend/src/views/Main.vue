<template>
  <q-layout view="hHh lpR fff">
    <!-- top -->
    <q-header class="text-black logo-container">
      <q-toolbar class="logo-wrapper">
        <q-btn flat round icon="menu" @click="miniState = !miniState" />
        <q-btn flat href="/">
          <q-img
            src="../assets/logo-watchtime-preto.png"
            height="35px"
            width="174px"
            class="q-mr-md"
          />
        </q-btn>

        <q-toolbar-title></q-toolbar-title>
      </q-toolbar>
    </q-header>

    <!-- sidebar -->
    <q-drawer
      :mini="miniState"
      show-if-above
      v-model="leftDrawerOpen"
      side="left"
      class="drawer"
    >
      <q-list>
        <!-- current user -->
        <q-item>
          <q-item-section avatar v-show="!miniState">
            <q-icon name="o_account_circle" />
          </q-item-section>
          <q-item-section class="text-weight-medium">
            {{ currentUser.name }}
          </q-item-section>
          <q-btn dense flat icon="o_logout" @click="logout" />
        </q-item>
        <q-separator />

        <!-- menu -->
        <template v-for="(menuItem, index) in menuList">
          <template v-if="menuItem.children && canView(menuItem)">
            <q-expansion-item
              :content-inset-level="1"
              :icon="menuItem.icon"
              :label="menuItem.label"
              :key="index"
            >
              <q-list>
                <template v-for="(subItem, subIndex) in menuItem.children">
                  <q-item
                    v-if="canView(subItem)"
                    clickable
                    :to="subItem.link"
                    :key="subIndex"
                    active-class="menu-link"
                  >
                    <q-item-section avatar>
                      <q-icon :name="subItem.icon" />
                    </q-item-section>
                    <q-item-section>
                      {{ subItem.label }}
                    </q-item-section>
                  </q-item>
                </template>
              </q-list>
            </q-expansion-item>
          </template>
          <template v-else>
            <q-item
              v-if="canView(menuItem)"
              clickable
              :to="menuItem.link"
              :key="index"
              active-class="menu-link"
            >
              <q-item-section avatar>
                <q-icon :name="menuItem.icon" />
              </q-item-section>
              <q-item-section>
                {{ menuItem.label }}
              </q-item-section>
            </q-item>
          </template>
        </template>
      </q-list>
    </q-drawer>

    <!-- main page -->
    <q-page-container>
      <q-page class="q-pa-sm">
        <router-view />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from "vue";
import { computed } from "@vue/reactivity";
import { useRouter } from "vue-router";
import AuthService from "../services/AuthService";

const router = useRouter();
const menuList = [
  { icon: "o_home", label: "Home", link: "/home" },
  { icon: "o_shop_two", label: "Pedidos de Compra", link: "/purchase_orders", requires: "forniture" },
  { icon: "o_description", label: "Invoices", link: "/purchase_invoices", requires: "forniture"},
  { icon: "o_watch", label: "Ordens de Serviço", link: "/services", requires:"os" },
  { icon: "o_local_shipping", label: "NF de Entrada", link: "/importation" ,requires: "forniture"},
  { icon: "o_sell", label: "Produtos", link: "/products", requires: "forniture"},
  {
    icon: "o_build",
    label: "Separação de Peças",
    link: "/parts_conference",
    requires: "forniture"
  },
  {
    icon: "o_settings",
    label: "Configurações",
    children: [
      {
        icon: "o_business",
        label: "Geral",
        link: "/settings/general",
        requires: "administrator",
      },
      {
        icon: "o_account_circle",
        label: "Preferências",
        link: "/settings/user",
      },
      {
        icon: "o_groups",
        label: "Usuários",
        link: "/settings/users",
        requires: "administrator",
      },
    ],
  },
  { icon: "video_file", label: "Vídeos", link: "/videos" },
  { icon: "o_info", label: "Sobre o Cockpit", link: "/info" },
];
const leftDrawerOpen = ref();
const miniState = ref(false);
const currentUser = computed(() => AuthService.user);

function canView(item) {
  const currentUser = AuthService.user;
  if (item.requires) {
    if (item.requires == "administrator") return currentUser.administrator;
    if (item.requires == "forniture") return currentUser.forniture;
    if (item.requires == "os") return currentUser.os;
    else return currentUser.roles && currentUser.roles.indexOf(item.requires);
  } else {
    return true;
  }
}

function drawerClick(e) {
  if (miniState.value) {
    miniState.value = false;

    e.stopPropagation();
  }
}

async function logout() {
  AuthService.logout();
  await router.push({ path: "/login" });
}
</script>

<style lang="scss" scoped>
.logo-container {
  background-color: #fab515;
}

.logo-wrapper {
  padding: 0 8px;
  height: 60px;
}

.menu-link {
  background: #e6e6f091;
  font-weight: 500;
  width: 98%;
  margin-left: 2%;
  border-top-left-radius: 50px;
  border-bottom-left-radius: 50px;
}

.drawer a:hover {
  border-top-left-radius: 50px;
  border-bottom-left-radius: 50px;
  margin-left: 2%;
}
</style>
