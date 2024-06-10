from django.contrib import admin
from .forms import VolunteerCreationForm
from .models import *


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    form = VolunteerCreationForm
    list_display = ("tg_id", "name", "email", "phone", "image", "is_active", "is_admin")


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("tg_id", "tags_list", "volume")
    def tags_list(self, obj):
        return ', '.join([related.name for related in obj.tags.all()])


