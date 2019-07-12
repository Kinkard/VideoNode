import paho.mqtt.client as mqtt

client = mqtt.Client("box")
client.connect("192.168.1.23")

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)

client.subscribe("device/video")
client.on_message=on_message
client.loop_forever()
