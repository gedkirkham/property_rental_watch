# Generated by Django 3.1.6 on 2021-02-22 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20210221_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_class',
            field=models.CharField(default='places', max_length=50, verbose_name='Class'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default='Chester', max_length=50, verbose_name='City'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.CharField(default='United Kingdom', max_length=50, verbose_name='Country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='country_code',
            field=models.CharField(default='gb', max_length=50, verbose_name='Country code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='display_name',
            field=models.CharField(default='test', max_length=100, verbose_name='Display name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='importance',
            field=models.FloatField(default=0.1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='lat',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='lon',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='place_id',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(default='Chester', max_length=50, verbose_name='State'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='state_district',
            field=models.CharField(default='Cheshire', max_length=50, verbose_name='State district'),
            preserve_default=False,
        ),
    ]
