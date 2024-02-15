<q-card flat bordered style="min-width: 350px">
    <q-badge >Fotos</q-badge>

      <q-list bordered>
  <q-expansion-item
    group="somegroup"
    label="Frente"
  >
    <q-card>
      <q-card-section>
        <q-uploader
        ref="uploader"
        label="Carregar imagem"
        :max-files="1"
        accept="image/*"
        @added="onFilesAdded"
      />
      <q-img v-if="data.foto_frente !== null" :src="data.foto_frente" />

        <q-btn color='red' label="Tirar Foto" @click="openCamera('frente')"></q-btn>


      </q-card-section>
    </q-card>
  </q-expansion-item>

  <q-separator />

  <q-expansion-item group="somegroup" label="Lado Direto">
    <q-card>
      <q-card-section>
        <q-uploader
        ref="uploader"
        label="Carregar imagem"
        :max-files="1"
        accept="image/*"
        @added="onFilesAdded"
      />
      <q-img v-if="data.foto_lado_direito !== null" :src="data.foto_lado_direito" />

        <q-btn color='red' label="Tirar Foto" @click="openCamera('lado_direito')"></q-btn>

      </q-card-section>
    </q-card>
  </q-expansion-item>

  <q-separator />

  <q-expansion-item group="somegroup" label="Lado Esquerdo">
    <q-card>
      <q-card-section>
        <q-uploader
        ref="uploader"
        label="Carregar imagem"
        :max-files="1"
        accept="image/*"
        @added="onFilesAdded"
      />
      <q-img v-if="data.foto_lado_esquerdo !== null" :src="data.foto_lado_esquerdo" />

        <q-btn color='red' label="Tirar Foto" @click="openCamera('lado_esquerdo')"></q-btn>

      </q-card-section>
    </q-card>
  </q-expansion-item>

  <q-separator />

  <q-expansion-item
    group="somegroup"
    label="Face Norte"
  >
    <q-card class="bg-teal-2">
      <q-card-section>
        <q-uploader
        ref="uploader"
        label="Carregar imagem"
        :max-files="1"
        accept="image/*"
        @added="onFilesAdded"
      />
      <q-img v-if="data.foto_norte !== null" :src="data.foto_norte" />

        <q-btn color='red' label="Tirar Foto" @click="openCamera('norte')"></q-btn>

      </q-card-section>
    </q-card>
  </q-expansion-item>
  <q-separator />

<q-expansion-item
group="somegroup"
label="Face Sul"
>
<q-card class="bg-teal-2">
<q-card-section>
  <q-uploader
        ref="uploader"
        label="Carregar imagem"
        :max-files="1"
        accept="image/*"
        @added="onFilesAdded"
      />
      <q-img v-if="data.foto_sul !== null" :src="data.foto_sul" />

        <q-btn color='red' label="Tirar Foto" @click="openCamera('sul')"></q-btn>

</q-card-section>
</q-card>
</q-expansion-item>

<q-separator />

<q-expansion-item
group="somegroup"
label="Fundo"
>
<q-card class="bg-teal-2">
<q-card-section>
  <q-uploader
        ref="uploader"
        label="Carregar imagem"
        :max-files="1"
        accept="image/*"
        @added="onFilesAdded"
      />
      <q-img v-if="data.foto_fundo !== null" :src="data.foto_fundo" />

        <q-btn color='red' label="Tirar Foto" @click="openCamera('fundo')"></q-btn>

</q-card-section>
</q-card>
</q-expansion-item>


</q-list>