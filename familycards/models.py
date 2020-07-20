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

        #FamilyMember.objects.get(first_name)

        return value.split(', ')


class FamilyMember(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    other_names = models.CharField(max_length=200, blank=True)
    birth_name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    date_of_birth = models.DateField(blank=True)
    city_of_birth = models.CharField(max_length=200, blank=True)
    country_of_birth = models.CharField(max_length=200, blank=True)
    date_of_death = models.DateField(blank=True)
    city_of_death = models.CharField(max_length=200, blank=True)
    country_of_death = models.CharField(max_length=200, blank=True)
    education = models.CharField(max_length=200, blank=True)
    job = models.CharField(max_length=200, blank=True)
    comments = models.CharField(max_length=500, blank=True)
    parents = MembersField(blank=True)
    partners = MembersField(blank=True)
    full_name = models.CharField(blank=True, max_length=200)

    # def set_full_name(self, x):
    #     self.full_name = f'{self.last_name} {self.first_name}'
    #
    # def full_name(self):
    #     return(f'{self.first_name} {self.last_name}')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('view_post', args=[str(self.slug)])

    def get_list_of_parents(self):
        parents_list = []
        for parent in self.parents:
            p = FamilyMember.objects.filter(first_name__startswith=parent.split(' ')[0])[0]
            parents_list.append(p)
        return parents_list


    def get_list_of_partners(self):
        partners_list = []
        for partner in self.partners:
            p = FamilyMember.objects.filter(first_name__startswith=partner.split(' ')[0])[0]
            partners_list.append(p)
        return partners_list


class DataFile(models.Model):

    def __str__(self):
        return self.title

    file = models.FileField(upload_to='')
    title = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)




