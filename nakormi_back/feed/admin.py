from django.contrib import admin

from feed.models import Transfer, Report, ReportPhoto


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('tags_list', 'report', 'volume')

    def tags_list(self, obj):
        return ', '.join([related.name for related in obj.tags.all()])


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id','action', 'date', 'from_user', 'to_user', 'point')

@admin.register(ReportPhoto)
class ReportPhotoAdmin(admin.ModelAdmin):
    list_display = ('report', 'photo_list')
    def photo_list(self, obj):
        return ', '.join([str(related.pk) for related in obj.photo.all()])