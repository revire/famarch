from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.urls import reverse
from django.conf import settings
from django.views.generic import TemplateView
from django.template.defaultfilters import slugify
from django.forms import formset_factory

from .models import FamilyMember
from .forms import UploadFileForm, UploadOnePerson
from .draw_tree import get_pic_name, get_list_of_parents
from .media import *

import os
import csv
import datetime
import json


def handle_uploaded_file(f):
   with open(f.name, 'wb+') as destination:
      for chunk in f.chunks():
         destination.write(chunk)


def handle_date(d):
   try:
      correct_date = datetime.datetime.strptime(d, '%Y-%m-%d')
   except:
      correct_date = datetime.datetime.strptime(d, '%Y')
   return correct_date

class IndexView(TemplateView):
   template_name = 'familycards/index.html'

   def get(self, request):
      context = {'family_members': FamilyMember.objects.all().order_by('first_name')}
      return render(request, self.template_name, context)


class MembersView(TemplateView):

   def get(self, request):
      family_members_upload = UploadFileForm()
      one_person_upload = UploadOnePerson()
      context = {'family_members': FamilyMember.objects.all()[:5], 'family_members_upload': family_members_upload, 'one_person_upload':one_person_upload}
      return render(request, 'familycards/add_members.html', context)


   def post(self, request, **data):

      family_members_upload = None
      file = UploadFileForm(request.POST, request.FILES)
      if file.is_valid():
         f = request.FILES['file']
         handle_uploaded_file(f)
         with open(f.name) as f:
            reader = csv.reader(f)
            for row in reader:
               created = FamilyMember(
                  first_name=row[0],
                  last_name=row[1],
                  other_names=row[2],
                  birth_name=row[3],
                  date_of_birth=handle_date(row[4]),
                  city_of_birth=row[5],
                  country_of_birth=row[6],
                  date_of_death=handle_date(row[7]),
                  city_of_death=row[8],
                  country_of_death=row[9],
                  education=row[10],
                  job=row[11],
                  comments=row[12],
                  parents=str(row[13]),
                  partners=(row[14]),
                  slug=slugify(f'{row[0]}_{row[1]}_{handle_date(row[4])}'),
                  full_name=f'{row[0]} {row[1]}'
               )
               print(created, type(created))
               created.save()
               print(created.parents, type(created.parents))
         message1 = 'Family Uploaded'
         family_members_upload = UploadFileForm()
      else:
         message1 = UploadFileForm()

      one_person_upload = None
      one_person_form = UploadOnePerson(request.POST)
      if one_person_form.is_valid():
         one_person_form.save(commit=False)
         # one_person_form.cleaned_data["slug"] = slugify(f'{one_person_form.cleaned_data["first_name"]}_{one_person_form.cleaned_data["last_name"]}_{one_person_form.cleaned_data["date_of_birth"]}')
         one_person_upload = one_person_form.save()
         one_person_upload.slug = slugify(f'{one_person_form.cleaned_data["first_name"]}_{one_person_form.cleaned_data["last_name"]}_{one_person_form.cleaned_data["date_of_birth"]}')
         one_person_upload.full_name = f'{one_person_form.cleaned_data["first_name"]} {one_person_form.cleaned_data["last_name"]}'
         print('the uploads slug', one_person_upload.slug)
         one_person_upload.save()
         print(one_person_upload)
      else:
         one_person_upload = UploadOnePerson()

      context = {'family_members': FamilyMember.objects.all()[:5], \
                 'message1': message1, \
                 'family_members_upload': family_members_upload, \
                 'one_person_upload': one_person_upload}
      return render(request, 'familycards/add_members.html', context)



def view_member(request, slug):
   member = get_object_or_404(FamilyMember, slug=slug)
   print(FamilyMember.parents)
   parents_list = []
   partners_list = []
   if member.parents != ['']:
      print(member.parents)
      for parent in member.parents:
         p = FamilyMember.objects.filter(first_name__startswith=parent.split(' ')[0])[0]
         parents_list.append(get_object_or_404(FamilyMember, slug=p.slug))
   if member.partners != ['']:
      for partner in member.partners:
         p = FamilyMember.objects.filter(first_name__startswith=partner.split(' ')[0])[0]
         partners_list.append(get_object_or_404(FamilyMember, slug=p.slug))
   context = {'member': member, 'parents':parents_list, 'partners':partners_list}
   return render(request, 'familycards/view_member.html', context)


def edit_member(request, slug):
   member = get_object_or_404(FamilyMember, slug=slug)
   if request.method == "POST":
      form = UploadOnePerson(request.POST, instance=member)
      if form.is_valid():
         member = form.save(commit=False)
         member.save()
         # return render(request, 'familycards/view_member.html', slug=member.slug)
      context = {'member': member}
      return redirect(request, 'familycards/view_member.html', context)
   else:
      form = UploadOnePerson(instance=member)
   context = {'form': form, 'member':member}
   return render(request, 'familycards/edit_member.html', context)


# def view_category(request, slug):
#    category = get_object_or_404(Category, slug=slug)
#    context = {'category': category, 'posts': Blog.objects.filter(category=category)[:5]}
#    return render(request, 'imnebel/view_category.html', context)

class TreeView(TemplateView):
   def view_tree(request):
      pass
   # members = FamilyMember.objects.all()
   # print('got members')
   # tree = get_pic_name(members)
   # print('got tree')
   # context = {'tree': tree}
   # return render(request, 'familycards/view_tree.html', context)

   def get(self, request):
      family_members = FamilyMember.objects.all()
      print('got members')
      context = {'family_members': family_members}
      return render(request, 'familycards/view_tree.html', context)

   def post(self, request, slug):
      family_member = FamilyMember.object.get(slug=slug)
      parents_dict = get_list_of_parents(family_member, FamilyMember)
      family_members = FamilyMember.objects.all()
      context = {'parents_dict':parents_dict, 'family_member':family_member, 'family_members':family_members}
      return render(request, 'familycards/view_tree.html', context)









