# Generated by Django 3.1.12 on 2021-07-21 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0013_auto_20210721_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresslookup',
            name='city',
            field=models.CharField(blank=True, max_length=100, verbose_name='City'),
        ),
    ]
