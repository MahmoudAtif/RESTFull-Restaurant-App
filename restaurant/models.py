from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Restaurant(AbstractModel):
    name=  models.CharField(max_length=50, unique=True)
    description = models.TextField(verbose_name=_("Description"))
    logo = models.ImageField(upload_to='resturant_images', null=True, blank=True)
    
    def __str__(self):
        return self.name

class WeekDay(models.Model):
    name = models.CharField(verbose_name=_("Day Name"), max_length=50)
    
    def __str__(self):
        return self.name

class OpeningHour(models.Model):
    restaurant=models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='days')
    day=models.OneToOneField(WeekDay, verbose_name=_("Day"), on_delete=models.CASCADE)
    opens_at=models.TimeField()
    closes_at=models.TimeField()
    
    def __str__(self):
        return f'{self.restaurant} | {self.day}'

class MenuGroup(AbstractModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(verbose_name=_("Group Name"), max_length=50)

    def __str__(self):
        return f'{self.name} | {self.restaurant}'

class MenuItem(AbstractModel):
    
    class ItemVariant(models.IntegerChoices):
        HAS_SIZE = 0, "Has Size"
        NO_SIZE = 1, "No Size"
        
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='items')
    group = models.ForeignKey(MenuGroup, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(verbose_name=_("Item Name"), max_length=50)
    variant = models.IntegerField(choices=ItemVariant.choices)
    description = models.TextField(verbose_name=_("Description"))
    image = models.ImageField(upload_to='item_images', null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.BooleanField(verbose_name=_("Available"), default=False)

    def __str__(self):
        return f'{self.name} | {self.restaurant}'



class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Variant (AbstractModel):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='variants')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    
    def __str__(self):
        return f'{self.item} | {self.size}'