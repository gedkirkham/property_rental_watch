# Generated by Django 3.1.12 on 2021-06-17 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0008_remove_address_address_lookup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresslookup',
            name='place_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]