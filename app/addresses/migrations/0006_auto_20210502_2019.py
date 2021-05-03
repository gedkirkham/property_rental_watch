# Generated by Django 3.1.8 on 2021-05-02 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0005_auto_20210302_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresslookup',
            name='county',
            field=models.CharField(default='', max_length=50, verbose_name='County'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addresslookup',
            name='suburb',
            field=models.CharField(default='', max_length=50, verbose_name='Suburb'),
            preserve_default=False,
        ),
    ]
