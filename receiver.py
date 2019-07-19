import paho.mqtt.client as mqtt
import paramiko

def process_video(client, userdata, message):
    print(str(message.payload, 'utf-8'))

# set up MQTT communication
client = mqtt.Client("box")

# register all callbacks during initialisation
client.message_callback_add("device/video", process_video)

client.connect("192.168.1.23")
client.subscribe("device/#", 2)
client.loop_forever()
