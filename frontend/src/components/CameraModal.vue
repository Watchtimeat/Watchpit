<template>
      <div class="flex full-height row items-center justify-around">
      <q-card class="wt-border">
        <div class="flex full-height row items-center justify-center q-mt-md">
      <video ref="video" autoplay></video>
      <q-btn  label="Tirar Foto" color='red' @click="captureImage" style="padding-left:4px"/>
    </div>
    </q-card>
    <q-card style="width: 20%" class="flex full-height row items-center justify-center">
      
      <div class="text-h6">Foto  </div> 
      <q-img v-if="imageUrl !== null" :src="imageUrl" />
      <q-btn v-if="imageUrl !== null" label="Gravar" color="green" @click="salvarImagem()" />
    
    </q-card>
    <q-uploader
        label="upload (clique na nuvem para enviar as fotos)"
        multiple
        batch
        :factory="CustomUpload"
        style="width: 40%"
        color="blue"
        accept=".jpg, .jpeg"
      />
  </div>

  <div class="flex full-height row items-center justify-center">

    </div>
</template>

<script>
import { onMounted,onBeforeUnmount, ref, toRefs  } from "vue";
import { useQuasar } from "quasar";
import axios from "axios";
import { Notify } from 'quasar';
export default {
  props: ['modalClosed','photoType','data'],
  setup(props) {

    const { photoType, data } = toRefs(props);
    const capturedImages = ref({});
    const video = ref(null);
    const imageUrl = ref(null);
    const mediaStream = ref(null);


    const startCamera = async () => {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
              try {
                  const stream = await navigator.mediaDevices.getUserMedia(   {  video: {
        width: { ideal: 1920 },
        height: { ideal: 1080 }
    } });
                  if (video.value) {
                      video.value.srcObject = stream;
                  }
                  mediaStream.value = stream;
              } catch (error) {
                  console.error("Erro ao acessar a câmera:", error);
              }
          } else {
              console.log("getUserMedia não é suportado pelo navegador.");
          }
      };

      const stopCamera = () => {
    if (mediaStream.value) {
        mediaStream.value.getTracks().forEach(track => track.stop());
    }
};


      onMounted(startCamera);
      onBeforeUnmount(() => {
            stopCamera();
        });
        const captureImage = () => {
  if (video.value) {
    const canvas = document.createElement("canvas");
    canvas.width = video.value.videoWidth;
    canvas.height = video.value.videoHeight;
    const context = canvas.getContext("2d");

    // Desenhar a imagem da webcam no canvas
    context.drawImage(video.value, 0, 0, canvas.width, canvas.height);

    // Adicionar o timestamp
    const timestamp = new Date().toLocaleString(); // ou formatar a data/hora como preferir
    context.font = "60px Arial"; // ajuste o tamanho e o tipo da fonte conforme necessário
    context.fillStyle = "white"; // cor do texto
    context.fillText(timestamp, 10, canvas.height - 20); // ajuste a posição conforme necessário

    // Criar blob da imagem com timestamp
    canvas.toBlob((blob) => {
      imageUrl.value = URL.createObjectURL(blob);
      const propertyName = `foto_${photoType.value}`;
      data.value[propertyName] = imageUrl.value; 
    }, "image/jpeg", 1);
  }
};  const  salvarImagem = async () => {
      console.log(data.value)
      const blobURL = imageUrl.value;
fetch(blobURL)
  .then(response => response.blob())
  .then(blob => {
    const file = new File([blob], 'imageFileName.jpg', { type: blob.type });
    // Agora você tem um objeto de arquivo que pode enviar via Axios
    sendFileToApi(file);
  });

      };

      const sendFileToApi = async (file) => {
  let formData = new FormData();
  formData.append('image', file);
  formData.append('os_number',data.value.codigo_estoklus)

  axios.post('https://app.watchtime.com.br/api/service_orders/fotos', formData)
  .then(response => {
    Notify.create({
              type: 'positive',
              message: `Foto Salva`
            });
            imageUrl.value = ''
  })
  .catch(error => {
    console.error('There was an error uploading the file:', error);
  });
}
const CustomUpload = async (files) => {
      // criar uma instância FormData
      const formData = new FormData();

      // adicionar cada arquivo ao FormData
      files.forEach((file, index) => {
        formData.append(`image`, file);
      });

      // adicionar outros parâmetros ao FormData se necessário
      formData.append('os_number', data.value.codigo_estoklus);

      // usar o Axios para enviar o FormData
      return axios
        .post('https://app.watchtime.com.br/api/service_orders/fotos', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then(response => {
          // tratar a resposta da API
          // se o upload foi bem sucedido, resolver a Promise
          // caso contrário, rejeitar a Promise
          if (response.status === 200) {
            Notify.create({
              type: 'positive',
              message: `Fotos Salvas`
            });
          } else {
            return Promise.reject(new Error('Upload falhou'));
          }
        })
        .catch(error => {
          // tratar erros de rede ou outros erros
          return Promise.reject(error);
        });
      }
const handleFileUpload = (event) => {
      this.file = event.target.files[0];
      console.log(this.file)
    }

    return { data,useQuasar, mediaStream,video, imageUrl, captureImage, salvarImagem,sendFileToApi, Notify,handleFileUpload,CustomUpload };
  },
};


  </script>
  

