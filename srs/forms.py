from django import forms
from srs.models import Notefile, Directory, Video, Audio, Document

class ImportForm(forms.Form):
    path = forms.CharField(label='Path', max_length=100)

class NotefileForm(forms.ModelForm):
    class Meta:
        model = Notefile
        fields = ('name',)

class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = ('name',)

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('url','title',)

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['url'].label = 'Source'


class AudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ('url','title',)

    def __init__(self, *args, **kwargs):
        super(AudioForm, self).__init__(*args, **kwargs)
        self.fields['url'].label = 'Source'

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('source',)

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['source'].label = "File Location"
