import os
import datetime
import paho.mqtt.client as mqtt
import paramiko
from pymediainfo import MediaInfo
from omxplayer.player import OMXPlayer

splash_video = 'fulgur_intro.mp4'
cwd = '/home/pi/Video/' # current working directory (last '/' is required)
host = '192.168.1.23'

if !os.exists(cwd):
    os.mkdir(cwd)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username='pi', password = 'cntgfyrbpbv')
sftp = ssh.open_sftp()

if !os.path.isfile(cwd + splash_video):
    sftp.get('/' + splash_video, cwd + splash_video)

# dirty fucking trick to have player instance (impossible to create empty player instace)
player = OMXPlayer(cwd + splash_video, pause=True)

def process_video(client, userdata, message):
    file_name = str(message.payload, 'utf-8')
    print("Requested video {0}".format(file_name))
    sftp.get('/' + file_name, cwd + file_name, callback=lambda d, t : print('Transferred: {0:3.2f}%'.format(100 * (d/t)), end='\r'))

    # reading video duration
    info = MediaInfo.parse(cwd + file_name)
    print("Downloaded {0} with duration {1}".format(file_name, datetime.timedelta(milliseconds=info.tracks[0].duration)))

    # play video
    player.load(cwd + file_name)

# set up MQTT communication
client = mqtt.Client("box")

# register all callbacks during initialisation
client.message_callback_add("device/video", process_video)

client.connect(host)
client.subscribe("device/#", 2)
client.loop_forever()
