from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.html import mark_safe

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Vendor

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = [
        "username",
        "email",
        "display_image",
        "is_active",
        "is_superuser",
    ]

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": (
        "profile_picture",
    )}),)

    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": (
        "profile_picture",
    )}),)

    def display_image(self, obj):
        return mark_safe('<a href="{}"> <img src="{}" width="30" height="30" style="border-radius: 50%;" /> </a>'.format(obj.profile_picture.url, obj.profile_picture.url))
    display_image.short_description = 'Profile_picture'

class VendorAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "display_image",
        "contact",
        "address",
    ]

    def display_image(self, obj):
        return mark_safe('<a href="{}"> <img src="{}" width="30" height="30" style="border-radius: 50%;" /> </a>'.format(obj.image.url, obj.image.url))
    display_image.short_description = 'Image'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Vendor, VendorAdmin)
