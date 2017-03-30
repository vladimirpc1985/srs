from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import logout
from django.core.files import File
from srs.models import Directory, Notefile, Notecard
from srs.forms import NotefileForm, DirectoryForm, ImportForm


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
    notecards_count = notecards.count()
    index = 0
    if notecards_count == 0:
        return render(request, 'srs/notecard_list_empty.html', {})
    else:
        return render(request, 'srs/notecard_list.html', {'notecards': notecards, 'startIndex': index})


def notecard_detail(request, pk):
    notecard = get_object_or_404(Notecard, pk=pk)
    return render(request, 'srs/notecard_detail.html', {'notecard': notecard})

# def notecard_detail(request, pk):
#     notecard = get_object_or_404(Notecard, pk=pk)
#     if request.method == "POST":
#         form = NotefileForm(request.POST)
#         if form.is_valid():
#             notecard = form.save(commit=False)
#             notecard.author = request.user
#             notecard.created_date = timezone.now()
#             notecard.save()
#             return redirect('notecard_detail')
#     else:
#         form = NotefileForm()
#     return render(request, 'srs/notecard_detail.html', {'form': form})


def about(request):
    return render(request, 'srs/about.html')


def contact(request):
    return render(request, 'srs/contact.html')

def import_notecard(request, name):
    if request.method == 'POST':
        form = ImportForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            path = cd.get('path')
            print('path is ' + path)
            readFile(path, name)
            return redirect('notecard_list', name=name)
    else:
        form = ImportForm()
    return render(request, 'srs/import_notecard.html', {'form': form, 'name':name})

def readFile(path, notefileName):
    # open file in read-only mode
    fileHandler = openFile(path, 'r')
    if fileHandler['opened']:
        # create Django File object using python's file object
        file = File(fileHandler['handler'])
        readContent(file, notefileName)
        file.close()

def openFile(path, mode):
    # open file using python's open method
    # by default file gets opened in read mode
    try:
        fileHandler = open(path, mode)
        return {'opened':True, 'handler':fileHandler}
    except:
        return {'opened':False, 'handler':None}

def readContent(file, notefileName):
    # we have atleast empty file now
    # use lines to iterate over the file in lines.
    lines = []
    for line in file.readlines():
        lines.append(line)
    #check if file is correct and create notecard if it's correct.
    checkFileFormat(lines, notefileName)

def checkFileFormat(lines, notefileName):
    #Check whether the length of the file is greater than 5 (at least 5 delimiters)
    length = len(lines)
    if length < 5:
        raise ValueError('File has not enough lines.')
    try:
        #Get indexes for delimiters
        header_index = lines.index('$$<IMPORT>$$\n')
        keyword_start_index = lines.index('*\n')
        header_start_index = lines.index('!\n')
        header_end_index = lines.index('$\n')
        body_end_index = lines.index('#\n')
        #Check for errors
        if header_index != 0:
            raise ValueError('The first line does not have the required header for the SQI file.')
        if keyword_start_index != header_index+1:
            raise ValueError('The second line does not have the keyword start delimiter.')
        if header_index >= keyword_start_index:
            raise ValueError('Header has to be placed before keyword-start delimiter.')
        if keyword_start_index >= header_start_index:
            raise ValueError('Keyword-start delimiter has to be placed before keyword-end and header-start delimiter.')
        if header_start_index >= header_end_index:
            raise ValueError('Header-start delimiter has to be placed before header-end delimiter.')
        if header_end_index >= body_end_index:
            raise ValueError('Header-end and body-start delimiter has to be placed before body-end delimiter.')
        #Get keywords
        keywords = ''
        for i in range(length)[keyword_start_index+1:header_start_index]:
            if i+1 == header_start_index:
                keywords += lines[i]
            else:
                keywords += lines[i] + ', '
        #Get header/title of the notecard
        header = ''
        for i in range(length)[header_start_index+1:header_end_index]:
            header += lines[i].strip('\n')
        #Get body of the notecard
        body = ''
        for i in range(length)[header_end_index+1:body_end_index]:
            body += lines[i]
        #if everything's ok, then we create the notecard
        createNotecard(keywords, header, body, notefileName)
    except ValueError as err:
        print(err.args)

def createNotecard(keywords, header, body, notefileName):
    if keywords != '' or header != '' or body != '':
        try:
            notefile_name = Notefile.objects.get(name=notefileName)
            Notecard.objects.create(name=header, keywords=keywords, body = body, notefile = notefile_name)
        except ValueError as err:
            print(err.args)
