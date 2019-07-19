import datetime
import paho.mqtt.client as mqtt
import paramiko
from pymediainfo import MediaInfo

host = '192.168.1.23'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username='pi', password = 'cntgfyrbpbv')
sftp = ssh.open_sftp()

def process_video(client, userdata, message):
    file_name = str(message.payload, 'utf-8')
    print("Requested video {0}".format(file_name))
    sftp.get("/" + file_name, file_name, callback=lambda d, t : print('Transferred: {0:3.2f}%'.format(100 * (d/t)), end='\r'))

    # reading video duration
    info = MediaInfo.parse(file_name)
    print("Downloaded {0} with duration {1}".format(file_name, datetime.timedelta(milliseconds=info.tracks[0].duration)))

# set up MQTT communication
client = mqtt.Client("box")

# register all callbacks during initialisation
client.message_callback_add("device/video", process_video)

client.connect(host)
client.subscribe("device/#", 2)
client.loop_forever()
