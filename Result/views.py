from django.shortcuts import render,HttpResponse
from Processing.models import Audio
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv



# Create your views here.
def show(request,id):
    obj = Audio.objects.get(id = id)

    response = HttpResponse(content_type='image/png')


    obj.d_notes = obj.d_notes.replace("'","")

    d_notes = obj.d_notes.strip('[]').split(', ')
    d_notes = list(d_notes)
    print(d_notes)



    obj.accuracy = obj.accuracy.replace("'","")

    accuracy = obj.accuracy.strip('[]').split(', ')
    accuracy = list(accuracy)
    print(accuracy)


    obj.decibel_l = obj.decibel_l.replace("'","")

    decibel_l = obj.decibel_l.strip('[]').split(', ')
    decibel_l = list(decibel_l)
    print(decibel_l)

    header = ['notes', 'accuracy', 'decible']

    with open('result.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for i in range(len(d_notes)):
            writer.writerow([d_notes[i], accuracy[i],decibel_l[i]])



    return render(request, 'Result/result_view.html', {
        'accuracy': accuracy,
        'd_notes': d_notes,
        #'colors': ["#FF4136", "#0074D9"],
    })

