#!/usr/bin/env python
# coding: utf-8

# # Analyzing Audio Data
# 
# I have always been interested how programms determine a frequency from a sound wave it recieves and I have always
# wanted to create a programm to detect audio signals and convert them to musical notes. In this project I would be creating an app where users can insert a sequence of notes, record a phrase and the programm would determin how accurate the phrase was.
# 
# ## Main Technologies used:
# - python language
# - pyaudio
# - numpy
# - kivy
# - matplotlib
# 
# 
# ## Process:
# 1. Recieving audio
# 2. Processing and visualising audio
# 3. Converting audio to Frequency
# 4. Frequency to Notes
# 5. CSV file
# 6. Sample Audio data analysis

# ## Importing packages:

# In[19]:



import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
import time
import struct
import sys
import time
import soundfile
import audioop
import math
import random


# ## (Part 1) Recieving audio:
# First step of this project is being able to 
# 

# In[2]:


def record():
    chunk = 1024 * 4 # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    filename = "output.wav"	

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True)
        
    frames = []  # Initialize array to store frames

    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    start_time = time.time()
    # Store data in chunks for 5 seconds
    while time.time() < start_time + 5:
        data = stream.read(chunk, exception_on_overflow = False) 
        frames.append(data)
        
    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Finished recording')

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    
record()


# In[3]:


CHUNK = 5000
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        frames_per_buffer=CHUNK,
        input=True)


# ## (Part 2) Processing and visualising audio:

# In[5]:


fig, (ax1)  = plt.subplots(1)

x = np.arange(0, 2 * CHUNK, 2)

line, = ax1.plot(x,np.random.rand(CHUNK))


ax1.set_title('AUDIO WAVEFORM')
ax1.set_ylabel('magnitude')
ax1.set_ylim(0, 500)
ax1.set_xlim(0, CHUNK)
plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])


start_time = time.time()

while time.time() < start_time + 15:
    data = stream.read(CHUNK, exception_on_overflow = False) 
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b') 


    plt.pause(0.001)
    fig.canvas.draw()
    fig.canvas.flush_events()
    
    line.set_data(np.arange(len(data_int)),abs(data_int))
        


# 

# ## (Part 3) FFT

# In[15]:


wf = wave.open(r"/Users/idanlau/Desktop/python/pyaudio/output.wav","rb")  

while True:
    try:
        data = wf.readframes(CHUNK) 
        data_int = np.array(struct.unpack(str(2*CHUNK) + 'B', data), dtype='b')
        print(np.fft.fft(data_int))
                
    except struct.error:
        pass
        break            
    
    


# ## (Part 3) FFT values to hertz

# In[17]:


wf = wave.open(r"/Users/idanlau/Desktop/python/pyaudio/output.wav","rb")  
while True:
    try:
        data = wf.readframes(CHUNK) 
        data_int = np.array(struct.unpack(str(2*CHUNK) + 'B', data), dtype='b')
        print(np.fft.fft(data_int))          
        w = np.fft.fft(data_int)
        freqs = np.fft.fftfreq(len(w))
        idx = np.argmax(np.abs(w))
        freq = freqs[idx]
        freq_in_hertz = abs(freq * RATE)
        print(freq_in_hertz)
        
    
    except struct.error:
        pass
        break            

    


# ## (Part 4) Converting frequency to notes

# In[23]:


d_notes = []
accuracy = []
decibel_l = []


def run():

	p = pyaudio.PyAudio() 
	CHUNK = 6000 # Record in chunks of 1024 samples
	sample_format = pyaudio.paInt16  # 16 bits per sample
	channels = 1
	RATE = 44100  # Record at 44100 samples per second


	wf = wave.open(r"/Users/idanlau/Desktop/python/pyaudio/output.wav","rb")  

	p = pyaudio.PyAudio()

	stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
			channels = wf.getnchannels(),
			rate = wf.getframerate(),
			output = True)


	# open stream based on the wave object which has been input.


	for i in range (50):
		data = wf.readframes(CHUNK) 
		try:

			rms = audioop.rms(data,2)
			decibel = 20 * math. log10(rms)
			
			data_int = np.array(struct.unpack(str(2*CHUNK) + 'B', data), dtype='b')

			
			w = np.fft.fft(data_int)
			freqs = np.fft.fftfreq(w.size) 
			idx = np.argmax(abs(w))
			#if (idx > 1000 and idx <= 4096):
				#idx = 4096-idx
			freq = freqs[idx]
			freq_in_hertz = int(abs(freq*RATE))*2
			
			if(freq_in_hertz < 8000 and freq_in_hertz > 100 and decibel>50 ):
				Note,acc = findnote(freq_in_hertz)
				#print(Note)
				d_notes.append(Note)
				accuracy.append(acc)
				decibel_l.append(decibel)

		except struct.error:
			pass
			break

	print(d_notes)
	print(decibel_l)
	return d_notes,accuracy



def findnote(freq):
	print(freq)
	notes = {'C':16.35,'C#':17.32,'D':18.35, 'D#':19.45, 'E':20.60, "F":21.83, "F#":23.12, 
	"G":24.50, "G#":25.96,"A":27.50,"A#":29.14,"B":30.87}

	interval = [0,16.35,32.70,65.41,130.81,261.63,523.25,1046.50,2093.00,4186.01]

	note_list = []

	closest = 100000000000

	mul = 0

	result = "None"

	comp = 0

	#find range of note using if statement
	n = 0

	if freq > 4186.01:
		mul = 8
		n = 9


	else:

		for n in range (len(interval)):
			if(interval[n] > freq):
				mul = n-2
				break


		
	for key in notes.keys():

		note = ((notes[key]*np.power(2,abs(mul))))

		if (freq > note):
			if ((int(freq) % note) < closest):
				closest = int(freq) % note
				note_list.append(key)

		else:

			if ((note % int(freq)) < closest):
				closest = note % int(freq)
				note_list.append(key)

	result = note_list[len(note_list)-1]	

	comp = notes.get(result)*np.power(2,abs(mul))


	#print(closest)		

	if ((interval[n] % int(freq)) < closest):
		closest = (interval[n] % int(freq))
		note_list.append('C')
		comp = interval[n]	 

	#print(str(freq)+": "+str(comp))	
	try:		
		
		acc = (1-(abs(freq-comp)/comp))*100
		#print(acc)
	

	except IndexError:
		pass	



	return result,acc

    
run()    


# In[ ]:





# In[ ]:





# In[ ]:




