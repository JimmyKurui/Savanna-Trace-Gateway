<template>
  <div id="app">
    <MqttSubscriber />
  </div>
</template>

<script>
import MqttSubscriber from '@/components/MqttSubscriber.vue';

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