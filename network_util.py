import datetime, time, json
import socket
import paho.mqtt.client as mqtt

# MQTT broker
id = '1'
client_name = 'ST_device' + id
broker_host = 'wss://mqtt-dashboard.com/mqtt' #'broker.emqx.io' 
broker_port = 8884 # 1883
# Topics 
title = f'Network notification for {client_name}'
ip_topic = f'/stats/notifications/{client_name}/network'
publish_delay = 5
# Network monitoring
lost_connection = got_connection = ''
reconnect_delay = 3
retries = 0
connected = False

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
    
# Set up MQTT client and connect to broker
client = mqtt.Client(client_name)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(broker_host, broker_port)

if __name__ == '__main__':
    while True:
        client.loop()
        # IP address
        ip_wifi = socket.gethostbyname(socket.gethostname())
        # Topic message to publish in JSON format
        ip_message = {
            'topic': ip_topic,
            'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'ipWifi': ip_wifi
        } 
        client.publish(ip_topic, json.dumps(ip_message))
        time.sleep(publish_delay)
        # Retry segment
        if not connected:
            try:
                time.sleep(reconnect_delay)
                retries = retries + 1
                client.reconnect()
                print("Reconnected!")
            except:
                print(f'Reconnection attempt {retries} failed')
        time.sleep(1)
    

