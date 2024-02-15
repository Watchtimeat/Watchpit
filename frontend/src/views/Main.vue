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
  { icon: "o_sell", label: "Estoque", link: "/products", requires: "forniture"},
  { icon: "o_person", label: "Cadastro de Pessoas", link: "/products", requires: "forniture"},
  { icon: "o_watch", label: "Cadastro de Relógios", link: "/products", requires: "forniture"}

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
  background-color: #1976d2;
}

.logo-wrapper {
  padding: 0 8px;
  height: 60px;
}

.menu-link {
  background: #ffffff91;
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
