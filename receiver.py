import paho.mqtt.client as mqtt

client = mqtt.Client("box")

def process_video_upload(client, userdata, message):
    print("Hue!")
    #print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    #print("message qos=",message.qos)

# register all callbacks during initialisation
client.message_callback_add("device/video", process_video_upload)

client.connect("192.168.1.23")
client.subscribe("device/#")
client.loop_forever()
