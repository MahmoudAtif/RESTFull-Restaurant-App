# Generated by Django 4.1.5 on 2023-04-20 14:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurant', '0001_initial'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.menuitem', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Item'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant', verbose_name='Restaurant'),
        ),
    ]
