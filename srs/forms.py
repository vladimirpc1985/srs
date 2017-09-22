from django import forms
from srs.models import Notefile, Directory, Video, Audio

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

class AudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ('url','title',)
