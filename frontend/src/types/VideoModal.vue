<template>
    <q-dialog>
      <q-card style="width: 90%;">
        <q-card-section>
          <h5>{{data.nome}}</h5>
          <p style="padding: 2px; margin-top: 16px;">{{data.descricao}}</p>
        </q-card-section>
              <q-card-section class="">
          <div class="">
            <div>
              <VideoPlayer :videoUrl="data.id" />
            </div>
          </div>
          <q-space />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Fechar" color="primary" v-close-popup 
          @click="fecharModal"/>
        </q-card-actions>
  
      </q-card>
    </q-dialog>
  </template>
  
  <script setup>
  import VideoPlayer from '@/components/VideoPlayer/VideoPlayer.vue';
  import { ref, defineProps } from "vue";
  
  const { data, value } = defineProps(["data", "value"]);
  
  
  
  </script>
  
  
  
  
  
  
  