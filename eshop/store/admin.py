from django.contrib import admin
from .models import Category, Item, UserProfile, Rating

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(UserProfile)
admin.site.register(Rating)
