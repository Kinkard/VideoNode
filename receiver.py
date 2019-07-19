import paho.mqtt.client as mqtt
import paramiko

host = "192.168.1.23"
transport = paramiko.Transport((host, 22))
transport.connect(username = "pi", password = "cntgfyrbpbv")
sftp = paramiko.SFTPClient.from_transport(transport)

def process_video(client, userdata, message):
    file_name = str(message.payload, 'utf-8')
    print("Requested video " + file_name)
    sftp.get("/" + file_name, file_name)
    print(file_name + " downloaded!")

# set up MQTT communication
client = mqtt.Client("box")

# register all callbacks during initialisation
client.message_callback_add("device/video", process_video)

client.connect(host)
client.subscribe("device/#", 2)
client.loop_forever()
