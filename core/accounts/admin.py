from django.contrib import admin

from .models import *

admin.site.site_header = 'TSFN Portal'

# user
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'region','is_staff', 'is_superuser')
    search_fields = ('name', 'email', 'phone', 'region')
    list_filter = ('is_staff', 'is_superuser')