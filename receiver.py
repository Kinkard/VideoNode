import paho.mqtt.client as mqtt

client = mqtt.Client("box")

file_name = None
def process_video_upload(client, userdata, message):
    if file_name is None:
        file_name = str(message.payload.decode("utf-8"))
    elif len(message.payload) == 0:
        print("Received file " + file_name + " from " + str(client))
        file_name = None

# register all callbacks during initialisation
client.message_callback_add("device/video", process_video_upload)

client.connect("192.168.1.23")
client.subscribe("device/#", 2)
client.loop_forever()
