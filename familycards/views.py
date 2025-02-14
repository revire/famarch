"""Functions of the app"""
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.template.defaultfilters import slugify
from django.conf import settings
from django.views.decorators.cache import never_cache

import os
import csv
import datetime
import mimetypes

from .models import FamilyMember
from .forms import UploadFileForm, UploadOnePerson
from .draw_tree import generate_tree

import logging


def handle_uploaded_file(file):
    """The function deals with uploaded files"""

    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    file_path = os.path.join(settings.MEDIA_ROOT, file.name)
    logging.info("Got the file_path")

    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return os.path.join('media', file.name)


def handle_date(date):
    """The function deals with the uploaded dates"""
    try:
        correct_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        date = "1900-01-01"
        correct_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    return correct_date


class IndexView(TemplateView):
    """The Initial Page. Contains list of added family members and links for other pages"""

    def get(self, request):
        context = {"family_members": FamilyMember.objects.all().order_by("first_name")}
        return render(request, "familycards/index.html", context)


class MembersView(TemplateView):
    """The Family Members Card. Shows added information about the person and provides links for relatives"""

    def get(self, request):
        family_members_upload = UploadFileForm()
        one_person_upload = UploadOnePerson()
        context = {
            "family_members": FamilyMember.objects.all()[:5],
            "family_members_upload": family_members_upload,
            "one_person_upload": one_person_upload,
        }
        return render(request, "familycards/add_members.html", context)

    def post(self, request, **data):
        family_members_upload = None
        file = UploadFileForm(request.POST, request.FILES)
        upload_messages = []
        if file.is_valid():
            uploaded_file = request.FILES["file"]
            handle_uploaded_file(uploaded_file)
            print(f"{uploaded_file.name=}")
            with open(os.path.join(settings.MEDIA_ROOT, uploaded_file.name)) as uploaded_file:
                reader = csv.reader(uploaded_file)
                for row in reader:
                    if row[0] == "first_name":
                        pass
                    elif (
                        row[0] == ""
                        and row[1] == ""
                        and row[2] == ""
                        and row[3] == ""
                        and row[4] == ""
                    ):
                        pass
                    else:
                        family_member = FamilyMember(
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
                            notes=row[12],
                            parents=str(row[13]),
                            partners=(row[14]),
                            slug=slugify(f"{row[0]}_{row[1]}_{handle_date(row[4])}"),
                            full_name=f"{row[0]} {row[1]}",
                        )
                        print(family_member, type(family_member))
                        try:
                            family_member.save()
                            upload_messages.append(f"{family_member} uploaded")
                        except:
                            upload_messages.append(
                                f"{family_member} already in database."
                            )
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
            one_person_upload.slug = slugify(
                f'{one_person_form.cleaned_data["first_name"]}_{one_person_form.cleaned_data["last_name"]}_{one_person_form.cleaned_data["date_of_birth"]}'
            )
            one_person_upload.full_name = f'{one_person_form.cleaned_data["first_name"]} {one_person_form.cleaned_data["last_name"]}'
            print("the uploads slug", one_person_upload.slug)
            # try:
            one_person_upload.parents = str(one_person_upload.parents)
            one_person_upload.partners = str(one_person_upload.partners)
            one_person_upload.save()
            upload_messages = f"{one_person_upload} uploaded"
            # except:
            upload_message = f"{one_person_upload} already in database."
            one_person_upload = UploadOnePerson()
        else:
            one_person_upload = UploadOnePerson()

        context = {
            "family_members": FamilyMember.objects.all()[:5],
            "upload_messages": upload_messages,
            "family_members_upload": family_members_upload,
            "one_person_upload": one_person_upload,
        }
        return render(request, "familycards/add_members.html", context)


def view_member(request, slug):
    member = get_object_or_404(FamilyMember, slug=slug)
    parents_list = []
    partners_list = []
    try:
        if member.parents != [""]:
            for parent in member.parents:
                p = FamilyMember.objects.filter(
                    first_name__startswith=parent.split(" ")[0]
                )[0]
                parents_list.append(get_object_or_404(FamilyMember, slug=p.slug))
        if member.partners != [""]:
            for partner in member.partners:
                p = FamilyMember.objects.filter(
                    first_name__startswith=partner.split(" ")[0]
                )[0]
                partners_list.append(get_object_or_404(FamilyMember, slug=p.slug))
    except IndexError:
        pass
    context = {"member": member, "parents": parents_list, "partners": partners_list}
    return render(request, "familycards/view_member.html", context)


def edit_member(request, slug):
    member = get_object_or_404(FamilyMember, slug=slug)
    if request.method == "POST":
        form = UploadOnePerson(request.POST, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.parents = str(member.parents)
            member.partners = str(member.partners)
            member.save()
            context = {"member": member, "slug": member.slug}
            return redirect("view_member", slug=member.slug)
    else:
        form = UploadOnePerson(instance=member)
    context = {"form": form, "member": member}
    return render(request, "familycards/edit_member.html", context)


def delete_member(request, slug):
    member = get_object_or_404(FamilyMember, slug=slug)
    delete_message = None
    member.delete()
    delete_message = f"{member} is deleted."
    context = {"delete_message": delete_message}
    return redirect("../../", context)


def delete_all(request):
    FamilyMember.objects.all().delete()
    return redirect("../")


def generate_csv(request, filename):
    family_members = FamilyMember.objects.all()
    fields = FamilyMember._meta.fields
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "first_name",
                "last_name",
                "other_names",
                "birth_names",
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
            ]
        )
        for member in family_members:
            row = []
            for field in fields:
                print(field.name.strip())
                if field.name in ("id", "slug", "full_name"):
                    pass
                elif field.name in ("parents", "partners"):
                    row.append(", ".join(getattr(member, field.name)))
                else:
                    row.append(getattr(member, field.name))
                print(row)
            writer.writerow(row)


def export_csv(request, filename):
    generate_csv(request, filename)
    generated_file = open(filename, "r")
    mime_type, _ = mimetypes.guess_type(filename)
    response = HttpResponse(generated_file, content_type=mime_type)
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response

def about(request):
    context = {}
    return render(request, "familycards/about.html", context)

@never_cache
def view_tree(request):
    tree = generate_tree()
    context = {"tree": tree}
    return render(request, "familycards/view_tree.html", context)
