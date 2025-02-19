from django import forms
from .models import DataFile, FamilyMember


def from_db_value(value, expression, connection):
    if value is None:
        return value
    return value.split(", ")


class MembersField(forms.CharField):
    def get_db_prep_value(self, value, connection, **kwargs):
        return super().get_db_prep_value(value, connection, prepared=True)

    def to_python(self, value):
        if isinstance(value, list):
            return value

        if value is None:
            return value
        return value.split(", ")


class UploadFileForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = DataFile
        fields = ["file", "title"]


class UploadOnePerson(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = (
            "first_name",
            "last_name",
            "other_names",
            "birth_name",
            "date_of_birth",
            "city_of_birth",
            "country_of_birth",
            "date_of_death",
            "city_of_death",
            "country_of_death",
            "education",
            "job",
            "notes",
            "parents",
            "partners",
        )
