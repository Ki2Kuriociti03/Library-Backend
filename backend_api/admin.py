from django.contrib import admin
from backend_api.models import User, Profile, Book, Favourite, Rating


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['full_name', 'verified']
    list_display = ['user', 'full_name', 'verified']


admin.site.register(Favourite)
admin.site.register(Rating)
admin.site.register(Book)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
    


