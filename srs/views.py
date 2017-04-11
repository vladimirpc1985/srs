import os
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import logout
from django.core.files import File
from django.contrib import messages
from django.contrib.auth.models import User
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
        return render(request, 'srs/notecard_list_empty.html', {'notecards': notecards, 'notefile_name': name})
    else:
        return render(request, 'srs/notecard_list.html', {'notecards': notecards, 'startIndex': index})


def notecard_detail(request, pk):
    notecard = get_object_or_404(Notecard, pk=pk)
    return render(request, 'srs/notecard_detail.html', {'notecard': notecard})


def about(request):
    return render(request, 'srs/about.html')


def contact(request):
    return render(request, 'srs/contact.html')

def import_notecard(request, name):
    if request.method == 'POST':
        form = ImportForm(request.POST)
        if form.is_valid():
            #Get full path.
            cd = form.cleaned_data
            path = cd.get('path')
            #To check if a notecard was created.
            notefile_Name = Notefile.objects.get(name=name)
            notecards = Notecard.objects.filter(notefile=notefile_Name)
            notecards_count_before = notecards.count()
            try:
                readFile(request, path, name)
                notecards_count_after = notecards.count()
                if notecards_count_after > notecards_count_before:
                    return redirect('notecard_list', name=name)
                else:
                    messages.info(request, 'The path you have entered is not valid.')
                    return render(request, 'srs/import_notecard.html', {'form': form, 'name':name})
            except:
                messages.info(request, 'The path you have entered is not valid.')
            return redirect('notecard_list', name=name)
    else:
        form = ImportForm()

    return render(request, 'srs/import_notecard.html', {'form': form, 'name':name})


def readFile(request, path, notefileName):
    # open binary file in read-only mode
    fileHandler = openFile(path, 'rb')
    if fileHandler['opened']:
        # create Django File object using python's file object
        file = File(fileHandler['handler'])
        readContent(request, file, notefileName)
        file.close()


def openFile(path, mode):
    # open file using python's open method
    # by default file gets opened in read mode
    try:
        fileHandler = open(path, mode)
        return {'opened':True, 'handler':fileHandler}
    except:
        return {'opened':False, 'handler':None}


def readContent(request, file, notefileName):
    # we have at least empty file now
    # use lines to iterate over the file in lines.
    lines = []
    for line in file:
        line = line.replace(b'\t', b'')
        line = line.replace(b'\r\n', b'')
        line = line.replace(b'\n', b'')
        lines.append(line)
    #check if file is correct and create notecard if it's correct.
    checkFileFormat(request, lines, notefileName)


def checkFileFormat(request, lines, notefileName):
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
            createNotecard(request, keywords, header, body, notefileName)
            #Update current_line so we can get the data from the next notecard.
            current_line = body_end_index+1
    except ValueError as err:
        print(err.args)


def createNotecard(request, keywords, header, body, notefileName):
    bin_keywords = keywords.replace(b'\x8d',b'')
    str_keywords = bin_keywords.decode('ascii')
    bin_header = header.replace(b'\x8d',b'')
    str_header = bin_header.decode('ascii')
    bin_body = body.replace(b'\x8d',b'')
    str_body = bin_body.decode('ascii')
    if str_keywords != '' or str_header != '' or str_body != '':
        try:
            notefile_name = Notefile.objects.get(name=notefileName)
            if request.user.is_authenticated():
                user = User.objects.get(username=request.user.username)
                Notecard.objects.create(author=user,name=str_header, keywords=str_keywords, body = str_body, notefile = notefile_name)
            else:
                messages.info(request, 'You need to log in before using SRS import feature.')
        except ValueError as err:
            print(err.args)


def export_notecard(request, name):
    if request.method == 'POST':
        form = ImportForm(request.POST)
        if form.is_valid():
            #Get full path.
            cd = form.cleaned_data
            path = cd.get('path')
            path = path.upper()
            try:
                create_file(name, path)
            except:
                messages.info(request, 'The path you have entered is not valid.')
                return render(request, 'srs/export_notecard.html', {'form': form, 'name':name})
            return redirect('notecard_list', name=name)
    else:
        form = ImportForm()

    return render(request, 'srs/export_notecard.html', {'form': form, 'name':name})


def create_file(name, path):
    #Get notecard list associated to given notefile
    notefile_Name = Notefile.objects.get(name=name)
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
