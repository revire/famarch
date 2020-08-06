from django import forms
from .models import DataFile, FamilyMember

class MembersField(forms.CharField):

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return value.split(', ')

    def get_db_prep_value(self, value, connection, **kwargs):
        return super().get_db_prep_value(value, connection, prepared=True)

    def to_python(self, value):
        if isinstance(value, list):
            return value

        if value is None:
            return value

        #FamilyMember.objects.get(first_name)

        return value.split(', ')


class UploadFileForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = DataFile
        fields = [
            'file',
            'title',
        ]

class UploadOnePerson(forms.ModelForm):

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
            'date_of_birth',
            'date_of_death',
        )


