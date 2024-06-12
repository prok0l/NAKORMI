from django.contrib import admin

from feed.models import Transfer, Report


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('tags_list','report','volume')
    def tags_list(self, obj):
        return ', '.join([related.name for related in obj.tags.all()])

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('tg_id','action','date')



