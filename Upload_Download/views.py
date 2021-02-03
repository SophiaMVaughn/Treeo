from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Fileform



# Create your views here.

def render_file_upload(request):
    if request.method == 'POST':
        try:
            up_form = Fileform(request.POST, request.FILES)
            file = request.FILES['file']
            print(file.size)
            if up_form.is_valid():
                file = request.FILES['file']
                print(file.size)
                #if file.size()
                #return render(request, 'templates/File/fileupload.html')
        except:
            return render(request, 'file_upload_Failed.html')
        else:
            return render(request, 'file_upload_Compleate.html')
    else:
        return render(request, 'fileupload.html')
def render_file_download(request):
    files = [
        {
            'FileName': '1.pdf',
            'Author': 'JG',
            'Decription': 'First post content',
            'date_uploaded': 'August 27, 2018'
        },
        {
            'FileName': '2.doc',
            'Author': 'RAB',
            'Decription': 'First post content',
            'date_uploaded': 'August 27, 2018'
        }
    ]
    context = {
        'files': files
    }
    return render(request, 'filedownload.html', context)