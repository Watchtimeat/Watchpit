<template>
  <div>
    <app-table
      ref="tableRef"
      :columns="columns"
      :rows="users"
      row-key="id"
      :loading="loading"
      @request="loadUsers"
      class="q-pa-md"
      :pagination="pagination"
    >
      <template v-slot:top>
        <div class="row full-width q-mb-lg">
          <div class="title-style">Configurações - Usuários</div>
          <q-space />
          <q-btn
            size="md"
            color="green"
            unelevated
            style="border-radius: 8px"
            icon="add_circle"
            class="wt-border"
            label="Novo usuário"
            @click="add"
          >
            <q-tooltip>Adicionar um novo usuário</q-tooltip>
          </q-btn>
        </div>
      </template>
    </app-table>

    <modal-form title="Usuário" v-model:show="showUser" @confirm="confirmUser">
      <q-form @submit.prevent="confirmUser" class="q-gutter-sm">
        <q-input
          outlined
          stack-label
          label="Email"
          lazy-rules="ondemand"
          type="email"
          v-model="user.email"
          color="grey-7"
          autocomplete="off"
          :rules="[(value) => !!value || 'Email obrigatório']"
        />

        <q-input
          outlined
          stack-label
          label="Nome"
          lazy-rules="ondemand"
          type="text"
          v-model="user.name"
          color="grey-7"
          :rules="[(value) => !!value || 'Nome obrigatório']"
        />

        <q-input
          outlined
          stack-label
          label="Senha"
          lazy-rules="ondemand"
          :type="showPassword ? 'text' : 'password'"
          v-model="user.password"
          color="grey-7"
          autocomplete="off"
        >
          <template v-slot:append>
            <q-icon
              :name="showPassword ? 'visibility' : 'visibility_off'"
              class="cursor-pointer"
              @click="showPassword = !showPassword"
            />
          </template>
        </q-input>
        <q-select
          label="Usuário do Estoklus"
          outlined
          input-debounce="0"
          emit-value
          :options="UsersFiltered"
          v-model="user.estoklus_id"
          use-chips
          stack-label
          use-input
          color="grey-7"
          class="q-my-lg"
          @filter="filterUsers"
        >
        </q-select>
        <q-select
          label="Loja"
          outlined
          input-debounce="0"
          emit-value
          :options="Lojas"
          v-model="user.loja"
          use-chips
          stack-label
          use-input
          color="grey-7"
          class="q-my-lg"
          @filter="filterUsers"
        >
        </q-select>
        <q-select
          label="Permissões por marca"
          outlined
          input-debounce="0"
          :options="brandsFiltered"
          v-model="user.brands"
          multiple
          counter
          use-chips
          stack-label
          use-input
          color="grey-7"
          class="q-my-lg"
          @filter="filterBrand"
          :hint="
            user.brands.length > 1 ? `Itens selecionados` : `Item selecionado`
          "
        >
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey">Sem opções</q-item-section>
            </q-item>
          </template>

          <template v-slot:selected-item="scope">
            <q-chip
              removable
              @remove="scope.removeAtIndex(scope.index)"
              :tabindex="scope.tabindex"
              color="secondary"
              text-color="white"
            >
              {{ scope.opt.label }}
            </q-chip>
          </template>
        </q-select>

        <div>
          <q-toggle
            color="secondary"
            label="Habilitado"
            v-model="user.enabled"
            class="q-mt-none q-mr-sm"
          />

          <q-toggle
            color="secondary"
            label="Administrador"
            v-model="user.administrator"
          />
          <q-toggle
            color="secondary"
            label="Ordem de Serviço"
            v-model="user.os"
          />
          <q-toggle
            color="secondary"
            label="Fornitura"
            v-model="user.forniture"
          />
        </div>

        <div v-for="(control, index) in form" :key="index">
          <div class="q-mb-sm">{{ control.label }}</div>
          <q-option-group
            color="secondary"
            :options="control.options"
            type="checkbox"
            v-model="user[control.field]"
            :label="control.label"
            class="row"
          />
        </div>

        <div class="row">
          <q-space />
          <q-btn
            type="submit"
            class="full-width wt-border"
            color="dark"
            label="Confirmar"
            :disable="!user.name || !user.email || !user.password || !user.estoklus_id || !user.loja"
          />
        </div>
      </q-form>
    </modal-form>

    <modal-dialog
      title="Excluir"
      v-model="dialog"
      :message="removeUserMessage"
      @confirm="removeUser"
      @close="resetState"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useQuasar } from "quasar";
import UserService from "../../../services/UserService";
import AppTable from "../../../components/app-table.vue";
import ModalForm from "../../../components/modal-form.vue";
import ModalDialog from "../../../components/modal-dialog.vue";
import ProductsService from "@/services/ProductsService";
import OrdersServicesService from "@/services/Services";

const showPassword = ref(false);
const removeUserMessage = ref("");
const tableRef = ref();
const $q = useQuasar();
const loading = ref(false);
const updating = ref(false);
const users = ref([]);
const user = ref({});
const showUser = ref(false);
const dialog = ref(false);
const brands = ref([]);
const pagination = ref({ rowsPerPage: 50 });
const brandsFiltered = ref([]);
const Lojas = ref(['PR','SP','RJ']);
const estoklusUsers = ref([]);
const UsersFiltered = ref([]);

onMounted(() => {
  loadBrands();
  loadEstoklusUsers();
});

async function loadBrands() {
  const response = await ProductsService.getProducts({
    _select: "brand",
    _distinct: true,
    _order_a: "brand",
  });

  brands.value = response.data?.map((b) => {
    return { label: b.brand.toUpperCase(), value: b.brand };
  });
}


async function loadEstoklusUsers() {
  const response = await OrdersServicesService.getUsersEstoklus();
  console.log(response)

  estoklusUsers.value = response?.map((b) => {
    return { label: b.label.toUpperCase(), value: b.id };
  });

}

const columns = [
  {
    name: "enabled",
    align: "center",
    label: "Habilitado",
    field: "enabled",
    type: "enabled",
  },
  { name: "name", align: "left", label: "Nome", field: "name", type: "text" },
  {
    name: "email",
    align: "left",
    label: "Email",
    field: "email",
    type: "text",
  },
  {
    name: "administrator",
    align: "center",
    label: "Administrador",
    field: "administrator",
    type: "check",
  },
  {
    name: "roles",
    align: "center",
    label: "Papéis",
    field: "roles",
    color: "teal",
    textColor: "white",
    type: "chips",
  },
  {
    name: "last_login",
    align: "left",
    label: "Último Login",
    field: "last_login",
    type: "datetime",
  },
  {
    name: "actions",
    align: "center",
    type: "actions",
    actions: [
      {
        icon: "edit",
        color: "dark",
        toolTip: "Modificar usuário",
        action: (props) => {
          editUser(props);
        },
      },
      {
        icon: "delete",
        color: "red",
        toolTip: "Remover usuário",
        action: (props) => {
          openRemoveDialog(props);
        },
      },
    ],
  },
];

const form = [
  {
    name: "roles",
    label: "Papéis",
    field: "roles",
    options: [
      { label: "Planejamento", value: "Planejamento" },
      { label: "Estoques", value: "Estoques" },
      { label: "Consulta", value: "Consulta" },
    ],
  },
];

onMounted(() => {
  tableRef.value.requestServerInteraction();
});

async function loadUsers() {
  loading.value = true;
  try {
    users.value = await UserService.getUsers();
  } catch (error) {}
  loading.value = false;
}

async function add() {
  user.value = {
    enabled: false,
    administrator: false,
    roles: [],
    brands: [],
  };
  showUser.value = true;
}

async function editUser(props) {
  loading.value = true;
  try {
    user.value = await UserService.getUserById(props.key);
  } catch (error) {}
  loading.value = false;
  showUser.value = true;
}

async function confirmUser() {
  updating.value = true;
  try {
    if (user.value.id) {
      await UserService.updateUser(user.value);
      $q.notify({
        message: `Usuário ${user.value.name} atualizado`,
        type: "positive",
        color: "green",
      });
      tableRef.value.requestServerInteraction();
    } else {
      await UserService.addUser(user.value);
      $q.notify({
        message: `Usuário ${user.value.name} adicionado`,
        type: "positive",
        color: "green",
      });
      tableRef.value.requestServerInteraction();
    }
  } catch (error) {}
  updating.value = false;
  showUser.value = false;
}

async function removeUser() {
  try {
    await UserService.deleteUser(user.value.row);
    tableRef.value.requestServerInteraction();

    $q.notify({
      message: `Usuário ${user.value.row.name} removido com sucesso`,
      type: "positive",
      color: "green",
    });
  } catch (error) {
    $q.notify({
      message: `Erro ao remover o usuário ${user.value.row.name}`,
      type: "negative",
      color: "danger",
    });
  }
}

function resetState() {
  user.value = {};
}

function openRemoveDialog(props) {
  user.value = props;
  removeUserMessage.value = `Você deseja confirmar a remoção do usuário "${props.row.name}"?`;
  dialog.value = true;
}

function filterBrand(val, update) {
  if (val === "") {
    update(() => {
      brandsFiltered.value = brands.value;
    });
    return;
  }

  update(() => {
    brandsFiltered.value = brands.value.filter(
      (brand) => brand.label.toLowerCase().indexOf(val.toLowerCase()) > -1
    );
  });
}

function filterUsers(val, update) {
  if (val === "") {
    update(() => {
      UsersFiltered.value = estoklusUsers.value;
    });
    return;
  }

  update(() => {
    UsersFiltered.value = estoklusUsers.value.filter(
      (user) => user.label.toLowerCase().indexOf(val.toLowerCase()) > -1
    );
  });
}
</script>
