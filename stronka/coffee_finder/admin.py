from django.contrib import admin
from .models import Profile, Place, Favourite, Rejected

class PlaceInLine(admin.TabularInline):
    model = Place
    extra = 0

class FavouriteInLine(admin.TabularInline):
    model = Favourite
    extra = 0

class RejectedInLine(admin.TabularInline):
    model = Rejected
    extra = 0

class ProfileAdmin(admin.ModelAdmin):
    inlines = [PlaceInLine,FavouriteInLine,RejectedInLine]

admin.site.register(Profile, ProfileAdmin)