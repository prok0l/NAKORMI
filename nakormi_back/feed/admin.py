from django.contrib import admin
from django.utils.safestring import mark_safe

from feed.models import Transfer, Report, ReportPhoto, TransferPhoto
from main.models import Photo


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('tags_list', 'report', 'volume')

    def tags_list(self, obj):
        return ', '.join([related.name for related in obj.tags.all()])


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id','action', 'date', 'from_user', 'to_user', 'point', 'district')

@admin.register(ReportPhoto)
class ReportPhotoAdmin(admin.ModelAdmin):
    list_display = ('report', 'photo_list', 'preview')
    readonly_fields = ['preview']
    def preview(self,obj):
        html = ''
        print(obj.photo)
        for image in [Photo.objects.get(pk = image.pk ) for image in obj.photo.all()]:
            html += (f'<a href="{image.photo.url}"><br><img src="{image.photo.url}"'
                     f' width="320px" height="180px"></br></a>')
        return mark_safe(html)
    def photo_list(self, obj):
        return ', '.join([str(related.pk) for related in obj.photo.all()])

@admin.register(TransferPhoto)
class TransferPhotoAdmin(admin.ModelAdmin):
    list_display = ('transfer', 'photo_list', 'preview')
    readonly_fields = ['preview']
    def preview(self,obj):
        html = ''
        print(obj.photo)
        for image in [Photo.objects.get(pk = image.pk ) for image in obj.photo.all()]:
            html += (f'<a href="{image.photo.url}"><br><img src="{image.photo.url}"'
                     f' width="320px" height="180px"></br></a>')
        return mark_safe(html)

    def photo_list(self, obj):
        return ', '.join([str(related.pk) for related in obj.photo.all()])