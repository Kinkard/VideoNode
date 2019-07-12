import paho.mqtt.client as mqtt

client = mqtt.Client("box")
client.connect("192.168.1.23")

counter = 0 # input messages counter
def on_message(client, userdata, message):
    counter += 1
    print(counter)
    #print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)

client.subscribe("device/video")
client.on_message=on_message
client.loop_forever()
