from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.html import mark_safe

from products.models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "display_image", "date"]

    def display_image(self, obj):
        return mark_safe('<a href="{}"> <img src="{}" width="30" height="30" style="border-radius: 50%;" /> </a>'.format(obj.image.url, obj.image.url))
    display_image.short_description = 'Image'


admin.site.register(Category, CategoryAdmin)