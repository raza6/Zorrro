#IMPORTS
import PySimpleGUI as sg
from bs4 import BeautifulSoup as bs
import youtube_dl, requests, os, sys, re, eyed3, subprocess

loop = False
modePlaylist = False
inputValues = []

def init():
    #Test youtube-dl version
    if(len(sys.argv) > 1 and "--ignore" in sys.argv):
        pass
    else:
        print("Checking up Youtube-dl version, it may take up to a few seconds")
        response = requests.get("https://youtube-dl.org/")
        if response.status_code == 200:
            ytdlhtml = bs(response.content, 'html.parser')
            utdref = ytdlhtml.find_all("div", "latest")[0].contents[0].contents[1][3:13]
            utdcur = subprocess.check_output(['youtube-dl', '--version']).decode().rstrip()
            if(utdcur == utdref):
                print("Youtube-dl is up-to-date")
            else:
                print("Youtube-dl is not up-to-date, the latest version is " + utdref + ".\nRun 'pip3 install --upgrade youtube-dl' or launch with --ignore if you're feeling lucky, u punk")
                exit()
    
    if(len(sys.argv) > 1 and "--loop" in sys.argv):
        global loop
        loop = True

def startZorro():
    #IHM INIT
    sg.theme('DarkGrey5')

    layoutForm = [  [sg.Text('URL    ', font='Consolas'), sg.In(key=1)],
                [sg.Text('Album  ', font='Consolas'), sg.In(key=2)],
                [sg.Text('Artiste', font='Consolas'), sg.In(key=3)],
                [sg.Text('Cover  ', font='Consolas'), sg.In(key=4)],
                [sg.Text('Titre  ', font='Consolas'), sg.In(key=5)],
                [sg.Button('Ok'), sg.Button('Annulette')] ]

    #Prompt window
    window = sg.Window('Zorrro', layoutForm)
    while True:
        event, values = window.read()
        if event in (None, 'Ok'):
            global inputValues
            inputValues = values.copy()
            break
        elif event in ('Annulette'):
            exit()

    window.close()

    #Move in the dl folder
    while "dl" in os.getcwd():
        os.chdir("..")
    if not os.path.exists("dl"):
        os.mkdir("dl")
    os.chdir("dl")
    
    global modePlaylist
    modePlaylist = "playlist" in inputValues[1]

    ytdl_opts = {
        'noplaylist': 'False' if modePlaylist else 'True',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': YtdlLogger(),
        'outtmpl': '%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
        ytdl.download([inputValues[1]])
    
#Set all tags
def normalize():
    tobetag = os.listdir(".")
    for file in tobetag:
        if("mp3" in file):
            #Set album and artist tags
            filt = eyed3.load(file)
            if(filt.tag.album == None):
                filt.tag.album = "Autres" if (inputValues[2] == "") else inputValues[2]
                filt.tag.artist = "" if (inputValues[3] == "") else inputValues[3]
                #Set cover
                if inputValues[4] != "":
                    mimet = inputValues[4][-3:]
                    filt.tag.images.remove('')
                    response = requests.get(inputValues[4], stream=True)
                    if response.status_code == 200:
                        filt.tag.images.set(type_=3, img_data=response.content, mime_type="image/" + mimet, description=u'')
                filt.tag.save()
                #Rename file
                if inputValues[5] != "":
                    if(modePlaylist):
                        result = re.search(inputValues[5], file[:len(file)-4])
                        title = result.group(1).lower().capitalize()
                        os.rename(file, title + ".mp3")
                    else:
                        os.rename(file, inputValues[5] + ".mp3")
    
    #Exit window
    layoutEnd = [  [sg.Text('Done !')], [sg.Button('Ok')]  ]
    
    window = sg.Window('Zorrro', layoutEnd)
    while True:
        event, _ = window.read()
        if event in (None, 'Ok'):
            break
    window.close()
    if(loop):
        startZorro()

class YtdlLogger(object):
    def info(self, msg):
        print("i " + msg)
    
    def debug(self, msg):
        if("ffmpeg" in msg):
            print("Start mp3 conversion")
        elif("Destination" in msg):
            print("Start downloading of " + msg[24:])
        if(modePlaylist):
            if("Finished downloading playlist" in msg):
                normalize()
        else:
            if("Deleting" in msg):
                normalize()

    def warning(self, msg):
        print("w " + msg)

    def error(self, msg):
        print("e " + msg)

init()
startZorro()

exit()