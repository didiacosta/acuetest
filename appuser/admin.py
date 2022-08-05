from django.contrib import admin
from .models import AppUser
# Register your models here.

class AdminAppUser(admin.ModelAdmin):
	list_display=('id','user',)
	search_field=('user',)

admin.site.register(AppUser,AdminAppUser)
