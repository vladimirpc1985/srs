from django import forms
from .models import Notefile, Directory

class NotefileForm(forms.ModelForm):

    class Meta:
        model = Notefile
        fields = ('name',)

class DirectoryForm(forms.ModelForm):

    class Meta:
        model = Directory
        fields = ('name',)