from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import *
from django.core.files.storage import FileSystemStorage
from .models import *
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from users_acc.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#upatient files should not be in admin view (upload/download)

@login_required
def render_file_upload(request):
    if request.method == 'POST':
        up_form = Fileform(request.POST, request.FILES)
        if up_form.is_valid():
            fname = request.FILES["file"].name
            if request.FILES["file"].size <= 52428800:
                if len(fname) <= 100:
                    fcheck=False
                    for i in [".doc",".docx",".odf",".pdf",".jpeg",".jpg",".png",".bmp",".gif"]:
                        if fname.endswith(i):
                            fcheck = True
                    if fcheck==True:
                        f=Uploaded_File()
                        f.usern=request.user
                        print(request.FILES["file"].name)
                        f.file_name = request.FILES["file"].name
                        f.file =request.FILES["file"]
                        f.file_type=up_form.cleaned_data.get('file_type')
                        f.save()
                        return render(request, 'upload_download/file_upload_Complete.html')
                    else:
                        context = {"errorMsg": "Unsupported File Type The Supported File Types are .doc, .docx, .odf, .pdf, .jpeg, .jpg, .png, .bmp, .gif"}
                        print("Unsupported File Type The Supported File Types are .doc, .docx, .odf, .pdf, .jpeg, .jpg, .png, .bmp, .gif")
                        return render(request, 'upload_download/file_upload_Failed.html', context)
                else:
                    context = {"errorMsg": "Your File Name is Too Long"}
                    print(
                        "Your File Name is Too Long")
                    return render(request, 'upload_download/file_upload_Failed.html', context)
            else:
                context = {"errorMsg":"Your File is Too Big >50MB"}
                print(
                    "Your File is Too Big >50MB")
                return render(request, 'upload_download/file_upload_Failed.html', context)
        else:
            return render(request, 'upload_download/file_upload_Failed.html')
    else:
        return render(request, 'upload_download/fileupload.html',{"form":Fileform()})





@login_required
def render_file_download(request):
    files = []
    if request.method == 'POST':
        if request.user.user_type == 1:
            form = AdminProviderFileForm(request.POST)
            if form.is_valid():
                for i in Uploaded_File.objects.filter(usern=form.provider.user):
                    files.append({
                        'FileName': i.file_name,
                        'Uploader': i.usern.username,
                        'file': i.file.url,
                        'date_uploaded': i.date_created,
                        'File_Type': i.get_file_type_display(),
                        'id': i.pk
                    })
                pagination = Paginator(files, 5)
                page = request.GET.get('page', 1)
                try:
                    pagination = pagination.page(page)
                except PageNotAnInteger:
                    pagination = pagination.page(1)
                except EmptyPage:
                    pagination = pagination.page(pagination.num_pages)
                #general except 501????
                context = {
                    'file_list': pagination
                }
                return render(request, 'upload_download/filedownload.html', context)
            else:
                return render(request, 'upload_download/filedownload.html', {"form": AdminProviderFileForm()})
    else:
        if request.user.user_type == 1:
            for i in Uploaded_File.objects.all():
                # just find a way to query the request.user instead of all
                if i.usern.user_type == 2:
                    files.append({
                        'FileName': i.file_name,
                        'Uploader': i.usern.username,
                        'file': i.file.url,
                        'date_uploaded': i.date_created,
                        'File_Type': i.get_file_type_display(),
                        'id': i.pk
                    })
            pagination = Paginator(files, 5)
            page = request.GET.get('page', 1)
            try:
                pagination = pagination.page(page)
            except PageNotAnInteger:
                pagination = pagination.page(1)
            except EmptyPage:
                pagination = pagination.page(pagination.num_pages)
            context = {
                'file_list': pagination
            }
            return render(request, 'upload_download/filedownload.html', context)
        elif request.user.user_type == 2:
            temp = Uploaded_File.objects.none()
            g = Uploaded_File.objects.filter(usern=request.user)
            # provider.user.last_name.
            # user.related name of profile.Patient_count
            if request.user.provider.Provider_type == 1:
                temp = Patient.objects.filter(doc_p=request.user.provider)
            elif request.user.provider.Provider_type == 2:
                temp = Patient.objects.filter(doc_d=request.user.provider)
            elif request.user.provider.Provider_type == 3:
                temp = Patient.objects.filter(doc_c=request.user.provider)
            for i in temp:
                t = Uploaded_File.objects.filter(usern=i.user)
                g = g | t
            for i in g:
                files.append({
                    'FileName': i.file_name,
                    'Uploader': i.usern.username,
                    'file': i.file.url,
                    'date_uploaded': i.date_created,
                    'File_Type': i.get_file_type_display(),
                    'id': i.pk
                })
        elif request.user.user_type == 3:
            for i in Uploaded_File.objects.filter(usern=request.user):
                # just find a way to query the request.user instead of all
                files.append({
                    'FileName': i.file_name,
                    'Uploader': i.usern.username,
                    'file': i.file.url,
                    'date_uploaded': i.date_created,
                    'File_Type': i.get_file_type_display(),
                    'id': i.pk
                })
        pagination = Paginator(files, 5)
        page = request.GET.get('page', 1)
        try:
            pagination = pagination.page(page)
        except PageNotAnInteger:
            pagination = pagination.page(1)
        except EmptyPage:
            pagination = pagination.page(pagination.num_pages)
        context = {
            'file_list': pagination
        }
        return render(request, 'upload_download/filedownload.html', context)


@login_required
def delete_file(request, id):
    if request.method == "POST":
        obj = get_object_or_404(Uploaded_File, id=id)
        obj.delete()
        return redirect('upload_download_file_download')
    context = {'file': id}
    return render(request, "upload_download/filedeleteconfirm.html", context)
