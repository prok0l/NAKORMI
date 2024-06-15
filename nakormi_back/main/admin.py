from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import District, Photo

# Register your models here.
from django.contrib import admin

from .models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'preview')
    def preview(self,obj):
        try:
            if obj.photo.url:
                html = f'<br><img src="{obj.photo.url}" width="320px" height="180px"></br>'
        except:
            html = '<p>Фото не найдено</p>'
        return mark_safe(html)
