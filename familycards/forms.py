from django import forms
from .models import DataFile




class UploadFileForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = DataFile
        fields = [
            'file',
            'title',
        ]
