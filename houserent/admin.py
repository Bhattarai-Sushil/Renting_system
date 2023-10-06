from django.contrib import admin
from .models import *

# Register your models here.
class flatavailableAdmin(admin.ModelAdmin):
    list_display=('id','title')
    prepopulated_fields={'slugs':("title",)}

admin.site.register(FlatsAvailable,flatavailableAdmin)