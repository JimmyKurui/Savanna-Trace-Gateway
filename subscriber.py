import datetime, time, json
import paho.mqtt.client as mqtt

# MQTT broker
id = '2'
client_name = 'ST_device' + id
broker_host = 'broker.emqx.io'
broker_port = 1883
# Topics 
title = 'Network statistics for {}'.format(client_name)
ip_topic = '/stats/notifications/ST_device1/network'

# Network monitoring
lost_connection = got_connection = ''
reconnect_delay = 3
retries = 0
connected = False
response = None
# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    global got_connection, connected
    if rc == 0:
        print('Connected to MQTT broker!')
        connected = True
    else:
        print('Failed to connect to MQTT broker')

def on_disconnect(client, userdata, rc):
    global lost_connection, connected, retries
    print('Disconnected from MQTT broker!')
    connected = False

def on_message(client, userdata, message):
    global response
    payload_dict = {"topic": message.topic}
    payload_dict.update(json.loads(message.payload.decode()))  
    response = payload_dict
    print(response)

# Set up MQTT client and connect to broker
client = mqtt.Client(client_name)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(broker_host, broker_port)

client.subscribe(ip_topic)

if __name__ == '__main__':
    while True:
        client.loop()
        # Retry Section
        if not connected:
            try:
                time.sleep(reconnect_delay)
                retries = retries + 1
                client.reconnect()
            except:
                print(f'Reconnection attempt {retries} failed')
        time.sleep(1)

