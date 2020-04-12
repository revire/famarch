from django.contrib import admin
from .models import FamilyMember



class MemberAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('first_name', 'last_name', 'date_of_birth', )}

admin.site.register(FamilyMember, MemberAdmin)