# Generated by Django 3.1.12 on 2021-06-17 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0009_auto_20210617_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresslookup',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='addresslookup',
            name='lon',
            field=models.FloatField(blank=True, null=True),
        ),
    ]