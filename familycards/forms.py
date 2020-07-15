from django import forms
from .models import DataFile, FamilyMember

class UploadFileForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = DataFile
        fields = [
            'file',
            'title',
        ]

class UploadOnePerson(forms.ModelForm):
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    other_names = forms.CharField(max_length=200, required=False)
    birth_name = forms.CharField(max_length=200, required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),
                                    input_formats=('%Y-%m-%d',),
                                    required=True)
    city_of_birth = forms.CharField(max_length=200, required=False)
    country_of_birth = forms.CharField(max_length=200, required=False)
    date_of_death = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),
                                    input_formats=('%Y-%m-%d',),
                                    required=False)
    city_of_birth = forms.CharField(max_length=200, required=False)
    city_of_death = forms.CharField(max_length=200, required=False)
    country_of_death = forms.CharField(max_length=200, required=False)
    education = forms.CharField(max_length=200, required=False)
    job = forms.CharField(max_length=200, required=False)
    comments = forms.CharField(max_length=500, required=False)
    parents = forms.CharField(max_length=500, required=False)
    partners = forms.CharField(max_length=500, required=False)

    class Meta:
        model = FamilyMember
        fields = (
            'first_name',
            'last_name',
            'other_names',
            'birth_name',
            'city_of_birth',
            'country_of_birth',
            'city_of_death',
            'country_of_death',
            'education',
            'job',
            'comments',
            'parents',
            'partners',
        )


