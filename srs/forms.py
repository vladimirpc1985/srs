from django import forms
from .models import Post
from .models import Notefile

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class NotefileForm(forms.ModelForm):

    class Meta:
        model = Notefile
        fields = ('name',)