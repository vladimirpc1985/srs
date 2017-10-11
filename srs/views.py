import re, time
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import logout
from django.core.files import File
from django.contrib import messages
from django.contrib.auth.models import User
from srs.models import Directory, Notefile, Notecard, Video, Audio, Document, Equation
from srs.forms import NotefileForm, DirectoryForm, ImportForm, VideoForm, AudioForm, DocumentForm, NotecardForm, EquationForm
from django.core import serializers
from pathlib import Path
from pytube import YouTube
import os.path
import json
import requests

def logout_view(request):
    logout(request)
    return redirect('welcome')


def welcome_text(request):
    return render(request, 'srs/welcome.html', {})


def welcome_srs(request):
    return render(request, 'srs/welcome_srs.html', {})


def getPath(request, current_directory):
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)

    path = ""
    while(current_directory != home_directory):
        path = current_directory.name + "/" + path
        current_directory = current_directory.parent_directory
    path = "/" + path
    return path


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
    path = getPath(request, current_directory)

    return render(request, 'srs/directory_view.html', {'notefiles': notefiles, 'directories': directories, 'parent': current_directory.parent_directory, 'path': path, 'pk': pk})


def selection_view(request):
    return render(request, 'srs/selection_view.html', {})


def video_list(request):
    videos = Video.objects.filter(created_date__lte=timezone.now())
    return render(request, 'srs/video_view.html', {'videos': videos})


def audio_list(request):
    audios = Audio.objects.filter(created_date__lte=timezone.now())
    return render(request, 'srs/audio_view.html', {'audios': audios})


def document_list(request):
    documents = Document.objects.filter(created_date__lte=timezone.now())
    return render(request, 'srs/document_view.html', {'documents': documents})


def create_directory(request, pk):
    duplicate = False
    parent = get_object_or_404(Directory, pk=pk)
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)

    # calculate path
    path = getPath(request, parent)

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


def create_notecard(request, pk):
    parentNotefile = get_object_or_404(Notefile, pk=pk)
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)

    # calculate path
    path = getPath(request, parentNotefile.directory) + parentNotefile.name + "/"

    if request.method == "POST":
        form = NotecardForm(request.POST)
        if form.is_valid():
            notecard = form.save(commit=False)
            notecard.author = request.user
            notecard.created_date = timezone.now()
            notecard.notefile = parentNotefile
            notecard.save()
            return redirect('notecard_list', pk=pk)
    else:
        form = NotecardForm()
    return render(request, 'srs/create_notecard.html', {'form': form, 'path': path, "pk": pk})


def login(request):
    return render(request, 'srs/login.html')


def create_account(request):
    return render(request, 'srs/create_account.html')


def notefile_list(request):
    notefiles = Notefile.objects.filter(created_date__lte=timezone.now())
    return render(request, 'srs/notefile_list.html', {'notefiles': notefiles})


def notefile_detail(request, pk):
    notefile = get_object_or_404(Notefile, pk=pk)

    # calculate path
    path = getPath(request, notefile.directory) + notefile.name + "/"

    return render(request, 'srs/notefile_detail.html', {'notefile': notefile, 'path': path})


def notefile_new(request, pk):
    duplicate = False
    parent = get_object_or_404(Directory, pk=pk)
    home_directory = Directory.objects.filter(author=request.user).get(parent_directory__isnull = True)

    # calculate path
    path = getPath(request, parent)

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

    # calculate path
    path = getPath(request, notefile_Name.directory) + notefile_Name.name + "/"

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

    # calculate path
    notefile_Name = notecard.notefile
    path = getPath(request, notefile_Name.directory) + notefile_Name.name + "/"
    if len(notecard.name) > 20:
        path += notecard.name[:20] + "..."
    else:
        path += notecard.name

    # Get the list of objects associated with this notecard.
    equations = Equation.objects.filter(notecard=notecard)
    videos = Video.objects.filter(notecard=notecard)
    audios = Audio.objects.filter(notecard=notecard)
    documents = Document.objects.filter(notecard=notecard)

    return render(request, 'srs/notecard_detail.html', {'notecard': notecard, 'pk': notecard.notefile.pk, 'path': path, 'videos': videos, 'audios': audios, 'documents': documents, 'equations': equations})


def create_video(request, pk):
    youtubeError = False
    badSource = False
    badType = False
    fileTooLarge = False
    parentNotecard = get_object_or_404(Notecard, pk=pk)

    # calculate path
    notefile_Name = parentNotecard.notefile
    path = getPath(request, notefile_Name.directory) + notefile_Name.name + "/"
    if len(parentNotecard.name) > 20:
        path += parentNotecard.name[:20] + "..."
    else:
        path += parentNotecard.name

    if(request.method == "POST"):
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user
            video.created_date = timezone.now()
            video.notecard = parentNotecard

            # video is a file on computer
            if os.path.isfile(video.url):
                with open(video.url, 'rb') as vid_file:
                    extension = os.path.splitext(video.url)[1]
                    # Make sure file has correct extension
                    if is_supported_video_extension(extension):
                        # TODO check if file < 4GB (definitely do this before saving video), also updated fileTooLarge boolean to true
                        video.video.save(video.title + time.strftime("%H%M%S") + extension, File(vid_file), save=True)
                        # TODO generate thumbnail for video
                        video.save()
                        return redirect('notecard_detail', pk=pk)
                    else:
                        badType = True
            # video is from internet or has a bad path
            else:
                # check if video is from youtube
                validation = youtube_url_validation(video.url)
                if(validation == 'valid'):
                    try:
                        #Used library defined in https://github.com/nficano/pytube
                        yt = YouTube(video.url)
                        yt.set_filename(video.title + time.strftime("%H%M%S"))
                        ytVideo = yt.filter('mp4')[-1]
                        downloadToPath = get_download_path(video.title + time.strftime("%H%M%S") + '.mp4')
                        #If directory does not exist, it is created.
                        directory = os.path.dirname(downloadToPath)
                        # TODO check if file < 4GB (probably want to check this before download function/create dir, but you could delete it after downloading it I guess), also updated fileTooLarge boolean to true
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        #Download video into local directory
                        ytVideo.download(directory)
                        video.video = downloadToPath
                        # TODO generate thumbnail for video
                        video.save()
                        return redirect('notecard_detail', pk=pk)
                    except:
                        # An error occurred with youtube
                        youtubeError = True
                        return render(request, 'srs/create_video.html', {'form': form, 'pk':pk, 'path':path, 'badSource':badSource, 'youtubeError':youtubeError, 'badType':badType})
                else:
                    try:
                        #Check to see if it's a valid internet URL
                        myRequest = requests.get(video.url)
                        if myRequest.status_code == 200:
                            #Check video extension
                            extension = os.path.splitext(video.url)[1]
                            if(is_supported_video_extension(extension)):
                                #Check if file size < 4GB
                                fileTooLarge = not is_valid_file_size(myRequest)
                                if not fileTooLarge:
                                    #Download video if its size is allowed.
                                    downloadToPath = get_download_path(video.title + time.strftime("%H%M%S") + extension)
                                    #If directory does not exist, it is created.
                                    directory = os.path.dirname(downloadToPath)
                                    if not os.path.exists(directory):
                                        os.makedirs(directory)
                                    with open(downloadToPath, 'wb') as video_file:
                                        video_file.write(myRequest.content)
                                    #Save downloaded audio into database
                                    video.video = downloadToPath
                                    # TODO generate thumbnail for video
                                    video.save()
                                    return redirect('notecard_detail', pk=pk)
                            else:
                                badType = True
                        else:
                            badSource = True
                    except:
                        badSource = True
    else:
        form = VideoForm()
    return render(request, 'srs/create_video.html', {'form': form, 'pk':pk, 'path':path, 'badSource':badSource, 'youtubeError':youtubeError, 'badType':badType, 'fileTooLarge': fileTooLarge})

#Return true if file size is less than or equal to 4GB; false otherwise.
def is_valid_file_size(request):
    size = request.headers['Content-length']
    return int(size) <= 4000000000

def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return 'valid'

    return 'invalid'


#Get the path where you want to download your video to.
def get_download_path(filename):
    return os.getcwd()+'/srs/media/videos/'+time.strftime("%Y/%m/%d")+'/'+filename

#Returns True if video extension is supported.
def is_supported_video_extension(extension):
    return extension in ('.264', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.3mm', '.3p2', '.60d', '.787', '.89', '.aaf', '.aec', '.aep', '.aepx',
                         '.aet', '.aetx', '.ajp', '.ale', '.am', '.amc', '.amv', '.amx', '.anim', '.aqt', '.arcut', '.arf', '.asf', '.asx', '.avb',
                         '.avc', '.avd', '.avi', '.avp', '.avs', '.avs', '.avv', '.axm', '.bdm', '.bdmv', '.bdt2', '.bdt3', '.bik', '.bin', '.bix',
                         '.bmk', '.bnp', '.box', '.bs4', '.bsf', '.bvr', '.byu', '.camproj', '.camrec', '.camv', '.ced', '.cel', '.cine', '.cip',
                         '.clpi', '.cmmp', '.cmmtpl', '.cmproj', '.cmrec', '.cpi', '.cst', '.cvc', '.cx3', '.d2v', '.d3v', '.dat', '.dav', '.dce',
                         '.dck', '.dcr', '.dcr', '.ddat', '.dif', '.dir', '.divx', '.dlx', '.dmb', '.dmsd', '.dmsd3d', '.dmsm', '.dmsm3d', '.dmss',
                         '.dmx', '.dnc', '.dpa', '.dpg', '.dream', '.dsy', '.dv', '.dv-avi', '.dv4', '.dvdmedia', '.dvr', '.dvr-ms', '.dvx', '.dxr',
                         '.dzm', '.dzp', '.dzt', '.edl', '.evo', '.eye', '.ezt', '.f4p', '.f4v', '.fbr', '.fbr', '.fbz', '.fcp', '.fcproject',
                         '.ffd', '.flc', '.flh', '.fli', '.flv', '.flx', '.gfp', '.gl', '.gom', '.grasp', '.gts', '.gvi', '.gvp', '.h264', '.hdmov',
                         '.hkm', '.ifo', '.imovieproj', '.imovieproject', '.ircp', '.irf', '.ism', '.ismc', '.ismv', '.iva', '.ivf', '.ivr', '.ivs',
                         '.izz', '.izzy', '.jss', '.jts', '.jtv', '.k3g', '.kmv', '.ktn', '.lrec', '.lsf', '.lsx', '.m15', '.m1pg', '.m1v', '.m21',
                         '.m21', '.m2a', '.m2p', '.m2t', '.m2ts', '.m2v', '.m4e', '.m4u', '.m4v', '.m75', '.mani', '.meta', '.mgv', '.mj2', '.mjp',
                         '.mjpg', '.mk3d', '.mkv', '.mmv', '.mnv', '.mob', '.mod', '.modd', '.moff', '.moi', '.moov', '.mov', '.movie', '.mp21',
                         '.mp21', '.mp2v', '.mp4', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg4', '.mpf', '.mpg', '.mpg2', '.mpgindex', '.mpl',
                         '.mpl', '.mpls', '.mpsub', '.mpv', '.mpv2', '.mqv', '.msdvd', '.mse', '.msh', '.mswmm', '.mts', '.mtv', '.mvb', '.mvc',
                         '.mvd', '.mve', '.mvex', '.mvp', '.mvp', '.mvy', '.mxf', '.mxv', '.mys', '.ncor', '.nsv', '.nut', '.nuv', '.nvc', '.ogm',
                         '.ogv', '.ogx', '.osp', '.otrkey', '.pac', '.par', '.pds', '.pgi', '.photoshow', '.piv', '.pjs', '.playlist', '.plproj',
                         '.pmf', '.pmv', '.pns', '.ppj', '.prel', '.pro', '.prproj', '.prtl', '.psb', '.psh', '.pssd', '.pva', '.pvr', '.pxv',
                         '.qt', '.qtch', '.qtindex', '.qtl', '.qtm', '.qtz', '.r3d', '.rcd', '.rcproject', '.rdb', '.rec', '.rm', '.rmd', '.rmd',
                         '.rmp', '.rms', '.rmv', '.rmvb', '.roq', '.rp', '.rsx', '.rts', '.rts', '.rum', '.rv', '.rvid', '.rvl', '.sbk', '.sbt',
                         '.scc', '.scm', '.scm', '.scn', '.screenflow', '.sec', '.sedprj', '.seq', '.sfd', '.sfvidcap', '.siv', '.smi', '.smi',
                         '.smil', '.smk', '.sml', '.smv', '.spl', '.sqz', '.srt', '.ssf', '.ssm', '.stl', '.str', '.stx', '.svi', '.swf', '.swi',
                         '.swt', '.tda3mt', '.tdx', '.thp', '.tivo', '.tix', '.tod', '.tp', '.tp0', '.tpd', '.tpr', '.trp', '.ts', '.tsp', '.ttxt',
                         '.tvs', '.usf', '.usm', '.vc1', '.vcpf', '.vcr', '.vcv', '.vdo', '.vdr', '.vdx', '.veg', '.vem', '.vep', '.vf', '.vft',
                         '.vfw', '.vfz', '.vgz', '.vid', '.video', '.viewlet', '.viv', '.vivo', '.vlab', '.vob', '.vp3', '.vp6', '.vp7', '.vpj',
                         '.vro', '.vs4', '.vse', '.vsp', '.w32', '.wcp', '.webm', '.wlmp', '.wm', '.wmd', '.wmmp', '.wmv', '.wmx', '.wot', '.wp3',
                         '.wpl', '.wtv', '.wve', '.wvx', '.xej', '.xel', '.xesc', '.xfl', '.xlmv', '.xmv', '.xvid', '.y4m', '.yog', '.yuv', '.zeg',
                         '.zm1', '.zm2', '.zm3', '.zmv')

def create_audio(request, pk):
    badType = False
    badSource = False
    fileTooLarge = False
    parentNotecard = get_object_or_404(Notecard, pk=pk)

    # calculate path
    notefile_Name = parentNotecard.notefile
    path = getPath(request, notefile_Name.directory) + notefile_Name.name + "/"
    if len(parentNotecard.name) > 20:
        path += parentNotecard.name[:20] + "..."
    else:
        path += parentNotecard.name

    if(request.method == "POST"):
        form = AudioForm(request.POST)
        if form.is_valid():
            audio = form.save(commit=False)
            audio.author = request.user
            audio.created_date = timezone.now()
            audio.notecard = parentNotecard

            # audio is a file on computer
            if os.path.isfile(audio.url):
                with open(audio.url, 'rb') as audio_file:
                    extension = os.path.splitext(audio.url)[1]
                    # Make sure file has correct extension
                    if is_supported_audio_extension(extension):
                        audio.audio.save(audio.title + time.strftime("%H%M%S") + extension, File(audio_file), save=True)
                        audio.save()
                        return redirect('notecard_detail', pk=pk)
                    else:
                        badType = True
            # audio is from internet or has a bad path
            else:
                try:
                    #Check if URL is valid
                    myRequest = requests.get(audio.url)
                    if myRequest.status_code == 200:
                        #Check if extension is correct.
                        extension = os.path.splitext(audio.url)[1]
                        if is_supported_audio_extension(extension):
                            #Check if file size < 4GB
                            fileTooLarge = not is_valid_file_size(myRequest)
                            if not fileTooLarge:
                                #Download audio from internet if file size is not allowed.
                                response = requests.get(audio.url)
                                downloadToPath = get_download_audio_path(audio.title + time.strftime("%H%M%S") + extension)
                                #If directory does not exist, it is created.
                                directory = os.path.dirname(downloadToPath)
                                if not os.path.exists(directory):
                                    os.makedirs(directory)
                                with open(downloadToPath, 'wb') as audio_file:
                                    audio_file.write(response.content)
                                #Store location in db and save
                                audio.audio = downloadToPath
                                audio.save()
                                return redirect('notecard_detail', pk=pk)
                        else:
                            badType = True
                    else:
                        badSource = True
                except:
                    badSource = True
    else:
        form = AudioForm()
    return render(request, 'srs/create_audio.html', {'form': form, 'pk':pk, 'path':path, "badType":badType, "badSource":badSource, "fileTooLarge":fileTooLarge})

#Returns True if audio extension is supported.
def is_supported_audio_extension(extension):
    return extension in ('.3gp', '.aa', '.aac', '.aax', '.act', '.aiff', '.amr', '.ape', '.au', '.awb', '.dct', '.dss', '.dvf', '.flac',
                         '.gsm', '.iklax', '.ivs', '.m4a', '.m4b', '.m4p', '.mmf', '.mp3', '.mpc', '.msv', '.ogg, .oga, mogg', '.opus',
                         '.ra, .rm', '.raw', '.sln', '.tta', '.vox', '.wav', '.wma', '.wv', '.webm', '.8svx')

#Get the path where you want to download your audio file to.
def get_download_audio_path(filename):
    return os.getcwd()+'/srs/media/audio/'+time.strftime("%Y/%m/%d")+'/'+filename

def create_document(request, pk):
    badType = False
    badFile = False
    fileTooLarge = False
    parentNotecard = get_object_or_404(Notecard, pk=pk)

    # calculate path
    notefile_Name = parentNotecard.notefile
    path = getPath(request, notefile_Name.directory) + notefile_Name.name + "/"
    if len(parentNotecard.name) > 20:
        path += parentNotecard.name[:20] + "..."
    else:
        path += parentNotecard.name

    if(request.method == "POST"):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.author = request.user
            document.created_date = timezone.now()
            document.notecard = parentNotecard

            # If the location contains a file
            if os.path.isfile(document.source):
                with open(document.source, 'rb') as document_file:
                    extension = os.path.splitext(document.source)[1]
                    if is_supported_document_extension(extension):
                        document.name = os.path.basename(document.source)
                        document.document.save(document.name.split('.')[0] + time.strftime("%H%M%S") + extension, File(document_file), save=True)
                        document.save()
                        return redirect('notecard_detail', pk=pk)
                    # The file type is not allowed
                    else:
                        badType = True
            # There is not a local file at that location
            else:
                #Check is there is a document online at this URL
                try:
                    myRequest = requests.get(document.source)
                    #Web site does exist; let us check if there is a file in the given URL.
                    if myRequest.status_code == 200:
                        #Check that extension is correct
                        extension = os.path.splitext(document.source)[1]
                        if(is_supported_document_extension(extension)):
                            fileTooLarge = is_valid_file_size(myRequest)
                            if not fileTooLarge:
                                response = requests.get(document.source)
                                document.name = os.path.basename(document.source)
                                downloadToPath = get_download_document_path(document.name.split('.')[0] + time.strftime("%H%M%S") + extension)
                                with open(downloadToPath, 'wb') as doc_file:
                                    doc_file.write(response.content)
                                document.document = downloadToPath
                                document.save()
                                return redirect('notecard_detail', pk=pk)
                        else:
                            badType = True
                    #Website does not exist; it is a bad URL for the document
                    else:
                        badFile = True
                #Website does not exist; it is a bad URL
                except:
                    badFile = True
    else:
        form = DocumentForm()
    return render(request, 'srs/create_document.html', {'form': form, 'pk':pk, 'badFile': badFile, 'badType': badType, 'path':path, 'fileTooLarge':fileTooLarge})

#Returns True if document extension is supported.
def is_supported_document_extension(extension):
    return extension in (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pps", ".ppsx")

#Get the path where you want to download your document to.
def get_download_document_path(filename):
    return os.getcwd()+'/srs/media/documents/'+time.strftime("%Y/%m/%d")+'/'+filename

def create_equation(request, pk):
    parentNotecard = get_object_or_404(Notecard, pk=pk)

    # calculate path
    notefile_Name = parentNotecard.notefile
    path = getPath(request, notefile_Name.directory) + notefile_Name.name + "/"
    if len(parentNotecard.name) > 20:
        path += parentNotecard.name[:20] + "..."
    else:
        path += parentNotecard.name

    if(request.method == "POST"):
        form = EquationForm(request.POST)
        if form.is_valid():
            equation = form.save(commit=False)
            equation.author = request.user
            equation.created_date = timezone.now()
            equation.notecard = parentNotecard
            print(equation.equation)
            equation.equation = equation.equation.replace('<math', '<math display="block"')
            print(equation.equation)
            equation.save()
            return redirect('notecard_detail', pk=pk)
    else:
        form = EquationForm()
    return render(request, 'srs/create_equation.html', {'form': form, 'pk':pk, 'path':path})


def about(request):
    return render(request, 'srs/about.html')


def contact(request):
    return render(request, 'srs/contact.html')

def import_notecard(request, pk):
    # calculate path
    notefile_Name = Notefile.objects.get(pk=pk)
    path = getPath(request, notefile_Name.directory) + notefile_Name.name + "/"

    if request.method == 'POST':
        form = ImportForm(request.POST)
        if form.is_valid():
            #Get full path.
            cd = form.cleaned_data
            path = cd.get('path')
            #To check if a notecard was created.
            notecards = Notecard.objects.filter(notefile=notefile_Name)
            notecards_count_before = notecards.count()
            try:
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
    checkFileFormat(request, lines, notefilePK)


def checkFileFormat(request, lines, notefilePK):
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
            init_notecard(request, keywords, header, body, notefilePK)
            #Update current_line so we can get the data from the next notecard.
            current_line = body_end_index+1
    except ValueError as err:
        print(err.args)

def init_notecard(request, keywords, header, body, notefilePK):
    str_keywords = keywords.decode('ascii', 'ignore')
    str_header = header.decode('ascii', 'ignore')
    str_body = body.decode('ascii', 'ignore')
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
    path = getPath(request, notefile_Name.directory) + notefile_Name.name + "/"

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
