from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import IndexView, MembersView

from . import views

#app_name = 'familycards'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add_members', MembersView.as_view(), name='add_members'),
    path('member/<slug>', views.view_member, name='view_member'),
    path('member/<slug>/edit', views.edit_member, name='edit_member'),
    path('tree', views.view_tree, name='view_tree'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




