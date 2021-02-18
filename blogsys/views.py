from django.shortcuts import render
from django.http import HttpResponseBadRequest
from blogsys.models import PostQ
from .forms import PostQform



def home(request):
    if request.method =='POST':
        form = PostQform(request.POST)

        if form.is_valid():

            print(form.cleaned_data.get('Name'))
            saverecord=PostQ()
            saverecord.postname=form.cleaned_data.get('Name')
            saverecord.text=form.cleaned_data.get('Message')
            saverecord.save()



            return render(request, 'blogsys/bloglog_submit.html', {"form":saverecord})

        else:

            return HttpResponseBadRequest()
    else:
        form = PostQform()
        return render(request, 'blogsys/bloglog.html', {"form": form})









