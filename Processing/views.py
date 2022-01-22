from django.shortcuts import render,redirect,reverse
import pyaudio
import wave
import audioop
import math
import numpy as np
import struct

import librosa
import soundfile as sf
from pydub import AudioSegment

from .forms import ConvertForm
from .models import Audio,File

import os

# Create your views here.
def processAudio(file):
    x, _ = librosa.load(file, sr=16000)

    sf.write('tmp.wav', x, 16000)

    # sf.write('1.wav', x, 16000)
    CHUNK = 6000  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    RATE = 44100  # Record at 44100 samples per second
    wf = wave.open('tmp.wav', "rb")
    d_notes = []
    accuracy = []
    decibel_l = []

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # open stream based on the wave object which has been input.

    for i in range(50):
        data = wf.readframes(CHUNK)
        try:

            rms = audioop.rms(data, 2)
            decibel = 20 * math.log10(rms)

            data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')

            w = np.fft.fft(data_int)
            freqs = np.fft.fftfreq(w.size)
            idx = np.argmax(abs(w))
            freq = freqs[idx]
            freq_in_hertz = int(abs(freq * RATE)) * 2

            if (freq_in_hertz < 8000 and freq_in_hertz > 100 and decibel > 50):
                Note, acc = findnote(freq_in_hertz)
                # print(Note)
                d_notes.append(Note)
                accuracy.append(acc)
                decibel_l.append(decibel)

        except struct.error:
            pass
            break

    a = Audio.objects.create(d_notes=d_notes,accuracy=accuracy,decibel_l=decibel_l)
    # print(d_notes)
    # print(decibel_l)
    # return d_notes, accuracy
    print("DONE")
    #print(a.id)
    print(reverse('results', kwargs={'id':  a.id}))
    return a.id



def findnote(freq):
    print(freq)
    notes = {'C': 16.35, 'C#': 17.32, 'D': 18.35, 'D#': 19.45, 'E': 20.60, "F": 21.83, "F#": 23.12,
             "G": 24.50, "G#": 25.96, "A": 27.50, "A#": 29.14, "B": 30.87}

    interval = [0, 16.35, 32.70, 65.41, 130.81, 261.63, 523.25, 1046.50, 2093.00, 4186.01]

    note_list = []

    closest = 100000000000

    mul = 0

    result = "None"

    comp = 0

    # find range of note using if statement
    n = 0

    if freq > 4186.01:
        mul = 8
        n = 9


    else:

        for n in range(len(interval)):
            if (interval[n] > freq):
                mul = n - 2
                break

    for key in notes.keys():

        note = ((notes[key] * np.power(2, abs(mul))))

        if (freq > note):
            if ((int(freq) % note) < closest):
                closest = int(freq) % note
                note_list.append(key)

        else:

            if ((note % int(freq)) < closest):
                closest = note % int(freq)
                note_list.append(key)

    result = note_list[len(note_list) - 1]

    comp = notes.get(result) * np.power(2, abs(mul))

    # print(closest)

    if ((interval[n] % int(freq)) < closest):
        closest = (interval[n] % int(freq))
        note_list.append('C')
        comp = interval[n]

    # print(str(freq)+": "+str(comp))
    try:

        acc = (1 - (abs(freq - comp) / comp)) * 100
    # print(acc)

    except IndexError:
        pass

    return result, acc



import pathlib
from django.http import FileResponse

def convert(request):

    try:
        # convert wav to mp3
        form = ConvertForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():

                src = request.FILES['file']
                dst = "test.wav"
                sound = AudioSegment.from_mp3(src)
                sound.export(dst, format="wav")
                file_server = pathlib.Path(os.path.abspath(dst))
                file_to_download = open(str(file_server), 'rb')

                response = FileResponse(file_to_download, content_type='application/force-download')
                response['Content-Disposition'] = 'inline; filename="a_name_to_file_client_hint.wav"'
                return response

            else:
                print(form.errors)
            return redirect("/")
    except RuntimeError:
        return redirect("/convert/")
    return render(request,'Home/convert_view.html',{"form":form})

