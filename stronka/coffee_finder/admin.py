from django.contrib import admin
from .models import Profile, Places, Favourites, Rejected

class PlacesInLine(admin.TabularInline):
    model = Places
    extra = 0

class FavouritesInLine(admin.TabularInline):
    model = Favourites
    extra = 0

class RejectedInLine(admin.TabularInline):
    model = Rejected
    extra = 0

class ProfileAdmin(admin.ModelAdmin):
    inlines = [PlacesInLine,FavouritesInLine,RejectedInLine]

admin.site.register(Profile, ProfileAdmin)