from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import IndexView, MembersView

from . import views

# app_name = 'familycards'
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about", views.about, name="about"),
    path("delete_all", views.delete_all, name="delete_all"),
    path("add_members", MembersView.as_view(), name="add_members"),
    path("member/<slug>", views.view_member, name="view_member"),
    path("member/<slug>/edit", views.edit_member, name="edit_member"),
    path("member/<slug>/delete", views.delete_member, name="delete_member"),
    path("tree", views.view_tree, name="view_tree"),
    path("export_csv/data/<filename>", views.export_csv, name="export_csv"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
