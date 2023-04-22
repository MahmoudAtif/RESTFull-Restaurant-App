from django.contrib import admin
from . import models
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.


class OpeningHourInline(admin.TabularInline):
    model = models.OpeningHour


class MenuItemInline(admin.TabularInline):
    model = models.MenuItem


class VariantInline(admin.TabularInline):
    model = models.Variant


@admin.register(models.MenuItem)
class MenuItemAdmin(SimpleHistoryAdmin):
    inlines = (VariantInline,)


class RestaurantAdmin(admin.ModelAdmin):
    inlines = (MenuItemInline,)


class MenuGroupAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'name']
    inlines = (MenuItemInline,)


class VariantAdmin(admin.ModelAdmin):
    list_display = ['item', 'size', 'price']


admin.site.register(models.Restaurant, RestaurantAdmin)
# admin.site.register(models.MenuItem, MenuItemAdmin, SimpleHistoryAdmin)
admin.site.register(models.WeekDay)
admin.site.register(models.OpeningHour),
admin.site.register(models.MenuGroup, MenuGroupAdmin),
admin.site.register(models.Size),
admin.site.register(models.Variant, VariantAdmin)
