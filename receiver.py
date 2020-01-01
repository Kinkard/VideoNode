import os
import datetime
import paho.mqtt.client as mqtt
import paramiko
from pymediainfo import MediaInfo
from omxplayer.player import OMXPlayer

# script parameters
splash_video = 'splash.mov'
cwd = '/home/pi/Video/' # current working directory (last '/' is required)
host = '192.168.1.23'

if not os.path.exists(cwd):
    os.mkdir(cwd)

# SFTP server connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username='pi', password = 'cntgfyrbpbv')
sftp = ssh.open_sftp()

class DownloadVerbose:
    def __init__(self):
        self.prev_downloaded = 0
        self.prev_time = datetime.datetime.now()

    def __call__(self, downloaded, total):
        percent = 100.0 * (downloaded/total)
        time = datetime.datetime.now()
        speed_Bps = (downloaded - self.prev_downloaded) / (time - self.prev_time).total_seconds()
        speed_Mbps = speed_Bps / 2**17
        print('Transferred: {0:3.2f}%, {1:3.2f} Mbps'.format(percent, speed_Mbps), end='\r')
        self.prev_downloaded = downloaded
        self.prev_time = time

def download_file(file_name):
    if os.path.isfile(cwd + splash_video):
        sftp_size = sftp.stat('/' + file_name).st_size
        file_size = os.stat(cwd + file_name).st_size
        if file_size == sftp_size:
            return # file already downloaded

    print("Download video {0}".format(file_name))
    sftp.get('/' + file_name, cwd + file_name, callback=DownloadVerbose())

def process_video(client, userdata, message):
    file_name = str(message.payload, 'utf-8')
    download_file(file_name)

    # reading video duration
    info = MediaInfo.parse(cwd + file_name)
    print("Downloaded {0} with duration {1}".format(file_name, datetime.timedelta(milliseconds=info.tracks[0].duration)))

    # play video
    player.load(cwd + file_name)

# dirty fucking trick to have player instance (impossible to create empty player instace)
download_file(splash_video)
player = OMXPlayer(cwd + splash_video, pause=True)

# set up MQTT communication
client = mqtt.Client("box")

# register all callbacks during initialisation
client.message_callback_add("device/video", process_video)

client.connect(host)
client.subscribe("device/#", 2)
client.loop_forever()
