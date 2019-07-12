import paho.mqtt.client as mqtt

client = mqtt.Client("box")

file_name = None
file = None
def process_video_upload(client, userdata, message):
    global file_name
    global file
    if file_name is None:
        file_name = str(message.payload.decode("utf-8")).split(':')[0]
        file = open(file_name, "wb") # open file for write in binary mode
    elif len(message.payload) == 0:
        print("Received file " + file_name)
        file_name = None
        file.close()
    else:
        file.write(message.payload)

# register all callbacks during initialisation
client.message_callback_add("device/video", process_video_upload)

client.connect("192.168.1.23")
client.subscribe("device/#", 2)
client.loop_forever()
