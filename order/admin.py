from django.contrib import admin
from . import models
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model=models.OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display=['user','restaurant','total_price','status','is_paid']
    inlines=(OrderItemInline,)

admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem)
admin.site.register(models.Coupon)
