from django.contrib import admin
from .models import Group, GroupMember
# Register your models here.

class GroupMemberInline(admin.TabularInline):
    model = GroupMember

class GroupAdmin(admin.ModelAdmin):
    inlines = [GroupMemberInline]

admin.site.register(Group, GroupAdmin)
