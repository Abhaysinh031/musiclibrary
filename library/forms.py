from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
from django import forms
from .models import Folder, Music



class MusicForm(forms.ModelForm):
    folder = forms.ModelChoiceField(queryset=Folder.objects.none(), required=False)
    class Meta:
        model = Music
        fields = ['title', 'artist', 'genre', 'file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': 'audio/*'})
        }
    
        


    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        if file:
            if not file.content_type.startswith('audio'):
                raise forms.ValidationError("File is not an audio type")
            if file.size > 1024*1024*5:  # 5MB limit
                raise forms.ValidationError("File size exceeds 5MB")
            return file
        else:
            raise forms.ValidationError("Couldn't read uploaded file")        

class FolderForm(forms.ModelForm):
    
    class Meta:
        model = Folder
        fields = ['name']            

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = []

