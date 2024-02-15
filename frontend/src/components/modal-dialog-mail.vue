<template>
  <q-dialog v-model="toggleDialogMail" maximized>
    <q-card class="wt-border q-pa-md">
      <q-card-section class="row items-center q-pa-none">
        <div class="title-style q-pa-none">  Enviar e-mail </div>
        <q-space />
        <q-btn icon="close" @click="close" flat round dense v-close-popup />
      </q-card-section>
      <q-card-section class="row items-center q-pa-none">
        <q-toggle color="green" label="Enviar PDF no E-mail" v-model="toggleAnexo" />
      </q-card-section>
      <q-card-section >
        <q-input v-model="OS.titulo_email" label="Título" class="q-mt-sm" outlined placeholder="Digite o título aqui..." />
        <q-input v-model="OS.texto_email" type="textarea" label="Texto" class="q-mt-sm" hint="Esse texto será inserido no histórico da OS" outlined placeholder="Digite o texto aqui...">
        </q-input>
      </q-card-section>

      <div style="width: 80%;height: 40%;" class="row inline items-start justify-evenly q-pa-sm">
        <q-card style="width: 40%;height: 40%" >
          <q-card-section>
        <div class="text-h6">Fotos da OS {{ OS.id }}</div>

      </q-card-section>
    <q-carousel
      
      v-if="imagesBase64.length > 0"
      animated
      style="height: 300px"
      v-model="slide"
      arrows
      infinite
      thumbnails
    >
      <q-carousel-slide
        v-for="(imageBase64, index) in imagesBase64"
        
        :key="index"
        :name="index"
        :img-src="imageBase64"
      />
      <template v-slot:control>
      <q-carousel-control position="top-left" :offset="[18, 18]" class="q-gutter-xs">
        <div>
          <q-btn push color="green"  icon="add" @click="selectImageForSending(imagesBase64[slide])" />
        </div>
        </q-carousel-control>
      </template>
    </q-carousel>
    <div v-else class="flex flex-center">
      <div class="text-h5 ">Nenhuma imagem disponível</div>
    </div>
  </q-card>
  <q-card style="width: 40%;height: 40%;" >
    <q-card-section>
        <div class="text-h6">Itens à enviar no e-mail</div>

      </q-card-section>
    <q-carousel
      animated
      v-if="selectedImagesBase64.length > 0"
      v-model="selectedSlide"
      arrows
      style="height: 300px"
      infinite
      thumbnails
    >
      <q-carousel-slide
        v-for="(imageBase64, index) in selectedImagesBase64"
        :key="index"
        :name="index"
        :img-src="imageBase64"
      >
      </q-carousel-slide>
      <template append v-slot:control>
      <q-carousel-control position="top-left" :offset="[18, 18]" class="q-gutter-xs">
        <q-btn push color="red" icon="remove" @click="removeImageFromSending(selectedSlide)" />
      </q-carousel-control>
      </template>
    </q-carousel>
    <div v-else >
      <div class="text-h5">Nenhuma imagem selecionada</div>
    </div>
  </q-card>
  </div>
      <q-card-actions align="right" class="q-pa-none q-mt-sm">
        <q-btn
          flat
          :label="cancelText ? cancelText : `Cancelar`"
          color="grey"
          v-close-popup
          @click="close"
          class="wt-border"
        />
        <q-btn
          unelevated
          :label="confirmationText ? confirmationText : `Confirmar`"
          color="secondary"
          @click="confirm"
          v-close-popup
          class="wt-border"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { computed,ref,watch,onMounted } from "vue";
import { Notify } from 'quasar';
import axios from "axios";

const props = defineProps([
  "title",
  "confirmationText",
  "dialog",
  "cancelText",
  "message",
  "text",
  "OS",
  "imagesBase64"
]);
const emit = defineEmits(["confirm", "close", "update:dialog","userTitle","userText"]);
const slide = ref(0)
const userText = ref('')
const userTitle = ref('')
const selectedSlide = ref(0)
const toggleAnexo = ref(true)
const toggleDialogMail = computed({
  get: () => {
    console.log(toggleDialogMail)
    return props.toggleDialogMail;
  },
  set:(value) => {
    console.log(toggleDialogMail)
    emit("update:dialog", value);
  },
});
watch(
  () => toggleDialogMail.value,
  (newValue, oldValue) => {
    if (newValue == true){
      console.log("abreiu")
    }
  }
);
const selectedImagesBase64 = ref([])

const selectImageForSending = (imageBase64) => {
  if (!selectedImagesBase64.value.includes(imageBase64)) {
    selectedImagesBase64.value.push(imageBase64)
    console.log(props.imagesBase64.length)
    if (slide.value < props.imagesBase64.length -1 ){
    slide.value++
  }
  } else {
    Notify.create({
              type: 'negative',
              message: 'Imagem já foi selecionada.'
            });
  }
}
const removeImageFromSending = (index) => {
  // Não precisa buscar a imagem em `props.imagesBase64` já que `index` refere-se a `selectedImagesBase64`
  if (index >= 0 && index < selectedImagesBase64.value.length) {
    // Remove a imagem diretamente de `selectedImagesBase64`
    selectedImagesBase64.value.splice(index, 1);
    
    // Atualiza o slide selecionado, se necessário
    if (selectedSlide.value >= selectedImagesBase64.value.length) {
      // Se o slide selecionado agora é maior que o número total de slides, atualiza para o último slide
      selectedSlide.value = Math.max(0, selectedImagesBase64.value.length - 1);
    }
  } else {
    console.log('Índice fora do intervalo.');
  }
}
async function carregaImagens(){
  
  try {
    const response = await axios.post(
      `https://app.watchtime.com.br/api/mail/listar_fotos`,
      dataToSubmit
    );
    imagesBase64 = response.data
  }
    catch{
      
    }

}

function loadtext(){

}

async function confirm() {

  try {
    let anexaPDF = 'S'
    if (!toggleAnexo.value){
      anexaPDF = 'N'
    }

    const response = await axios.post('https://app.watchtime.com.br/api/mail/via_cliente', {
      codigo_estoklus: props.OS.codigo_estoklus, // Código Estoklus
      loja: props.OS.loja,
      id:  props.OS.id,
      status: props.OS.status,
      anexosBase64: selectedImagesBase64.value, 
      titulo:props.OS.titulo_email,
      texto_usuario:props.OS.texto_email,
      envia_pdf: anexaPDF// Array de imagens selecionadas codificadas em base64
      // Outros dados necessários para a função `envia_email`
    });
    if (response.data === 'OK') {
      Notify.create({
              type: 'positive',
              message: `E-mail enviado`
            });
    }
  } catch (error) {
    Notify.create({
              type: 'negative',
              message: error
            });
  }

    emit("confirm", userTitle.value,userText.value);
    userTitle.value = ''
    userText.value = ''

}

function close() {
  emit("close");
  selectedSlide.value = 0
  selectedImagesBase64.value = []
  
}
</script>
