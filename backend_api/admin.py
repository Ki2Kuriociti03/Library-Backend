from django.contrib import admin
from backend_api.models import User, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['full_name', 'verified']
    list_display = ['user', 'full_name', 'verified']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
    


