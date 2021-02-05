from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Fileform
from django.core.files.storage import FileSystemStorage
from .models import Uploaded_File





def render_file_upload(request):
    if request.method == 'POST':
        up_form = Fileform(request.POST, request.FILES)
        if up_form.is_valid():
            if request.FILES["file"].size <= 52428800:
                if len(request.FILES["file"].name) <= 100:
                #some logic ?????????
                    f=Uploaded_File()
                    f.usern=request.user
                    f.name = request.FILES["file"].name
                    f.file =request.FILES["file"]
                    f.save()
                    print(f,f.file,f.name,f.file)
                return render(request, 'file_upload_Compleate.html')
            else:
                context = {"errorMsg":"Too Big"}
                return render(request, 'file_upload_Failed.html', context)
        else:
            return render(request, 'file_upload_Failed.html')
    else:
        return render(request, 'fileupload.html')


def render_file_download(request):
    files = []
    # dr = {'key': 'value'}
    # dr['mynewkey'] = 'mynewvalue'
    #print(Uploaded_File.objects.all())
    # test = Uploaded_File.objects.get(id=i.id)
    for i in Uploaded_File.objects.all():
        files.append({
                'FileName': i.file_name,
                'Uploader': i.usern.username,
                'file': i.file.url,
                'date_uploaded': i.date_created
                'id': i.id
            })

    context = {
        'file_list': files
    }
    return render(request, 'filedownload.html', context)
def delete_file(request):
    test.delete()