<template>
  <div class="wrapper">
    <div id="app">
      <p>Savanna Trace 2.0</p>
      <MqttSubscriber />
    </div>
  </div>
</template>

<script>
import MqttSubscriber from './components/MqttSubscriber.vue';

export default {
  components: {
    MqttSubscriber,
  },
};
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
</style>