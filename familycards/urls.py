from django.urls import path
from .views import IndexView

from . import views

#app_name = 'familycards'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('member/<slug>', views.view_member, name='view_member'),
]




