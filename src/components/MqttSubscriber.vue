<template>
  <div>
    <button @click="connectToMQT">Connect to MQTT Broker</button>
    <button @click="disconnectMQTT">Disconnect</button> 
  </div>
  <div>
    <p v-if="client.connected">Connected to MQTT broker!</p>
    <p v-else>Failed to connect to MQTT broker</p>
    <p v-if="receiveNews">Received message: {{ receiveNews }}</p>
  </div>
</template>

<script>
import mqtt from "precompiled-mqtt";
import { ref, reactive } from "vue";

export default {
  setup() {
    const connection = reactive({
      protocol: "mqtt",
      host: "broker.emqx.io",
      port: 1883,
      endpoint: "",
      clean: true,
      connectTimeout: 3000 * 1000, // ms
      reconnectPeriod: 3000, // ms
      clientId: "ST_client2",
      username: "",
      password: "",
    });

    const subscription = ref({
      topic: "/stats/notifications/ST_client1/network",
      qos: 0,
    });

    const receiveNews = ref("");
    // const qosList = [0, 1, 2];
    const client = ref({
      connected: false,
    });
    const subscribeSuccess = ref(false);
    const connecting = ref(false);
    let retryTimes = 0;

    const initData = () => {
      client.value.connected = false;
      retryTimes = 0;
      connecting.value = false;
      subscribeSuccess.value = false;
    };

    const handleOnReConnect = () => {
      retryTimes += 1;
      if (retryTimes > 5) {
        try {
          client.value.end();
          initData();
          console.error(`Connection maxReconnectTimes - ${retryTimes} limit, stopping retry`);
        } catch (error) {
          console.error(error.toString());
        }
      }
    };

    const createConnection = () => {
      try {
        connecting.value = true;
        const { protocol, host, port, endpoint, ...options } = connection;
        const connectUrl = `${protocol}://${host}:${port}${endpoint}`;
        client.value = mqtt.connect(connectUrl, options);
        if (client.value.on) {
          client.value.on("connect", () => {
            connecting.value = false;
            console.log("Connection succeeded!");
          });
          client.value.on("reconnect", handleOnReConnect);
          client.value.on("error", (error) => {
            console.log("Connection failed", error);
          });
          client.value.on("message", (topic, message) => {
            receiveNews.value = receiveNews.value.concat(message);
            console.log(`Received message ${message} from topic ${topic}`);
          });
        }
      } catch (error) {
        connecting.value = false;
        console.error("mqtt.connect error", error);
      }
    };

    const doSubscribe = () => {
      const { topic, qos } = subscription;
      client.value.subscribe(topic, { qos }, (error, res) => {
        if (error) {
          console.error("Subscribe to topics error", error);
          return;
        }
        subscribeSuccess.value = true;
        console.log("Subscribe to topics res", res);
      });
    };

    const destroyConnection = () => {
      if (client.value.connected) {
        try {
          client.value.end(false, () => {
            initData();
            console.log("Successfully disconnected!");
          });
        } catch (error) {
          console.log("Disconnect failed", error.toString());
        }
      }
    };

    const connectToMQTT = () => {
      initData();
      createConnection();
      doSubscribe();
    };

    const disconnectMQTT = () => {
      destroyConnection();
    };

    return {
      connection,
      receiveNews,
      client,
      subscribeSuccess,
      connecting,
      connectToMQTT,
      disconnectMQTT,
    };
  },
};
</script>

<style scoped>

</style>