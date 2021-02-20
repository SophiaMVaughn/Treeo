from django.shortcuts import render
from django.http import HttpResponseBadRequest
from blogsys.models import PostQ
from .forms import PostQform



def Health_Coach(request):
    if request.method =='POST':
        form = PostQform(request.POST)

        if form.is_valid():

            print(form.cleaned_data.get('Name'))
            save=PostQ()
            save.Name=form.cleaned_data.get('Name')
            save.Message=form.cleaned_data.get('Message')
            save.save()



            return render(request, 'blogsys/bloglog_submit.html', {"form":save})

        else:

            return HttpResponseBadRequest()
    else:
        form = PostQform()
        return render(request, 'blogsys/Health_Coach.html', {"form": form})




def provider(request):
    if request.method =='POST':
        form = PostQform(request.POST)

        if form.is_valid():

            print(form.cleaned_data.get('Name'))
            save=PostQ()
            save.Name=form.cleaned_data.get('Name')
            save.Message=form.cleaned_data.get('Message')
            save.save()



            return render(request, 'blogsys/bloglog_submit.html', {"form":save})

        else:

            return HttpResponseBadRequest()
    else:
        form = PostQform()
        return render(request, 'blogsys/provider.html', {"form": form})




def dietitian(request):
    if request.method =='POST':
        form = PostQform(request.POST)

        if form.is_valid():

            print(form.cleaned_data.get('Name'))
            save=PostQ()
            save.Name=form.cleaned_data.get('Name')
            save.Message=form.cleaned_data.get('Message')
            save.save()



            return render(request, 'blogsys/bloglog_submit.html', {"form":save})

        else:

            return HttpResponseBadRequest()
    else:
        form = PostQform()
        return render(request, 'blogsys/dietitian.html', {"form": form})

