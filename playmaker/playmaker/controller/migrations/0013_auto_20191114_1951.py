# Generated by Django 2.2.7 on 2019-11-14 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0012_remove_device_uri'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='is_active',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='is_private_session',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='is_restricted',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='is_selected',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='volume_percent',
            field=models.IntegerField(null=True),
        ),
    ]
