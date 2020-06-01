from django.contrib import admin
from .models import Profile, Favourite

class FavouriteInLine(admin.TabularInline):
    model = Favourite
    extra = 0
class ProfileAdmin(admin.ModelAdmin):
    inlines = [FavouriteInLine]

admin.site.register(Profile, ProfileAdmin)
