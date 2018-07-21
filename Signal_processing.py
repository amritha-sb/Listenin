import RPi.GPIO as GPIO

from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
#import numpy as np
 
import wave
 
import struct
from scipy.io import wavfile
import pyaudio
#!/usr/bin/python
import requests
import getpass
from lxml import html
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#row 4
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)#row 3
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)#row 2
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)#row 1
GPIO.setup(24, GPIO.OUT)  #coloumn3
GPIO.setup(25, GPIO.OUT)#column1
GPIO.setup(18, GPIO.OUT)#column2
GPIO.setup(21, GPIO.OUT) 
GPIO.output(21, 1)
m=[[1,2,3],[4,5,6],[7,8,9],[11,0,12]]
r=[22,27,17,23]
c=[24,25,18]
k=0


# instantiate lcd and specify pins
'''lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)
lcd.clear()'''
# display text on LCD display \n = new line
def displayresult(prediction):
    lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)
    lcd.clear()
    # display text on LCD display \n = new line
    lcd.message(prediction)
    sleep(.3)
    # scroll text off display
    '''for x in range(0, 16):
      lcd.move_right()
      sleep(.1)
    sleep(3)
    # scroll text on display 
    for x in range(0, 16):
      lcd.move_left()
      sleep(.1)'''

    sleep(.3)
    #lcd.clear()

def getusername(a):
    k=0;
    qt=['_','_','_','_','_','_','_','_']
    #for i in range(a):
        #username[a]='_'
    while True:
        for i in range(3):
            GPIO.output(c[i], 0)
            for j in range(4):
                button_state = GPIO.input(r[j])
                #print button_state
                if button_state == False:
                    #GPIO.output(24, True)
                    print k
                    print m[j][i],r[j],c[i],GPIO.input(r[j])
                    if j==0:
                        qt[k]='a'
                    elif j==1:
                        qt[k]='b'
                    elif j==2:
                        qt[k]='c'
                    elif j==3:
                        qt[k]='d'                        
                    k=k+1
                    print qt
                    #lcd.clear()
                    displayresult(qt)
                    #sleep(3)
                    sleep(0.1)
                    #print('Button Pressed...')
                    while(GPIO.input(r[j])==0):
                        pass
                    #time.sleep(0.2)
                #else:
                    #GPIO.output(24, False)
        if k==8:
            break;
    return ''.join(qt)

def graph_spectrogram(data):
    #rate, data = get_wav_info(wav_file)
    nfft = 256  # Length of the windowing segments
    fs = 256    # Sampling frequency
    pxx, freqs, bins, im = plt.specgram(data, nfft,fs)
    plt.axis('off')
    plt.savefig('trial1.png',
                dpi=100, # Dots per inch
                frameon='false',
                aspect='normal',
                bbox_inches='tight',
                pad_inches=0) # Spectrogram saved as a .png
    plt.show()
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
base_url = "http://93b65eb0.ngrok.io/"
#http://0e98178c.ngrok.io/

session_requests = requests.session()

#print ("connecting...")
displayresult("connecting...")
login_url = base_url + "account/login/"
#print login_url

result = session_requests.get(login_url)
#print "Status: " + str(result.status_code)
displayresult("Status: " + str(result.status_code))
tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]

#username = raw_input("Username: ")
displayresult("Username: ")
username=getusername(8)
print username
displayresult("Password: ")
#password = getpass.getpass()
password=getusername(8)
print password

payload = {
    "username": username, 
    "password": password, 
    "csrfmiddlewaretoken": authenticity_token
}

result = session_requests.post(
    login_url, 
    data = payload, 
    headers = dict(referer=login_url)
)


displayresult("Status: " + str(result.status_code))
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 16384
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file09.wav"
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
#print "recording..."
displayresult("recording..")
frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
#print "finished recording"
displayresult("finished")
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

infile = "file09.wav"
outname="filtered.wav"
wav_file = wave.open(infile, 'r')
frame_rate=wav_file.getframerate()
sampWidth=wav_file.getsampwidth()
nchannels=wav_file.getnchannels()
num_samples=wav_file.getnframes()
data = wav_file.readframes(num_samples)
wav_file.close()
k=len(data)
#print k
#print frame_rate
#print num_samples
#print wav_file.getsampwidth()
data = struct.unpack('{n}h'.format(n=k/2), data)
data = np.array(data)
#print data	
data_fft = np.fft.fft(data)#generates complex domain frequencies (Fast fourier Transform))

frequencies = np.abs(data_fft)#finds the modulus of it whic are the real frequency! phew
#print("The frequency is {} Hz".format(np.argmax(frequencies))) #prints the highest frequency! because the other frequency are not perfectly 0
#print len(frequencies)	
 
#plt.show()# Filter requirements.
order = 6
fs = frame_rate # sample rate, Hz
cutoff = 300  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, worN=8000)

y = butter_lowpass_filter(data, cutoff, fs, order)
graph_spectrogram(y)

if result.status_code == 200:
    #print "Logged in"
    displayresult("Logged in")
    url = base_url
    result = session_requests.get(url)

    #file_name = raw_input("Enter the spectrogram file name: ")
    file_name = '/home/pi/Desktop/trial1.png'
    #val = input("Enter the spectrogram result (1 for positive, 0 for negative):")
    val = 0
    if val == 1:
        spectrogram_result = True
    else:
        spectrogram_result = False

    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]


    payload = {
        "csrfmiddlewaretoken": authenticity_token,
        "result": spectrogram_result
    }

    with open(file_name, 'rb') as image_file:
        files = {
            "image": image_file,
        }

        result = session_requests.post(
            url,
            data=payload,
            files=files,
            headers=dict(referer=url)
        )

        print "Status: " + str(result.status_code)
        if result.status_code == 200:
            #print "Spectrogram submitted"
            displayresult("DONE")

       
         
