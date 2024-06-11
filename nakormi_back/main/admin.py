from django.contrib import admin

from .models import District


# Register your models here.

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
