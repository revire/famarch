from django.db import models
from django.urls import reverse
import json


class MembersField(models.TextField):

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

        FamilyMember.objects.get(first_name)

        return value.split(', ')


class FamilyMember(models.Model):

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    other_names = models.CharField(max_length=200)
    birth_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    city_of_birth = models.CharField(max_length=200)
    country_of_birth = models.CharField(max_length=200)
    education = models.CharField(max_length=200)
    job = models.CharField(max_length=200)
    comments = models.CharField(max_length=500)
    parents = MembersField(blank=True)
    # siblings = models.TextField(blank=True)

    #full_name = models.CharField(blank=True, max_length=200)

    # def set_full_name(self, x):
    #     self.full_name = f'{self.last_name} {self.first_name}'

    # @property
    # def full_name(self):
    #     return(f'{self.first_name} {self.last_name}')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


    def get_absolute_url(self):
        return reverse('view_post', args=[str(self.slug)])


class DataFile(models.Model):

    def __str__(self):
        return self.title

    file = models.FileField(upload_to='')
    title = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)

