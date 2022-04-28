from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.


class PageViewAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'timestamp']


admin.site.register(PageView, PageViewAdmin)
admin.site.register(Hobby)
admin.site.register(MyUser, UserAdmin)
UserAdmin.fieldsets += ("Custom fields set",
                        {'fields': ('image', 'city', 'dob', 'hobbies', 'friends',)}),
