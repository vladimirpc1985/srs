from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import logout
from django.core.files import File
from django.contrib import messages
from django.contrib.auth.models import User
from srs.models import Directory, Notefile, Notecard, Video
from srs.forms import NotefileForm, DirectoryForm, ImportForm, VideoForm
from django.core import serializers
import json

def logout_view(request):
    logout(request)
    return redirect('welcome')


def welcome_text(request):
    return render(request, 'srs/welcome.html', {})


def welcome_srs(request):
    return render(request, 'srs/welcome_srs.html', {})


def home_directory(request):
    # get notefiles and directories that lie in the home directory
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)
    notefiles = Notefile.objects.filter(author=request.user).filter(directory=home_directory)
    directories = Directory.objects.filter(author=request.user).filter(parent_directory=home_directory)
    # Edit sos dynamic
    return render(request, 'srs/directory_view.html', {'notefiles': notefiles, 'directories': directories, 'path': '/', 'pk': home_directory.pk})


def directory_content(request, pk):
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)
    current_directory = Directory.objects.get(pk=pk)
    notefiles = Notefile.objects.filter(author=request.user).filter(directory=current_directory.pk)
    directories = Directory.objects.filter(author=request.user).filter(parent_directory=current_directory.pk)

    # calculate path
    temp_directory = current_directory
    path = ""
    while(temp_directory != home_directory):
        path = temp_directory.name + "/" + path
        temp_directory = temp_directory.parent_directory
    path = "/" + path

    return render(request, 'srs/directory_view.html', {'notefiles': notefiles, 'directories': directories, 'parent': current_directory.parent_directory, 'path': path, 'pk': pk})


def selection_view(request):
    return render(request, 'srs/selection_view.html', {})


def video_list(request):
    videos = Video.objects.filter(created_date__lte=timezone.now())
    return render(request, 'srs/video_view.html', {'videos': videos})

def create_directory(request, pk):
    duplicate = False
    parent = get_object_or_404(Directory, pk=pk)
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)

    # calculate path
    temp_directory = parent
    path = ""
    while(temp_directory != home_directory):
        path = temp_directory.name + "/" + path
        temp_directory = temp_directory.parent_directory
    path = "/" + path

    if parent==home_directory:
        parent_is_home = True
    else:
        parent_is_home = False

    if request.method == "POST":
        form = NotefileForm(request.POST)
        if form.is_valid():
            if Notefile.objects.filter(directory=parent).filter(name=form.cleaned_data.get('name')).exists():
                duplicate = True;
            else:
                notefile = form.save(commit=False)
                notefile.author = request.user
                notefile.created_date = timezone.now()
                notefile.directory = parent
                notefile.save()
                if parent_is_home:
                    return redirect('home_directory')
                else:
                    return redirect('directory_content', pk=pk)
    else:
        form = NotefileForm()
    return render(request, 'srs/create_notefile.html', {'form': form, 'parent_is_home': parent_is_home, 'pk': pk, 'duplicate': duplicate, 'path': path})


def ftory(request, pk):
    duplicate = False
    parent = get_object_or_404(Directory, pk=pk)
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)

    # calculate path
    temp_directory = parent
    path = ""
    while(temp_directory != home_directory):
        path = temp_directory.name + "/" + path
        temp_directory = temp_directory.parent_directory
    path = "/" + path

    if request.method == "POST":
        form = DirectoryForm(request.POST)
        if form.is_valid():
            if Directory.objects.filter(parent_directory=parent).filter(name=form.cleaned_data.get('name')).exists():
                duplicate = True;
            else:
                directory = form.save(commit=False)
                directory.author = request.user
                directory.created_date = timezone.now()
                directory.parent_directory = parent
                directory.save()
                if parent==home_directory:
                    return redirect('home_directory')
                else:
                    return redirect('directory_content', pk=pk)
    else:
        form = DirectoryForm()
    return render(request, 'srs/create_directory.html', {'form': form, 'parent': parent, 'duplicate': duplicate, 'path': path})


def login(request):
    return render(request, 'srs/login.html')


def create_account(request):
    return render(request, 'srs/create_account.html')


def notefile_list(request):
    notefiles = Notefile.objects.filter(created_date__lte=timezone.now())
    return render(request, 'srs/notefile_list.html', {'notefiles': notefiles})


def notefile_detail(request, pk):
    notefile = get_object_or_404(Notefile, pk=pk)
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)

    # calculate path
    temp_directory = notefile.directory
    path = notefile.name + "/"
    while(temp_directory != home_directory):
        path = temp_directory.name + "/" + path
        temp_directory = temp_directory.parent_directory
    path = "/" + path

    return render(request, 'srs/notefile_detail.html', {'notefile': notefile, 'path': path})


def notefile_new(request, pk):
    duplicate = False
    parent = get_object_or_404(Directory, pk=pk)
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)

    # calculate path
    temp_directory = parent
    path = ""
    while(temp_directory != home_directory):
        path = temp_directory.name + "/" + path
        temp_directory = temp_directory.parent_directory
    path = "/" + path

    if parent==home_directory:
        parent_is_home = True
    else:
        parent_is_home = False

    if request.method == "POST":
        form = NotefileForm(request.POST)
        if form.is_valid():
            if Notefile.objects.filter(directory=parent).filter(name=form.cleaned_data.get('name')).exists():
                duplicate = True;
            else:
                notefile = form.save(commit=False)
                notefile.author = request.user
                notefile.created_date = timezone.now()
                notefile.directory = parent
                notefile.save()
                if parent_is_home:
                    return redirect('home_directory')
                else:
                    return redirect('directory_content', pk=pk)
    else:
        form = NotefileForm()
    return render(request, 'srs/create_notefile.html', {'form': form, 'parent_is_home': parent_is_home, 'pk': pk, 'duplicate': duplicate, 'path': path})


#TODO figure out where this is used and maybe replace name?
def get_notefile(request):
    return request.GET.get('name')


def notecard_list(request, pk):
    notefile_Name = Notefile.objects.get(pk=pk)
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)

    # calculate path
    temp_directory = notefile_Name.directory
    path = notefile_Name.name + "/"
    while(temp_directory != home_directory):
        path = temp_directory.name + "/" + path
        temp_directory = temp_directory.parent_directory
    path = "/" + path

    notecards = Notecard.objects.filter(notefile=notefile_Name)
    queryset = serializers.serialize('json', notecards)
    queryset = json.dumps(queryset)
    notecards_count = notecards.count()
    index = 0
    if notecards_count == 0:
        return render(request, 'srs/notecard_list_empty.html', {'notecards': notecards, 'pk': pk, 'path': path})
    else:
        auto_list = ""
        for notecard in notecards:
           auto_list  += notecard.keywords + "$$"
        auto_list = auto_list.split("$$")
        auto_list = [x for x in auto_list if x != ""]
        return render(request, 'srs/notecard_list.html', {'notecards': notecards, 'startIndex': index, 'queryset': queryset, 'auto_list': auto_list, 'pk': pk, 'path': path})


def notecard_detail(request, pk):
    notecard = get_object_or_404(Notecard, pk=pk)
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)

    # calculate path
    notefile_Name = notecard.notefile
    temp_directory = notefile_Name.directory
    path = notefile_Name.name + "/"
    while(temp_directory != home_directory):
        path = temp_directory.name + "/" + path
        temp_directory = temp_directory.parent_directory
    path = "/" + path

    # Get the list of videos associated with this notecard.
    videos = Video.objects.filter(notecard__name=notecard.name)
    print("Number of videos is ")
    print(videos.count())

    return render(request, 'srs/notecard_detail.html', {'notecard': notecard, 'pk': notecard.notefile.pk, 'path': path, 'videos': videos })


def create_video(request, pk):
    #parentNotecard = get_object_or_404(Notecard, pk=pk)
    #print(parentNotecard)
    if(request.method == "POST"):
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user
            video.created_date = timezone.now()
            #video.notecard = parentNotecard
            video.save()
            return redirect('home_directory')
    else:
        form = VideoForm()
    return render(request, 'srs/create_video.html', {'form': form})


def about(request):
    return render(request, 'srs/about.html')


def contact(request):
    return render(request, 'srs/contact.html')

def import_notecard(request, pk):

    # calculate path
    notefile_Name = Notefile.objects.get(pk=pk)
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)
    temp_directory = notefile_Name.directory
    path = notefile_Name.name + "/"
    while(temp_directory != home_directory):
        path = temp_directory.name + "/" + path
        temp_directory = temp_directory.parent_directory
    path = "/" + path

    if request.method == 'POST':
        form = ImportForm(request.POST)
        if form.is_valid():
            #Get full path.
            cd = form.cleaned_data
            path = cd.get('path')
            #To check if a notecard was created.
            notecards = Notecard.objects.filter(notefile=notefile_Name)
            print(notecards.count())
            notecards_count_before = notecards.count()
            try:
                #TODO check if replacing name with pk broke this
                readFile(request, path, pk)
                notecards_count_after = notecards.count()
                if notecards_count_after > notecards_count_before:
                    return redirect('notecard_list', pk=pk)
                else:
                    messages.info(request, 'The path you have entered is not valid.')
            except:
                messages.info(request, 'The path you have entered is not valid.')
    else:
        form = ImportForm()

    return render(request, 'srs/import_notecard.html', {'form': form, 'pk':pk, 'path': path})


def readFile(request, path, notefilePK):
    # open binary file in read-only mode
    fileHandler = openFile(path, 'rb')
    if fileHandler['opened']:
        # create Django File object using python's file object
        file = File(fileHandler['handler'])
        readContent(request, file, notefilePK)
        file.close()


def openFile(path, mode):
    # open file using python's open method
    # by default file gets opened in read mode
    try:
        fileHandler = open(path, mode)
        return {'opened':True, 'handler':fileHandler}
    except:
        return {'opened':False, 'handler':None}


def readContent(request, file, notefilePK):
    # we have at least empty file now
    # use lines to iterate over the file in lines.
    lines = []
    for line in file:
        line = line.replace(b'\t', b'')
        line = line.replace(b'\r\n', b'')
        line = line.replace(b'\n', b'')
        lines.append(line)
    #check if file is correct and create notecard if it's correct.
    print("About to check format")
    checkFileFormat(request, lines, notefilePk)


def checkFileFormat(request, lines, notefilePK):
    print("checkingFormat")
    #Check whether the length of the file is greater than 5 (at least 5 delimiters)
    length = len(lines)
    if length < 5:
        raise ValueError('File has not enough lines.')
    try:
        #Get indexes for delimiters
        header_index = lines.index(b'$$<IMPORT>$$')
        #Check for errors
        if header_index != 0:
            raise ValueError('The first line does not have the required header for the SQI file.')

        length = len(lines)
        current_line = header_index+1

        while(current_line < length):
            #Get indexes for delimiters
            keyword_start_index = lines.index(b'*', current_line)
            header_start_index = lines.index(b'!', current_line)
            header_end_index = lines.index(b'$', current_line)
            body_end_index = lines.index(b'#', current_line)

            #Check for errors
            if header_index >= keyword_start_index:
                raise ValueError('Header has to be placed before keyword-start delimiter.')
            if keyword_start_index >= header_start_index:
                raise ValueError('Keyword-start delimiter has to be placed before keyword-end and header-start delimiter.')
            if header_start_index >= header_end_index:
                raise ValueError('Header-start delimiter has to be placed before header-end delimiter.')
            if header_end_index >= body_end_index:
                raise ValueError('Header-end and body-start delimiter has to be placed before body-end delimiter.')
            #Get keywords
            keywords = b''
            for i in range(length)[keyword_start_index+1:header_start_index]:
                if i+1 == header_start_index:
                    keywords += lines[i]
                else:
                    keywords += lines[i] + b', '
            #Get header/title of the notecard
            header = b''
            for i in range(length)[header_start_index+1:header_end_index]:
                header += lines[i] + b'\r\n'
            #Get body of the notecard
            body = b''
            for i in range(length)[header_end_index+1:body_end_index]:
                body += lines[i] + b'\r\n'
            #If everything's ok, then we create the notecard
            createNotecard(request, keywords, header, body, notefilePK)
            #Update current_line so we can get the data from the next notecard.
            current_line = body_end_index+1
    except ValueError as err:
        print(err.args)


def createNotecard(request, keywords, header, body, notefilePK):
    bin_keywords = keywords.replace(b'\x8d',b'')
    str_keywords = bin_keywords.decode('ascii')
    bin_header = header.replace(b'\x8d',b'')
    str_header = bin_header.decode('ascii')
    bin_body = body.replace(b'\x8d',b'')
    str_body = bin_body.decode('ascii')
    if str_keywords != '' or str_header != '' or str_body != '':
        try:
            notefile_name = Notefile.objects.get(pk=notefilePK)
            if request.user.is_authenticated():
                user = User.objects.get(username=request.user.username)
                Notecard.objects.create(author=user,name=str_header, keywords=str_keywords, body = str_body, notefile = notefile_name)
            else:
                messages.info(request, 'You need to log in before using SRS import feature.')
        except ValueError as err:
            print(err.args)


def export_notecard(request, pk):
    # calculate path
    notefile_Name = Notefile.objects.get(pk=pk)
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)
    temp_directory = notefile_Name.directory
    path = notefile_Name.name + "/"
    while(temp_directory != home_directory):
        path = temp_directory.name + "/" + path
        temp_directory = temp_directory.parent_directory
    path = "/" + path

    if request.method == 'POST':
        form = ImportForm(request.POST)
        if form.is_valid():
            #Get full path.
            cd = form.cleaned_data
            path = cd.get('path')
            path = path.upper()
            try:
                create_file(pk, path)
                return redirect('notecard_list', pk=pk)
            except:
                messages.info(request, 'The path you have entered is not valid.')
    else:
        form = ImportForm()

    return render(request, 'srs/export_notecard.html', {'form': form, 'pk':pk, 'path': path})


def create_file(pk, path):
    #Get notecard list associated to given notefile
    notefile_Name = Notefile.objects.get(pk=pk)
    notecards = Notecard.objects.filter(notefile=notefile_Name)
    #Create file
    new_file = open(path,'wb')
    #Add required header for SQI file
    new_file.write(b'$$<IMPORT>$$\n')
    for notecard in notecards:
        #Add keyword start delimiter
        new_file.write(b'*\n')
        #Add keywords
        my_keywords_list = notecard.keywords.replace(' ','').split(',')
        for kw in my_keywords_list:
            new_file.write(bytes(kw,'utf-8'))
            new_file.write(b'\n')
        #Add KEYWORD-END & HEADER-START DELIMITER
        new_file.write(b'!\n')
        #Add header
        new_file.write(bytes(notecard.name, 'utf-8'))
        #Add HEADER-END & BODY-START DELIMITER
        new_file.write(b'\n$\n')
        #Add body
        new_file.write(bytes(notecard.body, 'utf-8'))
        #Add BODY-END DELIMITER
        new_file.write(b'\n#\n')
    #Close file
    new_file.close()
