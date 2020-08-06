from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.conf import settings
from django.views.generic import TemplateView
from django.template.defaultfilters import slugify
from django.http import JsonResponse
from django.core import serializers

from .models import FamilyMember
from .forms import UploadFileForm, UploadOnePerson
from .draw_tree import get_pic_name, get_list_of_parents
from .media import *

import os
import csv
import datetime
import json
import mimetypes


def handle_uploaded_file(f):
   with open(f.name, 'wb+') as destination:
      for chunk in f.chunks():
         destination.write(chunk)


def handle_date(d):
   try:
      correct_date = datetime.datetime.strptime(d, '%Y-%m-%d')
   except:
      print(d)
      d = '1900-01-01'
      correct_date = datetime.datetime.strptime(d, '%Y-%m-%d')
   return correct_date

class IndexView(TemplateView):

   def get(self, request):
      context = {'family_members': FamilyMember.objects.all().order_by('first_name')}
      return render(request, 'familycards/index.html', context)


class MembersView(TemplateView):

   def get(self, request):
      family_members_upload = UploadFileForm()
      one_person_upload = UploadOnePerson()
      context = {'family_members': FamilyMember.objects.all()[:5], 'family_members_upload': family_members_upload, 'one_person_upload':one_person_upload}
      return render(request, 'familycards/add_members.html', context)


   def post(self, request, **data):

      family_members_upload = None
      file = UploadFileForm(request.POST, request.FILES)
      upload_messages = []
      if file.is_valid():
         f = request.FILES['file']
         handle_uploaded_file(f)
         with open(f.name) as f:
            reader = csv.reader(f)
            for row in reader:
               if row[0]=='first_name':
                  pass
               elif row[0]=='' and row[1]=='' and row[2]=='' and row[3]=='' and row[4]=='':
                  pass
               else:
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
                  try:
                     created.save()
                     upload_messages.append(f'{created} uploaded')
                  except:
                     upload_messages.append(f'{created} already in database.')
         family_members_upload = UploadFileForm()
      else:
         family_members_upload = UploadFileForm()

      one_person_upload = None
      one_person_form = UploadOnePerson(request.POST)
      if one_person_form.is_valid():
         # one_person_form.save()
         f = one_person_form.save(commit=False)
         # one_person_form.cleaned_data["slug"] = slugify(f'{one_person_form.cleaned_data["first_name"]}_{one_person_form.cleaned_data["last_name"]}_{one_person_form.cleaned_data["date_of_birth"]}')
         one_person_upload = f
         one_person_upload.slug = slugify(f'{one_person_form.cleaned_data["first_name"]}_{one_person_form.cleaned_data["last_name"]}_{one_person_form.cleaned_data["date_of_birth"]}')
         one_person_upload.full_name = f'{one_person_form.cleaned_data["first_name"]} {one_person_form.cleaned_data["last_name"]}'
         print('the uploads slug', one_person_upload.slug)
         # try:
         one_person_upload.parents = str(one_person_upload.parents)
         one_person_upload.partners = str(one_person_upload.partners)
         one_person_upload.save()
         upload_messages = f'{one_person_upload} uploaded'
         # except:
         upload_message = f'{one_person_upload} already in database.'
         one_person_upload = UploadOnePerson()
      else:
         one_person_upload = UploadOnePerson()

      context = {'family_members': FamilyMember.objects.all()[:5], \
                 'upload_messages':upload_messages, \
                 'family_members_upload': family_members_upload, \
                 'one_person_upload': one_person_upload}
      return render(request, 'familycards/add_members.html', context)



def view_member(request, slug):
   member = get_object_or_404(FamilyMember, slug=slug)
   parents_list = []
   partners_list = []
   try:
      if member.parents != ['']:
         for parent in member.parents:
            p = FamilyMember.objects.filter(first_name__startswith=parent.split(' ')[0])[0]
            parents_list.append(get_object_or_404(FamilyMember, slug=p.slug))
      if member.partners != ['']:
         for partner in member.partners:
            p = FamilyMember.objects.filter(first_name__startswith=partner.split(' ')[0])[0]
            partners_list.append(get_object_or_404(FamilyMember, slug=p.slug))
   except IndexError:
      pass
   context = {'member': member, 'parents':parents_list, 'partners':partners_list}
   return render(request, 'familycards/view_member.html', context)


def edit_member(request, slug):
   member = get_object_or_404(FamilyMember, slug=slug)
   if request.method == "POST":
      form = UploadOnePerson(request.POST, instance=member)
      if form.is_valid():
         member = form.save(commit=False)
         member.parents = str(member.parents)
         member.partners = str(member.partners)
         member.save()
         context = {'member': member, 'slug':member.slug}
         return redirect('view_member', slug=member.slug)
   else:
      form = UploadOnePerson(instance=member)
   context = {'form': form, 'member':member}
   return render(request, 'familycards/edit_member.html', context)


def delete_member(request, slug):
   member = get_object_or_404(FamilyMember, slug=slug)
   delete_message = None
   print(member)
   member.delete()
   delete_message = f'{member} is deleted.'
   context = {'delete_message':delete_message}
   return redirect('../../')


def delete_all(request):
   FamilyMember.objects.all().delete()
   # context = {'message': f'{count_members} were deleted.'}
   return redirect('../')


def generate_csv(request, filename):
   family_members = FamilyMember.objects.all()
   fields = FamilyMember._meta.fields
   with open(filename, 'w') as f:
      writer = csv.writer(f)
      writer.writerow(['first_name','last_name','other_names','birth_names','date_of_birth','city_of_birth','country_of_birth','date_of_death','city_of_death','country_of_death','education','job','comments','parents','partners'])
      for member in family_members:
         row = []
         for field in fields:
            print(field.name.strip())
            if field.name in ('id', 'slug', 'full_name'):
               pass
            elif field.name in ('parents', 'partners'):
               print('THE LIST', type(getattr(member, field.name)))
               row.append(', '.join(getattr(member, field.name)))
            else:
               # print(getattr(member, field.name))
               row.append(getattr(member, field.name))
            print(row)
         writer.writerow(row)

def export_csv(request, filename):
   filename = filename
   generate_csv(request, filename)
   fl = open(filename, 'r')
   mime_type, _ = mimetypes.guess_type(filename)
   response = HttpResponse(fl, content_type=mime_type)
   response['Content-Disposition'] = f"attachment; filename={filename}"
   return response



def about(request):
   context = {'pam': 'pam'}
   return render(request, 'familycards/about.html', context)


# def view_category(request, slug):
#    category = get_object_or_404(Category, slug=slug)
#    context = {'category': category, 'posts': Blog.objects.filter(category=category)[:5]}
#    return render(request, 'imnebel/view_category.html', context)

class TreeView(TemplateView):
   # def view_tree(request):
   #    pass
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

   # def post(self, request, slug):
   #    if self.is_ajax and self.request.method == 'POST':
   #       family_member = FamilyMember.object.get(slug=slug)
   #       parents_dict = get_list_of_parents(family_member, FamilyMember)
   #       family_members = FamilyMember.objects.all()
   #       ser_instance = serializers.serialize('json', [parents_dict, family_members])
   #       #context = {'parents_dict':parents_dict, 'family_member':family_member, 'family_members':family_members}
   #       return JsonResponse({"instance": ser_instance}, status=200)
   #       # return render(request, 'familycards/view_tree.html', context)
   #
   #







