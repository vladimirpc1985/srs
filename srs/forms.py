from django import forms
from srs.models import Notefile, Directory

class ImportForm(forms.Form):
    path = forms.CharField(label='Path', max_length=20)

class NotefileForm(forms.ModelForm):
    class Meta:
        model = Notefile
        fields = ('name',)

class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = ('name',)
