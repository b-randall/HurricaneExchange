# Generated by Django 2.2.4 on 2019-10-07 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0021_stock_stock_daychangepercent'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='stock_rating',
            field=models.FloatField(default=0.0),
        ),
    ]
