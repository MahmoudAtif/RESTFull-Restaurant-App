from django.contrib import admin
from . import models
# Register your models here.


class OpeningHourInline(admin.TabularInline):
    model = models.OpeningHour

class MenuItemInline(admin.TabularInline):
    model = models.MenuItem

class VariantInline(admin.TabularInline):
    model = models.Variant


class WeekDayAdmin(admin.ModelAdmin):
    inlines=(OpeningHourInline,)
 
class MenuItemAdmin(admin.ModelAdmin):
    inlines = (VariantInline,)

class RestaurantAdmin(admin.ModelAdmin):
    inlines = (MenuItemInline,)

class MenuGroupAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'name']
    inlines = (MenuItemInline,)

class VariantAdmin(admin.ModelAdmin):
    list_display = ['item', 'size', 'price']


admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.MenuItem, MenuItemAdmin)
admin.site.register(models.WeekDay, WeekDayAdmin)
admin.site.register(models.OpeningHour),
admin.site.register(models.MenuGroup, MenuGroupAdmin),
admin.site.register(models.Size),
admin.site.register(models.Variant, VariantAdmin)
