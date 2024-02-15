<template>
    <div class="video-player-container">
      <video controls :src="videoUrl"></video>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      videoUrl: String
    }
  }
  </script>
  
  <style scoped>
  .video-player-container {
    position: relative;
    padding-bottom: 42.25%; /* Proporção 16:9 (56.25% = 9 / 16 * 100) */
    height: 0;
    overflow: hidden;
  }
  
  .video-player-container video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
  </style>
  