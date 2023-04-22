from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from simple_history.models import HistoricalRecords
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
# Create your models here.


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractModelHistory(models.Model):
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class Restaurant(AbstractModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(verbose_name=_("Description"))
    logo = models.ImageField(
        upload_to='resturant_images',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    def get_status(self):
        """Return restaurant status"""
        weekdays = self.days.select_related('day')
        dt = datetime.now()
        status = 'close'

        if weekdays.exists():
            for day in weekdays:
                current_day = dt.strftime('%A')
                if day.day.name == current_day:
                    if dt.time() > day.opens_at and dt.time() < day.closes_at:
                        status = 'open'
                        break
        return status


class WeekDay(models.Model):
    name = models.CharField(verbose_name=_("Day Name"), max_length=50)

    def __str__(self):
        return self.name


class OpeningHour(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='days'
    )
    day = models.OneToOneField(
        WeekDay,
        verbose_name=_("Day"),
        on_delete=models.CASCADE
    )
    opens_at = models.TimeField()
    closes_at = models.TimeField()

    def __str__(self):
        return f'{self.restaurant} | {self.day}'


class MenuGroup(AbstractModel):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    name = models.CharField(verbose_name=_("Group Name"), max_length=50)

    def __str__(self):
        return f'{self.name} | {self.restaurant}'


class MenuItem(AbstractModel, AbstractModelHistory):

    class ItemVariant(models.IntegerChoices):
        HAS_SIZE = 0, "Has Size"
        NO_SIZE = 1, "No Size"

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='items'
    )
    group = models.ForeignKey(
        MenuGroup,
        on_delete=models.CASCADE,
        related_name='items'
    )
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


class Variant(AbstractModel):
    item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.item} | {self.size}'


class Review(AbstractModel):
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name=_("Restaurant"),
        related_name='reviews',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        related_name='reviews',
        on_delete=models.CASCADE
    )
    comment = models.TextField(max_length=200)
    rating = models.FloatField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        unique_together = ['restaurant', 'user']

    def __str__(self):
        return f'{self.user} - {self.restaurant} - {self.rating}'
