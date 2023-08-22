<template>
  <div>
    <button @click="createConnection()">Connect</button>
    <button @click="destroyConnection()">Disconnect</button>
  </div>
  <div>
    <p v-if="client.connected">Connected to MQTT broker!</p>
    <p v-else>Disconnected</p>
    <p v-if="receivedMessages">Received message: {{ receivedMessages }}</p>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import mqtt from "precompiled-mqtt";

// Network variables
const connection = reactive({
  protocol: "ws",
  host: "mqtt.eclipseprojects.io",
  // ws -> 8083; wss -> 8084
  port: 80,
  endpoint: '/mqtt',
  clientId: "ST_client2",
  username: "",
  password: "",
  clean: true,
  connectTimeout: 600 * 1000, // ms
  reconnectPeriod: 4000, // ms
});

// topic & QoS for MQTT subscribing
const subscription = reactive({
  topic: "/stats/notifications/ST_device1/network",
  qos: 0,
});

// topic, QoS & payload for publishing message
const client = reactive({
  connected: false,
});
const subscribedSuccess = ref(false);
let receivedMessages = ref(null);
let reconnectInterval;

// Reconnect every 5 seconds
const handleOnReconnect = () => {
  console.log("Connection lost. Reconnecting in 3 seconds...");
  clearInterval(reconnectInterval);
  reconnectInterval = setInterval(() => {
    console.log("Reconnecting...");
    destroyConnection();
    createConnection();
    clearInterval(reconnectInterval);
  }, 5000);

};


// create MQTT connection
const createConnection = () => {
    try {
      const { protocol, host, port, endpoint, ...options } = connection;
      const connectUrl = `${protocol}://${host}:${port}/${endpoint}`;
      // Connection
      console.log("Connecting...");
      client.value = mqtt.connect(connectUrl, options);

      // Callbacks
      if (client.value.on) {
        client.value.on("connect", () => {
          clearInterval(reconnectInterval);
          client.connected = true;
          console.log("connection successful");
          subscribe();
        });
        client.value.on("reconnect", handleOnReconnect);
        client.value.on("error", (error) => {
          console.log("connection error:", error);
        });
        client.value.on("message", (topic, message) => {
          receivedMessages.value = JSON.parse(message);
          console.log(`received message: ${message} from topic: ${topic}`);
        });
      }
    } catch (error) {
      console.log("mqtt.connect error:", error);
    }
};

// subscribe topic
const subscribe = () => {
  const { topic, qos } = subscription;
    client.value.subscribe(topic, { qos }, (error, granted) => {
        if (error) {
          console.log("subscribe error:", error);
          return;
        } 
        subscribedSuccess.value = true;
        console.log("subscribe successfully:", granted);
      });
};

// disconnect
// disconnect
const destroyConnection = () => {
  if (client.value && client.value.connected) {
    client.value.end();
    client.connected = false;
    receivedMessages = "";
    console.log("Disconnected successfully");
  }
};

</script>

<style>
.mqtt-demo {
  max-width: 1200px;
  margin: 32px auto 0 auto;
}

h1 {
  font-size: 16px;
  margin-top: 0;
}

.el-card {
  margin-bottom: 32px;
}
.el-card__body {
  padding: 24px;
}

.el-select {
  width: 100%;
}

.text-right {
  text-align: right;
}

.sub-btn {
  margin-top: 30px;
}
</style>