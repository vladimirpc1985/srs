from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import logout
from .models import Directory, Notefile, Notecard
from .forms import NotefileForm, DirectoryForm
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder

def logout_view(request):
    logout(request)
    return redirect('welcome')


def welcome_text(request):
    return render(request, 'srs/welcome.html', {})


def welcome_srs(request):
    return render(request, 'srs/welcome_srs.html', {})


def home_directory(request):
    # notefiles = Notefile.objects.filter(author=request.user).filter(directory__isnull=True)
    notefiles = Notefile.objects.filter(author=request.user)
    directories = Directory.objects.filter(author=request.user).filter(parent_directory=2)
    # Edit sos dynamic
    return render(request, 'srs/directory_view.html', {'notefiles': notefiles, 'directories': directories})


def directory_content(request, name):
    current_directory = Directory.objects.get(name=name)
    notefiles = Notefile.objects.filter(author=request.user).filter(directory=current_directory.id)
    directories = Directory.objects.filter(author=request.user).filter(parent_directory=current_directory.id)
    return render(request, 'srs/directory_view.html', {'notefiles': notefiles, 'directories': directories})


def create_directory(request):
    if request.method == "POST":
        form = DirectoryForm(request.POST)
        if form.is_valid():
            directory = form.save(commit=False)
            directory.author = request.user
            directory.created_date = timezone.now()
            directory.save()
            return redirect('home_directory')
    else:
        form = DirectoryForm()
    return render(request, 'srs/create_directory.html', {'form': form})


def login(request):
    return render(request, 'srs/login.html')


def create_account(request):
    return render(request, 'srs/create_account.html')


def notefile_list(request):
    notefiles = Notefile.objects.filter(created_date__lte=timezone.now())
    return render(request, 'srs/notefile_list.html', {'notefiles': notefiles})


def notefile_detail(request, name):
    notefile = get_object_or_404(Notefile, name=name)
    return render(request, 'srs/notefile_detail.html', {'notefile': notefile})


def notefile_details(request, directory, notefile):
    current_directory = Directory.objects.get(name=directory)
    notefile = get_object_or_404(Notefile, name=notefile, directory=current_directory.id)
    return render(request, 'srs/notefile_detail.html', {'notefile': notefile})


def notefile_new(request):
    if request.method == "POST":
        form = NotefileForm(request.POST)
        if form.is_valid():
            notefile = form.save(commit=False)
            notefile.author = request.user
            notefile.created_date = timezone.now()
            notefile.save()
            return redirect('notefile_list')
    else:
        form = NotefileForm()
    return render(request, 'srs/create_notefile.html', {'form': form})


def get_notefile(request):
    return request.GET.get('name')


def notecard_list(request, name):
    notefile_Name = Notefile.objects.get(name=name)
    notecards = Notecard.objects.filter(notefile=notefile_Name)
    queryset = serializers.serialize('json', notecards)
    queryset = json.dumps(queryset)
    notecards_count = notecards.count()
    index = 0
    if notecards_count == 0:
        return render(request, 'srs/notecard_list_empty.html', {})
    else:
        return render(request, 'srs/notecard_list.html', {'notecards': notecards, 'startIndex': index, 'queryset': queryset})


def notecard_detail(request, pk):
    notecard = get_object_or_404(Notecard, pk=pk)
    return render(request, 'srs/notecard_detail.html', {'notecard': notecard})


def about(request):
    return render(request, 'srs/about.html')


def contact(request):
    return render(request, 'srs/contact.html')
