from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import Fileform
from django.core.files.storage import FileSystemStorage
from .models import Uploaded_File
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required




@login_required
def render_file_upload(request):
    if request.method == 'POST':
        up_form = Fileform(request.POST, request.FILES)
        if up_form.is_valid():
            if request.FILES["file"].size <= 52428800:
                if len(request.FILES["file"].name) <= 100:
                #some logic ?????????
                    f=Uploaded_File()
                    f.usern=request.user
                    print(request.FILES["file"].name)
                    f.file_name = request.FILES["file"].name
                    f.file =request.FILES["file"]
                    f.save()
                return render(request, 'file_upload_Complete.html')
            else:
                context = {"errorMsg":"Your File is Too Big >50MB"}
                return render(request, 'file_upload_Failed.html', context)
        else:
            return render(request, 'file_upload_Failed.html')
    else:
        return render(request, 'fileupload.html')

@login_required
def render_file_download(request):
    files = []
    # test = Uploaded_File.objects.get(id=i.id)
    for i in Uploaded_File.objects.all():
        #just find a way to query the request.user instead of all
        files.append({
                'FileName': i.file_name,
                'Uploader': i.usern.username,
                'file': i.file.url,
                'date_uploaded': i.date_created,
                'id': i.pk
            })

    context = {
        'file_list': files
    }
    return render(request, 'filedownload.html', context)


@login_required
def delete_file(request, id):
    if request.method == "POST":
        obj = get_object_or_404(Uploaded_File, id=id)
        obj.delete()
        #find a way to actually delete the file in storage mabye a signal
        return redirect('upload_download_file_download')
    context = {'file': id}
    return render(request, "filedeleteconfirm.html", context)
