from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.conf import settings
from django.views.generic import TemplateView
from django.template.defaultfilters import slugify

from .models import FamilyMember
from .forms import UploadFileForm
from .media import *

import os
import csv
import datetime
import json


def handle_uploaded_file(f):
   with open(f.name, 'wb+') as destination:
      for chunk in f.chunks():
         destination.write(chunk)


class IndexView(TemplateView):
   template_name = 'familycards/index.html'

   def get(self, request):
      family_members_upload = UploadFileForm()
      context = {'family_members': FamilyMember.objects.all()[:5], 'family_members_upload': family_members_upload}
      return render(request, self.template_name, context)

   def post(self, request, **data):
      file = UploadFileForm(request.POST, request.FILES)
      if file.is_valid():
         f = request.FILES['file']
         handle_uploaded_file(f)
         with open(f.name) as f:
            reader = csv.reader(f)
            for row in reader:
               print(row)
               created = FamilyMember(
                  first_name=row[0],
                  last_name=row[1],
                  other_names=row[2],
                  birth_name=row[3],
                  date_of_birth=datetime.datetime.strptime(row[4], '%Y-%m-%d'),
                  city_of_birth=row[5],
                  country_of_birth=row[6],
                  education=row[7],
                  job=row[8],
                  comments=row[9],
                  parents=str(row[10]),
                  # siblings=None,
                  slug=slugify(f'{row[0]} {row[1]} {row[4]}')
               )
               print(created, type(created))
               created.save()
               print(created.parents, type(created.parents))


         message = 'Members uploaded'
         family_members_upload = UploadFileForm()
      else:
         message = UploadFileForm()

      context = {'family_members':FamilyMember.objects.all()[:5], 'message':message, 'family_members_upload':family_members_upload}
      return render(request, self.template_name, context)


def view_member(request, slug):
   member = get_object_or_404(FamilyMember, slug=slug)
   print(FamilyMember.parents)
   parents_list = []
   for parent in member.parents:
      p = FamilyMember.objects.filter(first_name__startswith=parent.split(' ')[0])[0]
      parents_list.append(get_object_or_404(FamilyMember, slug=p.slug))
   context = {'member': member, 'parents':parents_list}
   return render(request, 'familycards/view_member.html', context)


# def view_category(request, slug):
#    category = get_object_or_404(Category, slug=slug)
#    context = {'category': category, 'posts': Blog.objects.filter(category=category)[:5]}
#    return render(request, 'imnebel/view_category.html', context)


