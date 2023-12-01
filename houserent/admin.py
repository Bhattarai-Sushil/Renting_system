from django.contrib import admin
from .models import *

# Register your models here.
class flatavailableAdmin(admin.ModelAdmin):
    list_display=('id','title')
    prepopulated_fields={'slugs':("title",)}

# class bookedAdmin(admin.ModelAdmin):
#     list_display=('flat_id','booked_user','status')
    

admin.site.register(FlatsAvailable,flatavailableAdmin)
# admin.site.register(Booked,bookedAdmin)