from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,reverse
from .forms import UploadFileForm
from Processing.views import processAudio

# Create your views here.
def homeView(request):

    try:
        if request.method == 'POST':
            form = UploadFileForm(request.POST or None, request.FILES or None)
            print(form['file'])
            if form.is_valid():
                id = processAudio(request.FILES['file'])
                return redirect(reverse('results', kwargs={'id': id}))
        else:
            form = UploadFileForm()
            return render(request, 'Home/home_view.html', {'form': form})
        return render(request,'Home/home_view.html', {'form': form})

    except RuntimeError:
        return redirect("/")