import paho.mqtt.client as mqtt

def process_video(client, userdata, message):
    print(message.payload)

# set up MQTT communication
client = mqtt.Client("box")

# register all callbacks during initialisation
client.message_callback_add("device/video", process_video)

client.connect("192.168.1.23")
client.subscribe("device/#", 2)
client.loop_forever()
