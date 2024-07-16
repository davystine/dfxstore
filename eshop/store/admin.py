from django.contrib import admin
from .models import Category, Item, UserProfile, Rating
from django.contrib.auth.models import User

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'on_sale')
    search_fields = ('name',)
    # Optional: Add permissions here if needed

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)
admin.site.register(Rating)
